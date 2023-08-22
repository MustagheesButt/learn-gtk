from gi.repository import GObject, Gtk
import os


class FileNode(GObject.Object):
    __gtype_name__ = "Country"

    def __init__(self, id, name, size, is_folder, children_data):
        super().__init__()

        self._id = id
        self._name = name
        self._size = size
        self._is_folder = is_folder
        self._children = children_data

    @GObject.Property(type=str)
    def id(self):
        return self._id

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @GObject.Property(type=str)
    def size(self):
        return self._size
    
    @GObject.Property(type=bool, default=False)
    def is_folder(self):
        return self._is_folder
    
    @GObject.Property
    def children_data(self):
        return self._children

    def __repr__(self):
        return (
            f"FileNode(id={self.id}, name={self.name})"
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
