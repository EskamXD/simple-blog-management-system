import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from MVC.Views.View import View

class PhotoGalleryView(View):
    def __init__(self, root, tab):
        super().__init__(root, tab)

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
            text="Photo gallery",
            fill="#FFFFFF",
            font=("OpenSansRoman Regular", 32 * -1),
            justify="center",
            width=700,
        )

        # Photo gallery
        self.photo_gallery = ttk.Treeview(self.canvas, bootstyle="primary")

    def place(self):
        self.canvas.place(x=0, y=0)
        self.photo_gallery.place(x=30.0, y=120.0, width=640.0, height=450.0)
