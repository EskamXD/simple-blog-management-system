from BlogManagement.BlogManagement import BlogManagement
from Composite.Category import Category
from Composite.Article import Article
from Database import Database

from Strategy.ValidationStrategy import ValidationStrategy
from Strategy.MetaTitleValidator import MetaTitleValidator
from Strategy.MetaDescriptionValidator import MetaDescriptionValidator
from Strategy.ImageSizeValidator import ImageSizeValidator
from Strategy.ArticleStatusChanger import ArticleStatusChanger

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

ARTICLES_PATH = str("data")


class GUI(BlogManagement):
    def __init__(self, db: "Database", root: "Category") -> None:
        self.db = db
        self.root = root
        self.window = ttk.Window(themename="superhero")
        self.window.title("Blog Management")
        self.window.geometry("700x570")
        self.window.configure(bg="#23232B")
        self.window.resizable(False, False)

        self.selected_category = tk.StringVar()

        # Load state from JSON
        try:
            self.root.load_composite_recursive("main_state.json")
        except FileNotFoundError:
            pass

    def run(self) -> None:
        # Menu Notebook
        menu = ttk.Notebook(self.window, bootstyle="dark")
        menu.pack(fill=BOTH, expand=True)

        # All app tabs
        add_article_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(add_article_tab, text="Add article")
        tree_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(tree_tab, text="Category tree")
        photo_gallery_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(photo_gallery_tab, text="Photo gallery")

        # Add article tab
        # Title text
        canvas = ttk.Canvas(
            add_article_tab,
            autostyle=False,
            background="#23232B",
            border=0,
            highlightthickness=0,
            height=570,
            width=700,
        )
        canvas.place(x=0, y=0)
        canvas.create_text(
            20.0,
            40.0,
            anchor="nw",
            text="Add article to the system",
            fill="#FFFFFF",
            font=("OpenSansRoman Regular", 32 * -1),
            justify="center",
            width=700,
        )

        frame = ttk.Frame(canvas)
        frame.place(x=0, y=120.0, width=700.0, height=450.0)

        # Category label
        category_label = ttk.Label(canvas, bootstyle="primary", text="Article category")
        category_label.place(x=30.0, y=150.0, width=300.0, height=20.0)

        # Category combobox
        category_menubutton = ttk.Menubutton(
            canvas,
            bootstyle="outline-primary",
            state="readonly",
            textvariable=self.selected_category,  # Link the variable to the Menubutton
        )
        category_menubutton.place(x=30.0, y=170.0, width=300.0, height=40.0)
        category_menubutton.menu = tk.Menu(category_menubutton, tearoff=0)
        category_menubutton["menu"] = category_menubutton.menu

        for child in self.root.children:
            category_menubutton.menu.add_radiobutton(
                label=child.name,
                value=child.name,
                command=lambda name=child.name: self.on_category_selected(name),
            )

        # Meta title label
        meta_title_label = ttk.Label(
            canvas, bootstyle="primary", text="Article meta title"
        )
        meta_title_label.place(x=30.0, y=210.0, width=300.0, height=20.0)

        # Meta title entry
        meta_title_entry = ttk.Entry(canvas, bootstyle="primary", width=50)
        meta_title_entry.place(x=30.0, y=230.0, width=300.0, height=40.0)

        # Meta description labelframe
        meta_description_label = ttk.Label(
            canvas,
            bootstyle="primary",
            text="Article meta description",
        )
        meta_description_label.place(x=370.0, y=150.0, width=300.0, height=20.0)

        # Meta description entry
        meta_description_entry = ttk.Text(
            canvas, highlightcolor="red", relief="solid", width=50, wrap="word"
        )
        meta_description_entry.place(x=370.0, y=170.0, width=300.0, height=100.0)

        # Line
        canvas.create_line(
            30.0,
            290.0,
            670.0,
            290.0,
            fill="#FFFFFF",
            width=1,
        )

        # Image rectangle
        canvas.create_rectangle(
            310.0,
            310.0,
            670.0,
            450.0,
            fill="#D9D9D9",
            outline="",
        )

        # Image button
        image_button = ttk.Button(
            canvas, bootstyle="outline-primary", text="Choose image"
        )
        image_button.place(x=30.0, y=310.0, width=150.0, height=40.0)

        # Thumbnail toggle
        thumbnail_toggle = ttk.Checkbutton(
            canvas, bootstyle="round-toggle", text="Thumbnail"
        )
        thumbnail_toggle.place(x=30.0, y=370.0, width=150.0, height=20.0)

        # Save button
        save_button = ttk.Button(canvas, bootstyle="outline-success", text="Save")
        save_button.place(x=30.0, y=420.0, width=150.0, height=40.0)

        # Cancel button
        cancel_button = ttk.Button(canvas, bootstyle="outline-danger", text="Cancel")
        cancel_button.place(x=30.0, y=480.0, width=150.0, height=40.0)

        # Tree tab
        # Title text
        canvas = ttk.Canvas(
            tree_tab,             
            autostyle=False,
            background="#23232B",
            border=0,
            highlightthickness=0,
            height=570,
            width=700,
        )
        canvas.place(x=0, y=0)
        canvas.create_text(
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
        treeview = ttk.Treeview(canvas, bootstyle="primary")
        treeview.place(x=30.0, y=120.0, width=640.0, height=450.0)

        #insert into treeview composite tree
        category_tree = self.root.operation()
        print(category_tree)
        treeview = self.insert_treeview(category_tree, treeview)

        # Photo gallery tab
        # Title text
        canvas = ttk.Canvas(
            photo_gallery_tab,
            autostyle=False,
            background="#23232B",
            border=0,
            highlightthickness=0,
            height=570,
            width=700,
        )
        canvas.place(x=0, y=0)
        canvas.create_text(
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
        photo_gallery = ttk.Treeview(canvas, bootstyle="primary")
        photo_gallery.place(x=30.0, y=120.0, width=640.0, height=450.0)

        self.window.mainloop()

    def on_category_selected(self, category_name: str) -> None:
        # Update the selected_category variable
        self.selected_category.set(category_name)

    def validate_meta_title(self, meta_title_entry: ttk.Entry) -> None:
        # Get the meta title from the entry widget
        meta_title = meta_title_entry.get()
        print(meta_title_entry, meta_title)
        # Validate the meta title using the MetaTitleValidator
        is_valid = self.title_validator.validate(meta_title)

        # Change the style of the entry based on validation result
        if is_valid == 1:
            meta_title_entry.configure(bootstyle="success")
        elif is_valid == -1:
            meta_title_entry.configure(bootstyle="danger")
        else:
            meta_title_entry.configure(bootstyle="primary")

    def insert_treeview(self, node, treeview, parent=ARTICLES_PATH):
        for child in self.root.children:
            if isinstance(child, Category):
                current_item = treeview.insert(parent, "end", text=child.name)
                for child2 in child.children:
                    self.insert_treeview(child2, current_item)
            elif isinstance(child, Article):
                treeview.insert(parent, "end", text=child.name)

    def save_and_exit(self) -> None:
        pass

    def add_article(self) -> None:
        pass

    def show_articles(self) -> None:
        pass

    def update_status(self) -> None:
        pass

    def show_categories(self) -> None:
        pass

    def show_titles(self) -> None:
        pass

    def print_composite(self) -> None:
        pass
