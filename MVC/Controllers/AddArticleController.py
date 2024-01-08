import datetime
import os
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog
from ttkbootstrap.constants import *

from Composite.Article import Article

from MVC.Controllers.Controller import Controller
from MVC.Views.AddArticleView import AddArticleView

from Strategy.ValidationStrategy import ValidationStrategy
from Strategy.ImageSizeValidator import ImageSizeValidator
from Strategy.ArticleStatusChanger import ArticleStatusChanger

ARTICLES_PATH = str("data")
META_OK = ("meta_ok", "#28a745")
META_LONG = ("meta_long", "#dc3545")
META_DEFAULT = ("meta_default", "#007bff")

class AddArticleController(Controller):
    def __init__(self, root: str, view: "AddArticleView" = None):
        super().__init__(root, view)

        self.filled_fields = {
            "category": False,
            "meta_title": False,
            "meta_description": False,
            "status": True,
            "image": False,
            "thumbnail": False,
        }
        self.temp_image = None

    def set_view(self, view: "AddArticleView"):
        self.view = view

    def place(self):
        self.view.place()

    def validate_meta_entry(
        self, widget: tk.Widget, meta_text: str, validator: ValidationStrategy, widget_name: str
    ) -> None:
        # Get the meta title from the entry widget
        # Validate the meta title using the MetaTitleValidator
        is_valid = validator.validate(meta_text)
        # print(widget, meta_text, is_valid, sep=": ")

        self.filled_fields[widget_name] = True
        # Change the style of the entry based on validation result
        if is_valid == META_OK[0]:
            widget.configure(highlightcolor=META_OK[1])
        elif is_valid == META_LONG[0]:
            widget.configure(highlightcolor=META_LONG[1])
        else:
            widget.configure(highlightcolor=META_DEFAULT[1])
            self.filled_fields[widget_name] = False

    def validate_status(self) -> None:
        validator = ArticleStatusChanger()
        return validator.validate(self.view.get_status())

    def validate_image_size(self, image_path) -> int:
        validator = ImageSizeValidator()
        return validator.validate(image_path)

    def choose_photo(self) -> None:
        if (
            self.view.get_category() == ""
            or self.view.get_category() is None
        ):
            self.handle_invalid_category()
            return

        filepath = filedialog.askopenfile(
            mode="r",
            filetypes=[
                ("Image files", ("*.jpg", "*.jpeg", "*.png")),
                ("all files", "*.*"),
            ],
            initialdir=os.getcwd(),
            title="Select an image",
        )

        buffer = self.validate_image_size(filepath.name)

        if isinstance(buffer, BytesIO):
            try:
                self.load_and_display_image(buffer)
            except Exception as e:
                print("Error loading image:", e)
            finally:
                filepath.close()
        elif buffer == -1:
            filepath.close()
            self.handle_large_image()
        else:
            filepath.close()
            self.handle_default_case()

    def load_and_display_image(self, buffer: BytesIO) -> None:
        image = Image.open(buffer)
        self.temp_image = image
        self.filled_fields["image"] = True

        thumbnail_to_display = image.copy()
        thumbnail_to_display.thumbnail((300, 210), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(thumbnail_to_display)

        self.view.image_label.configure(bootstyle="primary", image=photo)
        self.view.image_label.image = photo  # Keep a reference to avoid garbage collection
        buffer.close()

    def handle_invalid_category(self):
        self.view.image_label.configure(
            bootstyle="inverse-danger", text="Choose category first"
        )

    def handle_large_image(self):
        self.view.image_label.configure(
            bootstyle="inverse-danger", text="Image is too large"
        )

    def handle_default_case(self):
        self.view.image_label.configure(bootstyle="inverse-secondary")

    def handle_thumbnail_toggle(self):
        if self.view.get_thumbnail():
            print("Not selected")
            self.filled_fields["thumbnail"] = False
        else:
            print("Selected")
            self.filled_fields["thumbnail"] = True

    def save(self):
        if (
            self.view.get_category() != ""
            or self.view.get_category() is not None
        ):
            self.filled_fields["category"] = True

        # Check if all fields are filled
        if (
            self.filled_fields["category"] == False
            or self.filled_fields["meta_title"] == False
            or self.filled_fields["meta_description"] == False
            or self.filled_fields["image"] == False
        ):
            MsgBox = tk.messagebox.showwarning(
                "Warning", "Please fill all fields", icon="warning"
            )
            return

        status = self.validate_status()
        # Get category component
        category_name = self.view.get_category()
        # Save article to the system
        # Stwórz obiekt artykułu
        article_component = Article(
            self.view.get_meta_title().replace('?', ''),
            "",
            f"{ARTICLES_PATH}/{category_name}/images/{self.view.get_meta_title().replace('?','')}.webp",
            status,
            self.view.get_meta_description(),
            datetime.datetime.now().strftime("%Y-%m-%d"),
            category_name,
        )

        try: 
            category_component = {child.name: child for child in self.root.children}[category_name]
            print(category_component)
        except KeyError:
            category_component = None
        
        if category_component:
            category_component.add(article_component)

            # Zapisz obraz do folderu artykułu
            self.temp_image.save(
                f"{ARTICLES_PATH}/{category_name}/images/{article_component.title.replace('?', '')}.webp"
            )
            if self.filled_fields["thumbnail"]:
                # Zapisz miniaturkę do folderu artykułu
                thumbnail = self.temp_image.copy()
                thumbnail.thumbnail((300, 160), Image.ANTIALIAS)
                thumbnail.save(
                    f"{ARTICLES_PATH}/{category_name}/images/{article_component.title.replace('?', '')}_thumbnail.webp"
                )
            # Zapisz stan do DOCX i JSON
            article_component.save(category_component)
            self.root.save_composite_recursive("main_state.json")

        MsgBox = tk.messagebox.showinfo(
            "Information", "Article saved successfully", icon="info"
        )
        self.cancel()

    def cancel(self):
        self.view.set_category("")
        self.view.set_meta_title("")
        self.view.set_meta_description("")
        self.view.set_status("Draft")
        self.view.set_thumbnail(False)
        self.view.image_label.configure(bootstyle="inverse-secondary", image=None, text="Image preview")
        self.view.image_label.image = None
        self.temp_image = None
