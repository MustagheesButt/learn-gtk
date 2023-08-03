import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
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
        grid = builder.get_object("g2")

        # Obtain and show the main window
        self.win = builder.get_object("main_window")
        self.win.set_application(
            self
        )  # Application will close once it no longer has active windows attached to it
        self.win.present()

        media_files = self.get_media_files()
        self.add_media_to_grid(grid, media_files)

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


app = MyApp(application_id="com.example.GtkApplication")

app.run(sys.argv)
