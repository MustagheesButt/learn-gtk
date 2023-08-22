import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GObject
import os
import pathlib
import threading

from helpers import FileNode, get_media_files, add_media_to_grid


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
        css_provider.load_from_file(Gio.File.new_for_path("main.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Other stuff
        grid = builder.get_object("g2")

        def bg_task():
            media_files = get_media_files()
            add_media_to_grid(grid, media_files)

        threading.Thread(None, bg_task).start()

        colview = builder.get_object("cv1")
        cols = [
            builder.get_object("colv-col1"),
            builder.get_object("colv-col2"),
            builder.get_object("colv-col3"),
        ]
        self.initialize_list(colview, cols)

    # For tree view (now ColumnView)
    # https://discourse.gnome.org/t/gtk4-gtk-listview-python-example/12323
    # https://gitlab.gnome.org/GNOME/nautilus/-/merge_requests/817/diffs#eda6bc76b1b349dba139638475451c885330f28f
    # https://github.com/amolenaar/python-gtk4-list-view/blob/main/gtk4_list_view/simple_tree.py
    # https://stackoverflow.com/questions/74556059/how-to-build-a-tree-in-gtk4-4-10#:~:text=As%20the%20document%20said%2C%20TreeView,replacement%20for%20it%20is%20ColumnView.
    def initialize_list(self, columnview, cols):
        nodes = {
            "1": ("dummy.txt", "14 KB", False, {}),
            "2": (
                "home",
                "",
                True,
                {
                    "21": ("myfile.docx", "50 KB", False, {}),
                    "22": ("archive.zip", "150 MB", False, {}),
                },
            ),
            "3": ("video.mp4", "40 MB", False, {}),
            "4": (
                "etc",
                "",
                True,
                {"41": ("ssh", "", True, {"411": ("ssh.conf", "3 KB", False, {})})},
            ),
        }

        def construct_store(data):
            store = Gio.ListStore(item_type=FileNode)
            for n in data.keys():
                new_node = FileNode(
                    id=n,
                    name=data[n][0],
                    size=data[n][1],
                    is_folder=data[n][2],
                    children_data=data[n][3],
                )
                store.append(new_node)
            return store

        self.model = construct_store(nodes)

        # https://docs.gtk.org/gtk4/callback.TreeListModelCreateModelFunc.html
        def child_model(item, user_data):
            if not item.is_folder:
                return None
            return construct_store(item.children_data)

        tree = Gtk.TreeListModel.new(
            self.model,
            passthrough=False,
            autoexpand=False,
            create_func=child_model,
            user_data=None,
        )

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup, "name")
        factory.connect("bind", self._on_factory_bind, "name")
        factory.connect("unbind", self._on_factory_unbind, "name")
        factory.connect("teardown", self._on_factory_teardown, "name")

        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self._on_factory_setup, "size")
        factory2.connect("bind", self._on_factory_bind, "size")
        factory2.connect("unbind", self._on_factory_unbind, "size")
        factory2.connect("teardown", self._on_factory_teardown, "size")

        # factory3 = Gtk.SignalListItemFactory()
        # factory3.connect("setup", self._on_factory_setup)
        # factory3.connect("bind", self._on_factory_bind, "tag")
        # factory3.connect("unbind", self._on_factory_unbind, "tag")
        # factory3.connect("teardown", self._on_factory_teardown)

        cols[0].set_factory(factory)
        # col1 = Gtk.ColumnViewColumn(title="Country", factory=factory)
        # col1.props.expand = True
        # columnview.append_column(col1)

        cols[1].set_factory(factory2)
        # cols[2].set_factory(factory3)

        model = Gtk.NoSelection(model=tree)
        columnview.set_model(model)

        columnview.props.hexpand = True
        columnview.props.vexpand = True

    def _on_factory_setup(self, factory, list_item, what):
        cell = Gtk.Inscription()
        cell._binding = None
        if what == "name":
            expander = Gtk.TreeExpander()
            expander.set_child(cell)
            cell = expander
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        if what == "name":
            cell = cell.get_child()

        item = list_item.get_item()
        while isinstance(item, Gtk.TreeListRow):
            item = item.get_item()
        cell._binding = item.bind_property(
            what, cell, "text", GObject.BindingFlags.SYNC_CREATE
        )
        cell.set_hexpand(True)

        if what == "name":
            expander = list_item.get_child()
            expander.set_list_row(list_item.get_item())

    def _on_factory_unbind(self, factory, list_item, what):
        cell = list_item.get_child()
        if what == "name":
            cell = cell.get_child() # because it is a TreeExpander
        if cell._binding:
            cell._binding.unbind()
            cell._binding = None

    def _on_factory_teardown(self, factory, list_item, what):
        cell = list_item.get_child()
        if cell is not None:
            cell._binding = None

    def _on_selected_item_notify(self, dropdown, _):
        country = dropdown.get_selected_item()
        print(f"Selected item: {country}")


app = MyApp(application_id="com.example.GtkApplication")

app.run(sys.argv)
