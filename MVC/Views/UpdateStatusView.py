# import textwrap
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Composite.Article import Article
from Composite.Category import Category

from MVC.Views.View import View

from Strategy.ArticleStatusChanger import ArticleStatusChanger

from UpdateObserver.Observer import Observer
from UpdateObserver.Subject import Subject

class UpdateStatusView(View, Observer):
    def __init__(self, root, tab, controller) -> None:
        super().__init__(root, tab)
        self.controller = controller

        self.selected_category = tk.StringVar()
        self.selected_article = tk.StringVar()
        self.selected_status = tk.StringVar()

        # Add article tab
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
            text="Add article to the system",
            fill="#FFFFFF",
            font=("OpenSansRoman Regular", 32 * -1),
            justify="center",
            width=700,
        )

        self.frame = ttk.Frame(self.canvas)

        # Category label
        self.category_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Update article status"
        )

        # Category combobox
        self.category_menubutton = ttk.Menubutton(
            self.canvas,
            bootstyle="outline-primary",
            state="readonly",
            textvariable=self.selected_category,  # Link the variable to the Menubutton
        )
        self.category_menubutton.menu = tk.Menu(self.category_menubutton, tearoff=0)

        # Article label
        self.article_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Article name"
        )

        # Article combobox
        self.article_menubutton = ttk.Menubutton(
            self.canvas,
            bootstyle="outline-primary",
            state="disabled",
            textvariable=self.selected_article,  # Link the variable to the Menubutton
        )
        self.article_menubutton.menu = tk.Menu(self.article_menubutton, tearoff=0)

        # Status label
        self.status_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Article status"
        )

        # Status combobox
        self.status_menubutton = ttk.Menubutton(
            self.canvas,
            bootstyle="outline-primary",
            state="disabled",
            textvariable=self.selected_status,  # Link the variable to the Menubutton
        )
        self.status_menubutton.menu = tk.Menu(self.status_menubutton, tearoff=0)

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
        self.category_menubutton.place(x=30.0, y=170.0, width=300.0, height=40.0)
        self.category_menubutton["menu"] = self.category_menubutton.menu

        for child in self.root.children:
            self.category_menubutton.menu.add_radiobutton(
                label=child.name,
                value=child.name,
                command=lambda name=child.name: (
                    self.selected_category.set(name),
                    self.controller.update_article_list(name),
                ),
            )
          
        
        self.article_label.place(x=30.0, y=210.0, width=300.0, height=20.0)
        self.article_menubutton.place(x=30.0, y=230.0, width=300.0, height=40.0)
        self.article_menubutton["menu"] = self.article_menubutton.menu


        self.status_label.place(x=30.0, y=270.0, width=300.0, height=20.0)
        self.status_menubutton.place(x=30.0, y=290.0, width=300.0, height=40.0)
        self.status_menubutton["menu"] = self.status_menubutton.menu
 

        self.save_button.place(x=30.0, y=460.0, width=150.0, height=40.0)
        self.save_button.bind("<Button-1>", lambda *args: self.controller.save())

        self.cancel_button.place(x=30.0, y=520.0, width=150.0, height=40.0)
        self.cancel_button.bind("<Button-1>", lambda *args: self.controller.cancel())

    def update(self, subject: Subject) -> None:
        self.category_menubutton.menu.delete(0, tk.END)
        self.article_menubutton.menu.delete(0, tk.END)
        self.status_menubutton.menu.delete(0, tk.END)
        for child in self.root.children:
            self.category_menubutton.menu.add_radiobutton(
                label=child.name,
                value=child.name,
                command=lambda name=child.name: (
                    self.selected_category.set(name),
                    self.controller.update_article_list(name),
                ),
            )