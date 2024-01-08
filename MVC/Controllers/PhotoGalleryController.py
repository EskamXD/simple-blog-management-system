import os
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from screeninfo import get_monitors
from ttkbootstrap.constants import *

from Composite.Category import Category

from MVC.Controllers.Controller import Controller
from MVC.Views.PhotoGalleryView import PhotoGalleryView

from UpdateObserver.Observer import Observer
from UpdateObserver.Subject import Subject

ARTICLES_PATH = str("data")
IDEAL_RATIO = 1.0
IDEAL_WIDTH = 210
IDEAL_HEIGHT = 210

class PhotoGalleryController(Controller, Subject):
    def __init__(self, root: str, view: "PhotoGalleryView" = None):
        super().__init__(root, view)
        self.photo_paths = [] 
        self.get_photo_paths()
        self._observers = []

    def add_observer(self, observer: Observer) -> None:
        print("PhotoGalleryController: Attached an observer.")
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        print("PhotoGalleryController: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def set_view(self, view):
        self.view = view

    def place(self): 
        self.view.place()

    def load_images(self):
        column_count = 3
        row_count = (len(self.photo_paths) + column_count - 1) // column_count

        for i, photo_path in enumerate(self.photo_paths):
            img = Image.open(photo_path)
            split_path = photo_path.split("\\")
            image_name = split_path[-1]
            image_category = split_path[-3]

            # Resize the image while maintaining the aspect ratio
            width, height = img.size
            ratio = width / height

            if ratio > IDEAL_RATIO:
                img = img.resize((int(IDEAL_HEIGHT * ratio), IDEAL_HEIGHT), Image.ANTIALIAS)
            else:
                img = img.resize((IDEAL_WIDTH, int(IDEAL_WIDTH / ratio)), Image.ANTIALIAS)

            # Crop the image to the desired dimensions
            width, height = img.size
            if ratio > IDEAL_RATIO:
                left = (width - IDEAL_WIDTH) / 2
                top = 0
                right = (width + IDEAL_WIDTH) / 2
                bottom = height
            else:
                left = 0
                top = (height - IDEAL_HEIGHT) / 2
                right = width
                bottom = (height + IDEAL_HEIGHT) / 2

            img = img.crop((left, top, right, bottom))

            # Create PhotoImage and display the image
            photo = ImageTk.PhotoImage(img)
            row, column = divmod(i, column_count)
            label = ttk.Label(self.view.frame, image=photo)
            label.grid(row=row, column=column, padx=5, pady=5)

            # Keep a reference to avoid garbage collection
            label.photo = photo

            # Bind a callback to open a new window with the original photo when clicked
            label.bind("<Button-1>", lambda event, path=photo_path: self.open_original_window(path))
        
    def get_photo_paths(self):
        photo_list = []
        for child in self.root.children:
            if isinstance(child, Category):
                category_path = os.path.join(ARTICLES_PATH, child.name, "images")
                if os.path.exists(category_path) and os.path.isdir(category_path):
                    photo_files = [f for f in os.listdir(category_path) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
                    photo_list.extend([os.path.join(category_path, file) for file in photo_files])
                    print(photo_list)
                    
        self.photo_paths = photo_list
    
    def open_original_window(self, photo_path):
        full_path = os.getcwd() + "\\" + photo_path
        original_img = Image.open(full_path)
        split_path = photo_path.split("\\")
        name = split_path[-1]
        category = split_path[-3]

        for m in get_monitors():
            if m.is_primary:
                screen_width = m.width - m.width // 10
                screen_height = m.height - m.height // 10
                break
        else:
            screen_width = 1920
            screen_height = 1080

        # Resize the image if it's larger than the screen
        if original_img.width > screen_width or original_img.height > screen_height:
            original_img.thumbnail((screen_width, screen_height), Image.ANTIALIAS)

        # Create a new window
        original_window = tk.Toplevel(self.view.tab)
        original_window.title(name)

        # Create PhotoImage for the original image
        original_photo = ImageTk.PhotoImage(original_img)

        # Display the original image in a label
        original_label = ttk.Label(original_window, image=original_photo)
        original_label.pack()

        # Create a Canvas for the bar
        canvas = tk.Canvas(original_window, height=40, bg="white")
        canvas.pack(fill="x")

        # width, height = original_img.size

        # Display name and category in the bar
        # canvas.create_text(10, 20, anchor="w", fill="#ffffff", text=f"Name: {name}", font=("Arial", 10))
        canvas.create_text(10, 20, anchor="w", fill="#ffffff", text=f"Category: {category}", font=("Arial", 12))

        # Keep a reference to avoid garbage collection
        original_label.photo = original_photo

