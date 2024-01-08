from BlogManagement.BlogManagement import BlogManagement
from Composite.Category import Category
from Composite.Article import Article
from Database import Database



from MVC.Controllers.AddArticleController import AddArticleController
from MVC.Controllers.PhotoGalleryController import PhotoGalleryController
from MVC.Controllers.TreeController import TreeController
from MVC.Controllers.UpdateStatusController import UpdateStatusController

from MVC.Views.AddArticleView import AddArticleView
from MVC.Views.PhotoGalleryView import PhotoGalleryView
from MVC.Views.TreeView import TreeView
from MVC.Views.UpdateStatusView import UpdateStatusView

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
        self.photo_gallery_tab = None
        self.tree_tab = None
        self.update_status_tab = None

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
        menu.add(tree_tab, text="Add new category")
        self.tree_tab = tree_tab

        update_status_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(update_status_tab, text="Update status")
        self.update_status_tab = update_status_tab

        photo_gallery_tab = ttk.Frame(menu, bootstyle="default")
        menu.add(photo_gallery_tab, text="Photo gallery")
        self.photo_gallery_tab = photo_gallery_tab

        self.add_article()
        self.show_categories()
        self.show_photo_gallery()
        self.update_status()

        self.window.mainloop()

    def add_article(self) -> None:
        add_article_controller = AddArticleController(self.root)
        add_article_view = AddArticleView(self.root, self.add_article_tab, add_article_controller)
        add_article_controller.set_view(add_article_view)
        add_article_controller.place()

    def show_categories(self) -> None:
        tree_controller = TreeController(self.root)
        tree_view = TreeView(self.root, self.tree_tab, tree_controller)
        tree_controller.set_view(tree_view)
        tree_controller.place()

    def show_photo_gallery(self) -> None:
        photo_gallery_controller = PhotoGalleryController(self.root)
        photo_gallery_view = PhotoGalleryView(self.root, self.photo_gallery_tab, photo_gallery_controller)
        photo_gallery_controller.set_view(photo_gallery_view)
        photo_gallery_controller.load_images()
        photo_gallery_view.place()

    def update_status(self) -> None:
        update_status_controller = UpdateStatusController(self.root)
        update_status_view = UpdateStatusView(self.root, self.update_status_tab, update_status_controller)
        update_status_controller.set_view(update_status_view)
        update_status_controller.place()
