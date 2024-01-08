import os
import textwrap
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Composite.Article import Article
from Composite.Category import Category

from MVC.Controllers.Controller import Controller
from MVC.Views.TreeView import TreeView

from UpdateObserver.Observer import Observer
from UpdateObserver.Subject import Subject

ARTICLES_PATH = str("data")

class TreeController(Controller, Subject):
    def __init__(self, root: str, view: "TreeView" = None):
        super().__init__(root, view)
        self._observers = []

    def add_observer(self, observer: Observer) -> None:
        print("TreeController: Attached an observer.")
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        print("TreeController: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def set_view(self, view):
        self.view = view

    def place(self): 
        self.view.place()

    def wrap(self, string: str, lenght: int=8) -> str:
        return '\n'.join(textwrap.wrap(string, lenght))

    def insert_treeview(self, treeview: ttk.Treeview) -> ttk.Treeview:
        # Define columns
        treeview["columns"] = ("Article", "Create Date")

        # Configure column properties
        treeview.column("#0", width=5, anchor=tk.W)  # The first column (tree branches)
        treeview.column("Article", width=185, anchor=tk.W)
        treeview.column("Create Date", width=105, anchor=tk.W)

        # Set column headings
        treeview.heading("#0", text="", anchor=tk.W)
        treeview.heading("Article", text="| Articles", anchor=tk.W)
        treeview.heading("Create Date", text="| Create Date", anchor=tk.W)

        # Insert data into treeview
        for category in self.root.children:
            if isinstance(category, Category):
                category_item = treeview.insert("", tk.END, values=(category.name, ""))
            for article in category.children:
                if isinstance(article, Article):
                    article_item = treeview.insert(category_item, tk.END, values=(f"|-{article.title}", article.creation_date))

        return treeview

    def save(self):
        category_name = self.view.category_create.get()
        existing_categories = self.view.existing_category_listbox.get(0, tk.END)

        if category_name in existing_categories:
            MsgBox = tk.messagebox.showinfo(
                "Category already exists", "Category already exists"
            )
            self.view.category_create.delete(0, tk.END)
            return

        if category_name == "":
            MsgBox = tk.messagebox.showinfo(
                "Category name can't be null", "Category name can't be null"
            )
            return
        
        category = Category(category_name, self.root.name)
        self.root.add(category)
        self.view.existing_category_listbox.insert(tk.END, category.name)
        self.view.category_create.delete(0, tk.END)
        self.view.treeview.delete(*self.view.treeview.get_children())
        self.view.treeview = self.insert_treeview(self.view.treeview)
        self.root.save_composite_recursive("main_state.json")
        try:
            os.chdir(ARTICLES_PATH)
            os.mkdir(category_name)
        except FileExistsError:
            pass

        try:
            os.chdir(f"{ARTICLES_PATH}/{category_name}")
            os.mkdir("images")
        except FileNotFoundError:
            os.chdir(f"{category_name}")
            os.mkdir("images")
        except FileExistsError:
            pass

        self.cancel()
        self.notify_observers()

    def cancel(self):
        self.view.category_create.delete(0, tk.END)

