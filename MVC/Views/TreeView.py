import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from MVC.Views.View import View

class TreeView(View):
    def __init__(self, root, tab):
        super().__init__(root, tab)

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

        # Treeview
        self.treeview = ttk.Treeview(self.canvas, bootstyle="primary")

        # Scrollbar
        # self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical")


    def place(self):
        self.canvas.place(x=0, y=0)

        self.treeview.place(x=0.0, y=120.0, width=700.0, height=450.0)
        self.treeview = self.insert_treeview(self.treeview)

        # self.scrollbar.place(x=680.0, y=120.0, height=450.0)
        # self.scrollbar.configure(command=self.treeview.yview)
        # self.treeview.configure(yscrollcommand=self.scrollbar.set)


    def insert_treeview(self, treeview: ttk.Treeview):
        # Define columns
        treeview["columns"] = ("Category", "Article", "Creation Date")

        # Configure column properties
        treeview.column("#0", width=50, anchor=tk.W, stretch=True)  # The first column (tree branches)
        treeview.column("Category", width=150, anchor=tk.W, stretch=True)
        treeview.column("Article", width=150, anchor=tk.W, stretch=True)
        # treeview.column("Type", width=100, anchor=tk.W, stretch=True)
        treeview.column("Creation Date", width=100, anchor=tk.W, stretch=True)

        # Set column headings
        treeview.heading("#0", text="", anchor=tk.W)
        treeview.heading("Category", text="| Category", anchor=tk.W)
        treeview.heading("Article", text="| Article", anchor=tk.W)
        # treeview.heading("Type", text="| Type", anchor=tk.W)
        treeview.heading("Creation Date", text="| Creation Date", anchor=tk.W)

        # Insert data into treeview
        for category in self.root.children:
            category_item = treeview.insert("", tk.END, values=(f"{category.name}", "", ""))
            for article in category.children:
                article_item = treeview.insert(category_item, tk.END, values=("", f"{article.title}", article.creation_date))


