from BlogManagement.BlogManagement import BlogManagement

from Composite.Category import Category

from Database import Database

from MVC.Controllers.AddArticleController import AddArticleController
from MVC.Controllers.PhotoGalleryController import PhotoGalleryController
from MVC.Controllers.TreeController import TreeController
from MVC.Controllers.UpdateStatusController import UpdateStatusController

from MVC.Views.AddArticleView import AddArticleView
from MVC.Views.PhotoGalleryView import PhotoGalleryView
from MVC.Views.TreeView import TreeView
from MVC.Views.UpdateStatusView import UpdateStatusView

from UpdateObserver.Observer import Observer

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


        self.add_article_controller = AddArticleController(self.root)
        self.add_article_view = AddArticleView(self.root, self.add_article_tab, self.add_article_controller)

        self.photo_gallery_controller = PhotoGalleryController(self.root)
        self.photo_gallery_view = PhotoGalleryView(self.root, self.photo_gallery_tab, self.photo_gallery_controller)

        self.tree_controller = TreeController(self.root)
        self.tree_view = TreeView(self.root, self.tree_tab, self.tree_controller)

        self.update_status_controller = UpdateStatusController(self.root)
        self.update_status_view = UpdateStatusView(self.root, self.update_status_tab, self.update_status_controller)

        # Load state from JSON
        try:
            self.root.load_composite_recursive("main_state.json")
        except FileNotFoundError:
            pass

    def run(self) -> None:
        self.add_article()
        self.show_categories()
        self.show_photo_gallery()
        self.update_status()

        self.window.mainloop()

    def add_article(self) -> None:
        self.add_article_controller.set_view(self.add_article_view)
        self.add_article_controller.place()

        self.add_article_controller.add_observer(self.tree_view)
        self.add_article_controller.add_observer(self.photo_gallery_view)
        self.add_article_controller.add_observer(self.update_status_view)

    def show_categories(self) -> None:
        self.tree_controller.set_view(self.tree_view)
        self.tree_controller.place()

        self.tree_controller.add_observer(self.add_article_view)

    def show_photo_gallery(self) -> None:
        self.photo_gallery_controller.set_view(self.photo_gallery_view)
        self.photo_gallery_controller.load_images()
        self.photo_gallery_view.place()

    def update_status(self) -> None:
        self.update_status_controller.set_view(self.update_status_view)
        self.update_status_controller.place()
        
        self.update_status_controller.add_observer(self.update_status_view)
