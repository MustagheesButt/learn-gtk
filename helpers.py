from gi.repository import GObject, Gtk
import os


class Country(GObject.Object):
    __gtype_name__ = "Country"

    def __init__(self, country_id, country_name, pm, tag):
        super().__init__()

        self._country_id = country_id
        self._country_name = country_name
        self._country_pm = pm
        self._country_tag = tag

    @GObject.Property(type=str)
    def country_id(self):
        return self._country_id

    @GObject.Property(type=str)
    def country_name(self):
        return self._country_name

    @GObject.Property(type=str)
    def country_pm(self):
        return self._country_pm
    
    @GObject.Property(type=str)
    def country_tag(self):
        return self._country_tag

    def __repr__(self):
        return (
            f"Country(country_id={self.country_id}, country_name={self.country_name})"
        )


def get_media_files():
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


def add_media_to_grid(grid, files):
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
