import textwrap
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Composite.Article import Article
from Composite.Category import Category

from MVC.Views.View import View

class TreeView(View):
    def __init__(self, root, tab, controller) -> None:
        super().__init__(root, tab)
        self.controller = controller

        # Tree tab
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

        self.frame = ttk.Frame(self.canvas)

        # Treeview
        self.treeview = ttk.Treeview(self.canvas, bootstyle="primary")

        # Category label
        self.category_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Create new category"
        )

        # Category entry
        self.category_create = ttk.Entry(
            self.canvas, bootstyle="primary", width=50
        ) 

        # Existing category label
        self.existing_category_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Existing categories"
        )

        # Existing category list
        self.existing_category_listbox = tk.Listbox(
            self.canvas, width=50
        )

        # Save button
        self.save_button = ttk.Button(
            self.canvas, bootstyle="outline-success", text="Save"
        )

        # Cancel button
        self.cancel_button = ttk.Button(
            self.canvas, bootstyle="outline-danger", text="Cancel"
        )

    def place(self):
        self.canvas.place(x=0, y=0)
        self.frame.place(x=0, y=120.0, width=700.0, height=490.0)


        self.category_label.place(x=30.0, y=150.0, width=300.0, height=20.0)
        self.category_create.place(x=30.0, y=180.0, width=300.0, height=40.0)

        self.existing_category_label.place(x=30.0, y=250.0, width=300.0, height=20.0)
        self.existing_category_listbox.place(x=30.0, y=280.0, width=300.0, height=150.0)
        
        for category in self.root.children:
            self.existing_category_listbox.insert(tk.END, category.name)

        self.save_button.place(x=30.0, y=460.0, width=150.0, height=40.0)
        self.save_button.bind("<Button-1>", lambda *args: self.controller.save())

        self.cancel_button.place(x=30.0, y=520.0, width=150.0, height=40.0)
        self.cancel_button.bind("<Button-1>", lambda *args: self.controller.cancel())

        self.canvas.place(x=0, y=0)

        self.treeview.place(x=370.0, y=120.0, width=300.0, height=490.0)
        self.treeview = self.controller.insert_treeview(self.treeview)
