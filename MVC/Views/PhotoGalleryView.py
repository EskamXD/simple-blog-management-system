import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

from MVC.Views.View import View

ARTICLES_PATH = str("data")

class PhotoGalleryView(View):
    def __init__(self, root, tab, controller):
        super().__init__(root, tab)
        self.controller = controller
        
        # Photo gallery tab
        # Title text
        self.canvas = ttk.Canvas(
            self.tab,             
            autostyle=False,
            background="#23232B",
            border=0,
            highlightthickness=0,
            height=570,
            width=700,
        )
        self.canvas.create_text(
            20.0,
            40.0,
            anchor="nw",
            text="Category tree",
            fill="#FFFFFF",
            font=("OpenSansRoman Regular", 32 * -1),
            justify="center",
            width=700,
        )

        self.frame = ScrolledFrame(self.tab, autohide=False)

    def place(self):
        self.canvas.place(x=0, y=0)
        self.frame.place(x=0, y=120.0, width=695.0, height=490.0)