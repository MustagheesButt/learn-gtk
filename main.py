import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GObject
import os
import pathlib

from helpers import Country, get_media_files, add_media_to_grid


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
        media_files = get_media_files()
        add_media_to_grid(grid, media_files)

        colview = builder.get_object("cv1")
        cols = [
            builder.get_object("colv-col1"),
            builder.get_object("colv-col2"),
            builder.get_object("colv-col3")
        ]
        self.initialize_list(colview, cols)
    
    # For tree view (now ColumnView)
    # https://discourse.gnome.org/t/gtk4-gtk-listview-python-example/12323
    # https://gitlab.gnome.org/GNOME/nautilus/-/merge_requests/817/diffs#eda6bc76b1b349dba139638475451c885330f28f
    # https://github.com/amolenaar/python-gtk4-list-view/blob/main/gtk4_list_view/simple_tree.py
    def initialize_list(self, columnview, cols):
        nodes = {
            "au": ("Austria", "Van der Bellen", "europe"),
            "uk": ("United Kingdom", "Charles III", "europe"),
            "us": ("United States", "Biden", "NA"),
        }

        self.model = Gio.ListStore(item_type=Country)
        for n in nodes.keys():
            self.model.append(Country(country_id=n, country_name=nodes[n][0], pm=nodes[n][1], tag=nodes[n][2]))

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

        factory3 = Gtk.SignalListItemFactory()
        factory3.connect("setup", self._on_factory_setup)
        factory3.connect("bind", self._on_factory_bind, "country_tag")
        factory3.connect("unbind", self._on_factory_unbind, "country_tag")
        factory3.connect("teardown", self._on_factory_teardown)

        cols[0].set_factory(factory)
        # col1 = Gtk.ColumnViewColumn(title="Country", factory=factory)
        # col1.props.expand = True
        # columnview.append_column(col1)

        cols[1].set_factory(factory2)
        cols[2].set_factory(factory3)

        model=Gtk.NoSelection(model=self.model)
        columnview.set_model(model)


        columnview.props.hexpand = True
        columnview.props.vexpand = True

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


app = MyApp(application_id="com.example.GtkApplication")

app.run(sys.argv)
