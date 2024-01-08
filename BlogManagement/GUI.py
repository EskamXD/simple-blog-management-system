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


class FunctionConfig:
    def __init__(self, controller_cls, view_cls, tab=None):
        self.controller_cls = controller_cls
        self.view_cls = view_cls
        self.tab = tab


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

        self.function_configs = {
            "Add Article": FunctionConfig(AddArticleController, AddArticleView),
            "Show Categories": FunctionConfig(TreeController, TreeView),
            "Show Photo Gallery": FunctionConfig(
                PhotoGalleryController, PhotoGalleryView
            ),
            "Update Status": FunctionConfig(UpdateStatusController, UpdateStatusView),
        }

        # Load state from JSON
        try:
            self.root.load_composite_recursive("main_state.json")
        except FileNotFoundError:
            pass

    def run(self) -> None:
        self.add_function("Add Article")
        self.add_function("Show Categories")
        self.add_function("Show Photo Gallery")
        self.add_function("Update Status")

        self.window.mainloop()

    def add_function(self, function_name: str) -> None:
        config = self.function_configs.get(function_name)
        if config:
            controller = config.controller_cls(self.root)
            view = config.view_cls(self.root, config.tab, controller)
            controller.set_view(view)
            controller.place()

            # Add observers
            for other_function_name, other_config in self.function_configs.items():
                if other_function_name != function_name:
                    other_controller = other_config.controller_cls(self.root)
                    other_view = other_config.view_cls(
                        self.root, other_config.tab, other_controller
                    )
                    other_controller.set_view(other_view)
                    controller.add_observer(other_view)

            # Add to main window
            view.place()
