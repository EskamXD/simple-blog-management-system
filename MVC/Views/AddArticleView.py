import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from MVC.Views.View import View

from Strategy.ValidationStrategy import ValidationStrategy
from Strategy.MetaTitleValidator import MetaTitleValidator
from Strategy.MetaDescriptionValidator import MetaDescriptionValidator
from Strategy.ImageSizeValidator import ImageSizeValidator
from Strategy.ArticleStatusChanger import ArticleStatusChanger

class AddArticleView(View):
    def __init__(self, root, tab) -> None:
        super().__init__(root, tab)
        self.selected_category = tk.StringVar()
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
        self.category_label = ttk.Label(self.canvas, bootstyle="primary", text="Article category")

        # Category combobox
        self.category_menubutton = ttk.Menubutton(
            self.canvas,
            bootstyle="outline-primary",
            state="readonly",
            textvariable=self.selected_category,  # Link the variable to the Menubutton
        )
        self.category_menubutton.menu = tk.Menu(self.category_menubutton, tearoff=0)


        # Meta title label
        self.meta_title_label = ttk.Label(
            self.canvas, bootstyle="primary", text="Article meta title"
        )

        # Meta title entry
        # self.meta_title_variable = ttk.StringVar()
        # self.meta_title_entry = ttk.Entry(self.canvas, bootstyle="primary", textvariable=self.meta_title_variable , width=50)
        self.meta_title_entry = ttk.Text(self.canvas, relief="solid", width=50, wrap="word")

        # Meta description labelframe
        self.meta_description_label = ttk.Label(
            self.canvas,
            bootstyle="primary",
            text="Article meta description",
        )

        # Meta description entry
        # self.meta_desription_variable = ttk.StringVar()
        self.meta_description_entry = ttk.Text(
            self.canvas, relief="solid", width=50, wrap="word"
        )

        # Status label
        self.status_label = ttk.Label(self.canvas, bootstyle="primary", text="Article status")

        # Status combobox
        self.status_menubutton = ttk.Menubutton(
            self.canvas,
            bootstyle="outline-primary",
            state="readonly",
            textvariable=self.selected_status,  # Link the variable to the Menubutton
        )
        self.status_menubutton.menu = tk.Menu(self.status_menubutton, tearoff=0)


        # Line
        self.canvas.create_line(
            30.0,
            290.0,
            670.0,
            290.0,
            fill="#FFFFFF",
            width=1,
        )

        # Image rectangle
        self.canvas.create_rectangle(
            310.0,
            310.0,
            670.0,
            450.0,
            fill="#D9D9D9",
            outline="",
        )

        # Image button
        self.image_button = ttk.Button(
            self.canvas, bootstyle="outline-primary", text="Choose image"
        )

        # Thumbnail toggle
        self.thumbnail_toggle = ttk.Checkbutton(
            self.canvas, bootstyle="round-toggle", text="Thumbnail"
        )

        # Image frame
        self.image_frame = ttk.Frame(self.canvas, bootstyle="primary")
        self.temp_text = ttk.Label(self.image_frame, bootstyle="info", justify="center", text="Image preview")

        # Save button
        self.save_button = ttk.Button(self.canvas, bootstyle="outline-success", text="Save")

        # Cancel button
        self.cancel_button = ttk.Button(self.canvas, bootstyle="outline-danger", text="Cancel")

    def place(self):
        self.canvas.place(x=0, y=0)
        self.frame.place(x=0, y=120.0, width=700.0, height=450.0)

        self.category_label.place(x=30.0, y=150.0, width=300.0, height=20.0)
        self.category_menubutton.place(x=30.0, y=170.0, width=300.0, height=40.0)
        self.category_menubutton["menu"] = self.category_menubutton.menu

        for child in self.root.children:
            self.category_menubutton.menu.add_radiobutton(
                label=child.name,
                value=child.name,
                command=lambda name=child.name: self.selected_category.set(name),
            )

        self.meta_title_label.place(x=30.0, y=210.0, width=300.0, height=20.0)
        self.meta_title_entry.place(x=30.0, y=230.0, width=300.0, height=40.0)
        # self.meta_title_variable.trace_add("write", lambda *args: self.validate_meta_entry(self.meta_title_entry, self.meta_title_entry.get(), MetaTitleValidator()))
        self.meta_title_entry.bind("<KeyRelease>", lambda *args: self.validate_meta_entry(self.meta_title_entry, self.meta_title_entry.get("1.0", "end-1c"), MetaTitleValidator()))

        self.meta_description_label.place(x=370.0, y=150.0, width=300.0, height=20.0)
        self.meta_description_entry.place(x=370.0, y=170.0, width=300.0, height=100.0)
        self.meta_description_entry.bind("<KeyRelease>", lambda *args: self.validate_meta_entry(self.meta_description_entry, self.meta_description_entry.get("1.0", "end-1c"), MetaDescriptionValidator()))

        self.status_label.place(x=30.0, y=270.0, width=300.0, height=20.0)
        self.status_menubutton.place(x=30.0, y=290.0, width=300.0, height=40.0)
        self.status_menubutton["menu"] = self.status_menubutton.menu

        for status in set(ArticleStatusChanger.get_status_dict().values()):
            self.status_menubutton.menu.add_radiobutton(
                label=status,
                value=status,
                command=lambda name=status: self.selected_status.set(name),
            )
        self.selected_status.set("Draft")

        self.image_button.place(x=30.0, y=350.0, width=150.0, height=40.0)
        self.image_button.bind("<Button-1>", lambda *args: self.validate_image_size(ImageSizeValidator()))
        self.thumbnail_toggle.place(x=30.0, y=410.0, width=150.0, height=20.0)
        self.image_frame.place(x=370.0, y=350.0, width=300.0, height=200.0)

        self.save_button.place(x=30.0, y=460.0, width=150.0, height=40.0)
        self.cancel_button.place(x=30.0, y=520.0, width=150.0, height=40.0)


    def validate_meta_entry(self, widget: tk.Widget, meta_text: str, validator: ValidationStrategy) -> None:
        # Get the meta title from the entry widget
        # Validate the meta title using the MetaTitleValidator
        is_valid = validator.validate(meta_text)
        # print(widget, meta_text, is_valid, sep=": ")

        # Change the style of the entry based on validation result
        if is_valid == 1:
            # widget.configure(bootstyle="success")
            widget.configure(highlightcolor="#28a745")
        elif is_valid == -1:
            # widget.configure(bootstyle="danger")
            widget.configure(highlightcolor="#dc3545")
        else:
            # widget.configure(bootstyle="primary")
            widget.configure(highlightcolor="#007bff")

    def validate_image_size(self, validator: ValidationStrategy) -> None:
        # Validate the image size using the ImageSizeValidator
        is_valid = validator.validate()
        # print(is_valid, sep=": ")

        # Change the style of the entry based on validation result
        if is_valid == 1:
            self,
        elif is_valid == -1:
            self.image_button.configure(bootstyle="danger")
        else:
            self.image_button.configure(bootstyle="outline-primary")

