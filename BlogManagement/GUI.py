from BlogManagement.BlogManagement import BlogManagement
from Composite.Category import Category
from Composite.Article import Article
from Database import Database



from MVC.Views.AddArticleView import AddArticleView
from MVC.Views.TreeView import TreeView
from MVC.Views.PhotoGalleryView import PhotoGalleryView

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
        self.window.geometry("700x610")
        self.window.configure(bg="#23232B")
        self.window.resizable(False, False)

        self.selected_category = tk.StringVar()

        self.add_article_tab = None
        self.tree_tab = None
        self.photo_gallery_tab = None

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
        self.add_article_tab = add_article_tab

        tree_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(tree_tab, text="Category tree")
        self.tree_tab = tree_tab

        photo_gallery_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(photo_gallery_tab, text="Photo gallery")
        self.photo_gallery_tab = photo_gallery_tab

        self.add_article()
        self.show_articles()

        self.window.mainloop()

    def save_and_exit(self) -> None:
        pass

    def add_article(self) -> None:
        add_article = AddArticleView(self.root, self.add_article_tab)
        add_article.place()

    def show_articles(self) -> None:
        tree = TreeView(self.root, self.tree_tab)
        tree.place()

    def update_status(self) -> None:
        pass

    def show_categories(self) -> None:
        pass

    def show_titles(self) -> None:
        pass

    def print_composite(self) -> None:
        pass
