import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GObject
import os
import pathlib


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        builder = Gtk.Builder()
        builder.add_from_file("main.ui")

        # Obtain the button widget and connect it to a function
        # button = builder.get_object("btn1")
        # button.connect("clicked", self.hello)

        # Obtain and show the main window
        self.win = builder.get_object("main_window")
        self.win.set_application(
            self
        )  # Application will close once it no longer has active windows attached to it
        self.win.present()

        # Apply styles
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(Gio.File.new_for_path('main.css'))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Other stuff
        grid = builder.get_object("g2")
        media_files = self.get_media_files()
        self.add_media_to_grid(grid, media_files)

        colview = builder.get_object("cv1")
        self.initialize_list(colview)

    def get_media_files(self):
        dirs = ["/Users/mustaghees/Movies", "/Users/mustaghees/Projects"]
        exts = [
            ".3g2",
            ".3gp",
            ".asf",
            ".asx",
            ".avi",
            ".flv",
            ".m2ts",
            ".mkv",
            ".mov",
            ".mp4",
            ".mpg",
            ".mpeg",
            ".rm",
            ".swf",
            ".vob",
            ".wmv",
        ]
        # exts = [".mkv"]
        found = []

        for dir in dirs:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    if file.endswith(tuple(exts)):
                        found.append(os.path.join(root, file))

        return found

    def add_media_to_grid(self, grid, files):
        for i in range(len(files)):
            file = files[i]
            x = i % 3
            y = int(i / 3)

            media = Gtk.MediaFile.new_for_filename(file)
            video = Gtk.Video.new_for_media_stream(media)
            video.set_autoplay(True)
            video.set_hexpand(True)
            video.set_vexpand(True)

            # btn = Gtk.Button(label=file)
            grid.attach(video, x, y, 1, 1)
    
    # For tree view (now ColumnView)
    # https://discourse.gnome.org/t/gtk4-gtk-listview-python-example/12323
    # https://gitlab.gnome.org/GNOME/nautilus/-/merge_requests/817/diffs#eda6bc76b1b349dba139638475451c885330f28f
    # https://github.com/amolenaar/python-gtk4-list-view/blob/main/gtk4_list_view/simple_tree.py
    def initialize_list(self, columnview):
        nodes = {
            "au": ("Austria", "Van der Bellen"),
            "uk": ("United Kingdom", "Charles III"),
            "us": ("United States", "Biden"),
        }

        self.model = Gio.ListStore(item_type=Country)
        for n in nodes.keys():
            self.model.append(Country(country_id=n, country_name=nodes[n][0], pm=nodes[n][1]))

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, "country_name")
        factory.connect("unbind", self._on_factory_unbind, "country_name")
        factory.connect("teardown", self._on_factory_teardown)

        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self._on_factory_setup)
        factory2.connect("bind", self._on_factory_bind, "country_pm")
        factory2.connect("unbind", self._on_factory_unbind, "country_pm")
        factory2.connect("teardown", self._on_factory_teardown)

        model=Gtk.NoSelection(model=self.model)
        self.cv = columnview
        self.cv.set_model(model)
        col1 = Gtk.ColumnViewColumn(title="Country", factory=factory)
        col1.props.expand = True
        self.cv.append_column(col1)
        col2 = Gtk.ColumnViewColumn(title="Head of State", factory=factory2)
        col2.props.expand = True
        self.cv.append_column(col2)
        self.cv.props.hexpand = True
        self.cv.props.vexpand = True

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        country = list_item.get_item()
        cell._binding = country.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def _on_factory_unbind(self, factory, list_item, what):
        cell = list_item.get_child()
        if cell._binding:
            cell._binding.unbind()
            cell._binding = None

    def _on_factory_teardown(self, factory, list_item):
        cell = list_item.get_child()
        cell._binding = None

    def _on_selected_item_notify(self, dropdown, _):
        country = dropdown.get_selected_item()
        print(f"Selected item: {country}")


class Country(GObject.Object):
    __gtype_name__ = "Country"

    def __init__(self, country_id, country_name, pm):
        super().__init__()

        self._country_id = country_id
        self._country_name = country_name
        self._country_pm = pm

    @GObject.Property(type=str)
    def country_id(self):
        return self._country_id

    @GObject.Property(type=str)
    def country_name(self):
        return self._country_name

    @GObject.Property(type=str)
    def country_pm(self):
        return self._country_pm

    def __repr__(self):
        return f"Country(country_id={self.country_id}, country_name={self.country_name})"


app = MyApp(application_id="com.example.GtkApplication")

app.run(sys.argv)
