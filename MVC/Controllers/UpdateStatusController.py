# import os
# import textwrap
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Composite.Article import Article
from Composite.Category import Category

from MVC.Controllers.Controller import Controller
from MVC.Views.UpdateStatusView import UpdateStatusView

from Strategy.ArticleStatusChanger import ArticleStatusChanger


ARTICLES_PATH = str("data")

class UpdateStatusController(Controller):
    def __init__(self, root: str, view: "UpdateStatusView" = None):
        super().__init__(root, view)

    def set_view(self, view):
        self.view = view

    def place(self): 
        self.view.place()

    def update_article_list(self, category_name: Category) -> None:
        # Clear the article list
        self.view.article_menubutton.menu.delete(0, tk.END)
        self.view.selected_article.set("")
        self.view.article_menubutton.configure(state="readonly")
        
        category_component_dict = {child.name: child for child in self.root.children}

        # Populate the article list
        for article in category_component_dict[category_name].children:
            self.view.article_menubutton.menu.add_command(
                label=article.title,
                command=lambda article=article: (
                    self.view.selected_article.set(article.title),
                    self.update_status_list(article),
                ),
            )

    def update_status_list(self, article: Article) -> None:
        self.view.status_menubutton.menu.delete(0, tk.END)
        self.view.selected_status.set("")
        self.view.status_menubutton.configure(state="readonly")

        current_status = article.status

        for status in set(ArticleStatusChanger.get_status_dict().values()):
            self.view.status_menubutton.menu.add_command(
                label=status,
                command=lambda status=status: self.view.selected_status.set(status),
            )

        # first letter uppercase
        current_status = current_status[0].upper() + current_status[1:]
        self.view.selected_status.set(current_status)


    def save(self):
        # Get the selected category
        category_name = self.view.selected_category.get()
        category_component_dict = {child.name: child for child in self.root.children}
        category = category_component_dict[category_name]

        # Get the selected article
        article_title = self.view.selected_article.get()
        article = {article.title: article for article in category.children}[article_title]

        # Get the selected status
        status = self.view.selected_status.get()
        
        # Change the status
        article.status = status
        self.root.save_composite_recursive("main_state.json")

    def cancel(self):
        self.view.selected_category.set("")
        
        self.view.selected_article.set("")
        self.view.article_menubutton.configure(state="disabled")

        self.view.selected_status.set("")
        self.view.status_menubutton.configure(state="disabled")