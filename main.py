import tkinter as tk
from tkinter import filedialog, font, messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
import csv
from os import listdir, rmdir, path, mkdir
import os
import io


class Tooltip:
    def __init__(self, widget, text, font=("Roboto", 9)):
        self.widget = widget
        self.text = text
        self.font = font
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25  # Dostosuj położenie tooltipu
        y += self.widget.winfo_rooty() + 25  # Dostosuj położenie tooltipu
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text,
                         background="lightyellow", relief="solid", borderwidth=1, font=self.font)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class App:
    def __init__(self, root, images_count):
        self.root = root
        self.root.title("Zarządzanie blogiem")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Roboto",
                                   size=14)

        self.images_count = images_count

        self.create_widgets()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True)

        self.create_tab_blog()
        # self.create_tab_categories()
        # self.create_tab_settings()

    def create_tab_blog(self):
        # Notebook tab about blog title, metadata, photo
        notebook_tab_blog = ttk.Frame(self.notebook)
        notebook_tab_blog.pack(fill="both", expand=True)
        self.notebook.add(notebook_tab_blog, text="Blog")

        """begin of lebalframes for blog tab"""
        # label frames
        metadata_labelframe = ttk.LabelFrame(notebook_tab_blog, text="Metadane",
                                             bootstyle="primary")
        metadata_labelframe.place(relwidth=1, relheight=0.25, relx=0, rely=0)

        photo_labelframe = ttk.LabelFrame(notebook_tab_blog, text="Zdjęcie",
                                          bootstyle="primary")
        photo_labelframe.place(relwidth=1, relheight=0.65, relx=0, rely=0.25)

        button_labelframe = ttk.LabelFrame(notebook_tab_blog, text="",
                                           bootstyle="primary")
        button_labelframe.place(relwidth=1, relheight=0.1, relx=0, rely=0.9)
        """end of lebalframes for blog tab"""

        # main frames in labelframe "Metadane"
        left_frame_metadata = ttk.Frame(metadata_labelframe)
        left_frame_metadata.place(relwidth=0.8, relheight=1, relx=0, rely=0)

        right_frame_metadata = ttk.Frame(metadata_labelframe)
        right_frame_metadata.place(relwidth=0.2, relheight=1, relx=0.8, rely=0)

        # main frames in labelframe "Zdjęcie"
        left_frame_photos = ttk.Frame(photo_labelframe)
        left_frame_photos.place(relwidth=0.8, relheight=1, relx=0, rely=0)

        right_frame_photos = ttk.Frame(photo_labelframe)
        right_frame_photos.place(relwidth=0.2, relheight=1, relx=0.8, rely=0)

        """begin of widgets in labelframe "Metadane" """
        # frames for labelframe "Metadane"
        category_frame = ttk.Frame(left_frame_metadata)
        category_frame.place(relwidth=1, relheight=0.33, relx=0, rely=0)

        keyword_frame = ttk.Frame(left_frame_metadata)
        keyword_frame.place(relwidth=1, relheight=0.33, relx=0, rely=0.33)

        title_frame = ttk.Frame(left_frame_metadata)
        title_frame.place(relwidth=1, relheight=0.33, relx=0, rely=0.66)

        # widgets for category_frame
        category_label = ttk.Label(category_frame, text="Kategoria")
        category_label.place(relwidth=0.25, relx=0.05, rely=0)

        self.category_combobox = ttk.Combobox(
            category_frame, state="readonly")
        self.category_combobox.place(
            relwidth=0.65, relx=0.3, rely=0)

        root_dir = "categories"
        folders = [category for category in listdir(
            root_dir) if path.isdir(path.join(root_dir, category))]

        self.category_combobox["values"] = folders

        # widgets for keyword_frame
        keyword_label = ttk.Label(keyword_frame, text="Słowo kluczowe")
        keyword_label.place(relwidth=0.25, relx=0.05, rely=0)

        self.keyword_entry = ttk.Entry(keyword_frame)
        self.keyword_entry.place(
            relwidth=0.65, relx=0.3, rely=0)

        # widgets for title_frame
        title_label = ttk.Label(title_frame, text="Tytuł")
        title_label.place(relwidth=0.25, relx=0.05, rely=0)

        self.title_entry = ttk.Entry(title_frame)
        self.title_entry.place(
            relwidth=0.65, relx=0.3, rely=0)
        self.title_entry.bind("<KeyRelease>", self.calculate_width)

        # widgets in right_frame_metadata
        self.word_counter_label = ttk.Label(
            right_frame_metadata, text="0 / 60 (0px / 600px)", font=("Roboto", 9), justify="right")
        self.word_counter_label.place(
            relwidth=0.95, relx=0, rely=0.63)

        self.progress_bar = ttk.Progressbar(
            right_frame_metadata, mode="determinate", maximum=60)
        self.progress_bar.place(relwidth=0.95,
                                relx=0., rely=0.77)
        """end of widgets in labelframe "Metadane" """

        """begin of widgets in labelframe "Zdjęcie" """

        # splitting left_frame_photos into 2 frames
        top_left_frame_photos = ttk.Frame(left_frame_photos)
        top_left_frame_photos.place(relwidth=1, relheight=0.2, relx=0, rely=0)

        bottom_left_frame_photos = ttk.Frame(left_frame_photos)
        bottom_left_frame_photos.place(
            relwidth=1, relheight=0.8, relx=0, rely=0.2)

        # widgets in left_frame_photos
        photo_label = ttk.Label(top_left_frame_photos, text="Zdjęcie")
        photo_label.place(relwidth=0.25, relx=0.05, rely=0.1)

        self.photo_button = ttk.Button(
            top_left_frame_photos, text="Wybierz plik", command=self.load_image)
        self.photo_button.place(
            relwidth=0.2, relx=0.3, rely=0)

        thumbnail_frame = ttk.Frame(top_left_frame_photos)
        thumbnail_frame.place(relwidth=0.2, relheight=1, relx=0.55, rely=0.1)

        self.thumbnail_label = ttk.Label(
            thumbnail_frame, text="Miniaturka", bootstyle="secondary")
        self.thumbnail_label.place(relwidth=0.8, relx=0, rely=0)

        self.thumbnail_checkbutton_variable = tk.IntVar()
        self.thumbnail_checkbutton = ttk.Checkbutton(
            thumbnail_frame, variable=self.thumbnail_checkbutton_variable, bootstyle="disabled-round-toggle", command=self.thumbnail_checkbutton_action, state="disabled")
        self.thumbnail_checkbutton.place(
            relwidth=0.2, relx=0.8, rely=0.05)

        self.thb_width_entry = ttk.Entry(
            top_left_frame_photos, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"), bootstyle="diabled", state=tk.DISABLED)
        self.thb_width_entry.place(relwidth=0.07, relx=0.8, rely=0.1)

        self.thb_height_entry = ttk.Entry(
            top_left_frame_photos, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"), bootstyle="diabled", state=tk.DISABLED)
        self.thb_height_entry.place(relwidth=0.07, relx=0.88, rely=0.1)

        self.loaded_photo_label = ttk.Label(bottom_left_frame_photos)
        self.loaded_photo_label.place(relwidth=1, relheight=1, relx=0, rely=0)

        # splitting right_frame_photos into 2 frames
        top_right_frame_photos = ttk.Frame(right_frame_photos)
        top_right_frame_photos.place(relwidth=1, relheight=0.2, relx=0, rely=0)

        bottom_right_frame_photos = ttk.Frame(right_frame_photos)
        bottom_right_frame_photos.place(
            relwidth=1, relheight=0.8, relx=0, rely=0.2)

        # widgets in right_frame_photos
        self.label_jpeg = ttk.Label(top_right_frame_photos,
                                    text="JPEG", font=("Roboto", 9), bootstyle="secondary")
        self.label_jpeg.place(relwidth=0.25, relx=0.05, rely=0.1)

        self.toggle_jpeg_webp_checkbutton = ttk.Checkbutton(
            top_right_frame_photos, bootstyle="disabled-round-toggle", command=self.toggle_photo_format, state="disabled")
        self.toggle_jpeg_webp_checkbutton.place(
            relwidth=0.2, relx=0.3, rely=0.1)

        self.label_webp = ttk.Label(top_right_frame_photos, text="WEBP", font=(
            "Roboto", 9), bootstyle="secondary")
        self.label_webp.place(relwidth=0.25, relx=0.5, rely=0.1)

        # 2 label frames for pohoto specs
        self.oryginal_photo_specs_labelframe = ttk.LabelFrame(
            bottom_right_frame_photos, bootstyle="secondary", text="Oryginalne")
        self.oryginal_photo_specs_labelframe.place(
            relwidth=0.9, relheight=0.35, relx=0, rely=0)

        self.new_photo_specs_labelframe = ttk.LabelFrame(
            bottom_right_frame_photos, bootstyle="secondary", text="Nowe")
        self.new_photo_specs_labelframe.place(
            relwidth=0.9, relheight=0.35, relx=0, rely=0.35)

        self.thumbnail_photo_specs_labelframe = ttk.LabelFrame(
            bottom_right_frame_photos, bootstyle="secondary", text="Miniatura")
        self.thumbnail_photo_specs_labelframe.place(
            relwidth=0.9, relheight=0.25, relx=0, rely=0.7)

    ###############################################################
    # Buttons events
    def load_image(self):
        try:
            self.filename = filedialog.askopenfilename(title="Wybierz zdjęcie", filetypes=(
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("all files", "*.*")))
            if not self.filename:
                raise Exception("Nie wybrano zdjęcia")
        except Exception as e:
            print("Błąd load", e)
        else:
            self.image = Image.open(self.filename)

            format = self.new_image_format()
            thumbnail = False

            try:
                original_photo = self.get_original_photo(self.image.copy())
                new_photo = self.get_new_photo(self.image.copy(), format)
                if self.thumbnail_checkbutton_variable.get() == 1:
                    thumbnail_photo = self.get_thumbnail_photo(
                        self.image.copy(), format, new_photo)
                    thumbnail = True

                if not original_photo or not new_photo:
                    raise Exception("Nie udało się załadować zdjęcia")
            except Exception as e:
                messagebox.showerror("Błąd load", e)
            else:
                self.enable_photo_options()
                display_photo_section = self.get_display_photo_section(self.image.copy(
                ), original_photo, new_photo, thumbnail_photo if thumbnail else False)

    ###############################################################
    # Checkbutton events
    def thumbnail_checkbutton_action(self):
        if self.thumbnail_checkbutton_variable.get() == 1:
            state = tk.NORMAL
            style = "primary"
        else:
            state = tk.DISABLED
            style = "secondary"

        self.thb_width_entry.config(state=state, bootstyle=style)
        self.thb_height_entry.config(state=state, bootstyle=style)
        self.thumbnail_photo_specs_labelframe.config(bootstyle=style)
        # self.thumbnail_photo_specs_labelframe.

    def toggle_photo_format(self):
        if self.toggle_jpeg_webp_checkbutton.instate(['selected']):
            self.label_webp.config(bootstyle="default")
            self.label_jpeg.config(bootstyle="secondary")
        else:
            self.label_webp.config(bootstyle="secondary")
            self.label_jpeg.config(bootstyle="default")

        self.refresh_photo_specs()

    def new_image_format(self):
        if self.toggle_jpeg_webp_checkbutton.instate(['selected']):
            return "webp"
        else:
            return "jpeg"

    ###############################################################
    # Entry events
    def validate_number(self, value):
        if value.isdigit() or value == "":
            return True
        else:
            return False

    def calculate_width(self, event):
        title = self.title_entry.get()

        font = ImageFont.truetype("arialbd.ttf", 20, encoding="utf-8")
        image = Image.new("RGB", (1, 1), "white")
        draw = ImageDraw.Draw(image)

        width_pixels = int(draw.textlength(title, font=font))
        self.word_counter_label.config(
            text=f"{len(title)} / 60 ({width_pixels}px / 600px)")

        num_characters = len(title)
        color = self.calculate_color(num_characters, width_pixels)

        self.progress_bar["value"] = min(len(title), 60)
        self.progress_bar.config(bootstyle=color)

    def calculate_color(self, num_characters, width_pixels):
        if num_characters <= 15 and width_pixels <= 600:
            return "danger"
        elif num_characters <= 25 and width_pixels <= 600:
            return "warning"
        elif num_characters <= 35 and width_pixels <= 600:
            return "info"
        elif num_characters <= 60 and width_pixels <= 600:
            return "success"
        elif num_characters > 60 or width_pixels > 600:
            return "danger"
        else:
            return "danger"

    ###############################################################
    # Photo functions
    def get_original_photo(self, image):
        image_name = os.path.basename(self.filename)
        image_width, image_height = image.size
        image_size_bytes = os.path.getsize(self.filename)
        image_size_bytes = self.bytes_to_str(image_size_bytes)

        return {"image_name": image_name, "image_width": image_width, "image_height": image_height, "image_size_bytes": image_size_bytes}

    def get_new_photo(self, image, format):
        try:
            current_category = self.category_combobox.get()
            image_width, image_height = image.size

            if not current_category:
                raise Exception("Nie wybrano kategorii")

            if format == "jpeg" and image.mode != "RGB":
                if not messagebox.askokcancel("Zmiana formatu zdjęcia", "Zdjęcie nie jest w formacie RGB. Czy chcesz kontynuować?"):
                    raise Exception("Operacja przerwana")
                else:
                    image = image.convert("RGB")

            new_image_name = f"{str(current_category[0]).upper()}_{self.images_count[current_category] + 1}.{'webp' if format else 'jpg'}"
            if image_width < 1200:
                new_image_width = image_width
                new_image_height = image_height
            else:
                new_image_width = 1200
                new_image_height = int(image_height * (1200 / image_height))

            temp_image = io.BytesIO()
            image.resize((new_image_width, new_image_height)
                         ).save(temp_image, format, quality=80)
            new_image_size_bytes = temp_image.tell()
            new_image_size_bytes = self.bytes_to_str(new_image_size_bytes)
            temp_image.close()

        except Exception as e:
            messagebox.showerror("Błąd new", e)
            return False
        else:
            return {"new_image_name": new_image_name, "new_image_width": new_image_width, "new_image_height": new_image_height, "new_image_size_bytes": new_image_size_bytes}

    def get_thumbnail_photo(self, image, format, new_image):
        thumbnail_image_name = new_image["new_image_name"].split(
            ".")[0] + "_thumbnail." + format

        if format == "jpeg" and image.mode != "RGB":
            image = image.convert("RGB")

        try:
            new_image_width = new_image["new_image_width"]
            new_image_height = new_image["new_image_height"]
            thb_width = int(self.thb_width_entry.get())
            thb_height = int(self.thb_height_entry.get())

            if thb_width > new_image_width or thb_height > new_image_height:
                raise Exception(
                    "Miniatura nie może być większa niż zdjęcie")

            if thb_width == 0 or thb_height == 0:
                raise Exception("Nie podano rozmiaru miniatury")

            if thb_width > thb_height:
                thb_height = int(thb_width * (thb_height / thb_width))
            elif thb_width < thb_height:
                thb_width = int(thb_height * (thb_width / thb_height))

            aspect_ratio = image.width / image.height
            if aspect_ratio > thb_width / thb_height:
                new_width = thb_width
                new_height = int(thb_width / aspect_ratio)
            else:
                new_width = int(thb_height * aspect_ratio)
                new_height = thb_height

            image = image.resize(
                (new_width, new_height))

            left = (new_width - thb_width) / 2
            top = (new_height - thb_height) / 2
            right = (new_width + thb_width) / 2
            bottom = (new_height + thb_height) / 2
            image = image.crop(
                (left, top, right, bottom))

            temp_image = io.BytesIO()
            image.save(temp_image, format, quality=80)
            thumbnail_image_size_bytes = temp_image.tell()
            thumbnail_image_size_bytes = self.bytes_to_str(
                thumbnail_image_size_bytes)
            temp_image.close()

        except Exception as e:
            messagebox.showerror("Błąd thumbnail", e)
            return False
        else:
            return {"thumbnail_image_name": thumbnail_image_name, "thumbnail_image_width": thb_width, "thumbnail_image_height": thb_height, "thumbnail_image_size_bytes": thumbnail_image_size_bytes}

    def get_display_photo_section(self, image, original_photo, new_photo, thumbnail_photo):
        width = self.loaded_photo_label.winfo_width()
        height = self.loaded_photo_label.winfo_height()
        image.thumbnail((width-width*0.05, height-height*0.05))
        photo = ImageTk.PhotoImage(image)

        self.loaded_photo_label.config(image=photo, anchor="center")
        self.loaded_photo_label.image = photo

        self.oryginal_photo_specs_labelframe.config(bootstyle="primary")
        self.new_photo_specs_labelframe.config(bootstyle="primary")

        ##########################################
        # Frames for oryginal photo specs
        frame_oryginal_name = ttk.Frame(
            self.oryginal_photo_specs_labelframe)
        frame_oryginal_name.place(
            relwidth=1, relheight=0.33, relx=0, rely=0)

        frame_oryginal_resolution = ttk.Frame(
            self.oryginal_photo_specs_labelframe)
        frame_oryginal_resolution.place(
            relwidth=1, relheight=0.33, relx=0, rely=0.33)

        frame_oryginal_size = ttk.Frame(
            self.oryginal_photo_specs_labelframe)
        frame_oryginal_size.place(
            relwidth=1, relheight=0.33, relx=0, rely=0.66)

        ##########################################
        # Frames for new photo specs
        frame_new_name = ttk.Frame(self.new_photo_specs_labelframe)
        frame_new_name.place(relwidth=1, relheight=0.33, relx=0, rely=0)

        frame_new_resolution = ttk.Frame(self.new_photo_specs_labelframe)
        frame_new_resolution.place(
            relwidth=1, relheight=0.33, relx=0, rely=0.33)

        frame_new_size = ttk.Frame(self.new_photo_specs_labelframe)
        frame_new_size.place(relwidth=1, relheight=0.33, relx=0, rely=0.66)

        ##########################################
        # Frames for thumbnail photo specs
        frame_thumbnail_name = ttk.Frame(
            self.thumbnail_photo_specs_labelframe)
        frame_thumbnail_name.place(
            relwidth=1, relheight=0.5, relx=0, rely=0)

        frame_thumbnail_size = ttk.Frame(
            self.thumbnail_photo_specs_labelframe)
        frame_thumbnail_size.place(
            relwidth=1, relheight=0.5, relx=0, rely=0.5)

        ##########################################
        # Labels for oryginal photo specs
        label_oryginal_name = ttk.Label(
            frame_oryginal_name, font=("Roboto", 8), text=f"Nazwa: {original_photo['image_name']}")
        label_oryginal_name.place(relwidth=0.9, relx=0.05, rely=0.1)
        label_oryginal_name.bind(
            "<Configure>", lambda e: label_oryginal_name.configure(wraplength=e.width))
        original_tooltip = Tooltip(
            label_oryginal_name, original_photo['image_name'])

        label_oryginal_resolution = ttk.Label(
            frame_oryginal_resolution, font=("Roboto", 8), text=f"Wymiary: {original_photo['image_width']} x {original_photo['image_height']}")
        label_oryginal_resolution.place(relwidth=0.9, relx=0.05, rely=0.1)

        label_oryginal_size = ttk.Label(
            frame_oryginal_size, font=("Roboto", 8), text=f"Rozmiar: {original_photo['image_size_bytes']}")
        label_oryginal_size.place(relwidth=0.9, relx=0.05, rely=0.1)

        ##########################################
        # Labels for new photo specs
        self.label_new_name = ttk.Label(
            frame_new_name, font=("Roboto", 8), text=f"Nazwa: {new_photo['new_image_name']}")
        self.label_new_name.place(relwidth=0.9, relx=0.05, rely=0.1)
        self.label_new_name.bind(
            "<Configure>", lambda e: self.label_new_name.configure(wraplength=e.width))
        new_tooltip = Tooltip(self.label_new_name, new_photo['new_image_name'])

        self.label_new_resolution = ttk.Label(
            frame_new_resolution, font=("Roboto", 8), text=f"Wymiary: {new_photo['new_image_width']} x {new_photo['new_image_height']}")
        self.label_new_resolution.place(relwidth=0.9, relx=0.05, rely=0.1)

        self.label_new_size = ttk.Label(
            frame_new_size, font=("Roboto", 8), text=f"Rozmiar: {new_photo['new_image_size_bytes']}")
        self.label_new_size.place(relwidth=0.9, relx=0.05, rely=0.1)

        ##########################################
        # Labels for thumbnail photo specs
        self.label_thumbnail_name = ttk.Label(
            frame_thumbnail_name, font=("Roboto", 8))
        self.label_thumbnail_name.place(relwidth=0.9, relx=0.05, rely=0.1)

        self.label_thumbnail_size = ttk.Label(
            frame_thumbnail_size, font=("Roboto", 8))
        self.label_thumbnail_size.place(relwidth=0.9, relx=0.05, rely=0.1)

        if self.thumbnail_checkbutton_variable.get() == 1:
            self.label_thumbnail_name.config(
                text=f"Nazwa: {thumbnail_photo['thumbnail_image_name']}")
            self.label_thumbnail_name.bind(
                "<Configure>", lambda e: self.abel_thumbnail_name.configure(wraplength=e.width))
            thumbnail_tooltip = Tooltip(
                self.label_thumbnail_name, f"{thumbnail_photo['thumbnail_image_name']}")

            self.label_thumbnail_size.config(
                text=f"Rozmiar: {thumbnail_photo['thumbnail_image_size_bytes']}")

    ###############################################################
    # Other functions

    def bytes_to_str(self, size_bytes):
        if size_bytes >= 1024**3:
            image_size_gb = size_bytes / (1024**3)
            size_str = f"{image_size_gb:.2f} GB"

        elif size_bytes >= 1024**2:
            image_size_mb = size_bytes / (1024**2)
            size_str = f"{image_size_mb:.2f} MB"
        else:
            image_size_kb = size_bytes / 1024
            size_str = f"{image_size_kb:.2f} KB"

        return size_str

    def enable_photo_options(self):
        self.thumbnail_label.config(bootstyle="default")
        self.toggle_jpeg_webp_checkbutton.config(state=tk.NORMAL)
        self.thumbnail_checkbutton.config(state=tk.NORMAL)
        self.label_jpeg.config(bootstyle="default")

    def refresh_photo_specs(self):
        try:
            image = self.image.copy()
            new_photo = self.get_new_photo(image, self.new_image_format())
            if self.thumbnail_checkbutton_variable.get() == 1:
                thumbnail_photo = self.get_thumbnail_photo(
                    image, self.new_image_format(), new_photo)
                thumbnail = True

            if not new_photo:
                raise Exception("Nie udało się załadować zdjęcia")
        except Exception as e:
            messagebox.showerror("Błąd refresh", e)
        else:
            self.label_new_name.config(
                text=f"Nazwa: {new_photo['new_image_name']}")
            self.label_new_resolution.config(
                text=f"Wymiary: {new_photo['new_image_width']} x {new_photo['new_image_height']}")
            self.label_new_size.config(
                text=f"Rozmiar: {new_photo['new_image_size_bytes']}")

            if self.thumbnail_checkbutton_variable.get() == 1:
                self.label_thumbnail_name.config(
                    text=f"Nazwa: {thumbnail_photo['thumbnail_image_name']}")
                self.label_thumbnail_size.config(
                    text=f"Rozmiar: {thumbnail_photo['thumbnail_image_size_bytes']}")

        # def create_tab_categories(self):
        #     tab_categories = ttk.Frame(self.notebook)
        #     self.notebook.add(tab_categories, text="Kategorie")

        #     self.category_entries = {}

        #     root_dir = "categories"
        #     for category in listdir(root_dir):
        #         category_path = path.join(root_dir, category)
        #         if path.isdir(category_path):
        #             num_docx = sum(1 for file in listdir(
        #                 category_path) if file.endswith('.docx'))
        #             label_text = f"{category} ({num_docx} plików .docx)"

        #             categories_list_frame = ttk.Frame(tab_categories)
        #             categories_list_frame.pack(
        #                 fill="x", padx=10, pady=10, side="top")

        #             checkbox_var = tk.IntVar()
        #             checkbox = ttk.Checkbutton(
        #                 categories_list_frame, variable=checkbox_var)
        #             checkbox.pack(anchor="w", padx=5, pady=5, side="left")

        #             label = ttk.Label(categories_list_frame, text=label_text)
        #             label.pack(anchor="w", padx=5, pady=5, side="left")

        #             separator = ttk.Separator(
        #                 tab_categories, orient="horizontal", bootstyle="primary")
        #             separator.pack(fill="x", padx=5, pady=5, side="top")

        #             self.category_entries[category] = checkbox_var

        #     tool_labelframe = ttk.LabelFrame(
        #         tab_categories, bootstyle="primary", padding=10)
        #     tool_labelframe.pack(side="bottom", fill="x", padx=10, pady=10)

        #     add_button = ttk.Button(
        #         tool_labelframe, text="Dodaj kategorię", command=self.add_category)
        #     add_button.grid(row=0, column=0, padx=5)

        #     remove_button = ttk.Button(
        #         tool_labelframe, text="Usuń kategorie", command=self.remove_selected_categories, bootstyle="danger")
        #     remove_button.grid(row=0, column=1, padx=5)

        #     print(self.category_entries)

        # def add_category(self):
        #     new_category_name = simpledialog.askstring(
        #         "Nowa kategoria", "Wprowadź nazwę nowej kategorii:")
        #     if new_category_name:
        #         category_path = path.join("categories", new_category_name)
        #         if not path.exists(category_path):
        #             mkdir(category_path)
        #             self.refresh_categories()
        #             print(f"Dodano nową kategorię: {new_category_name}")

        # def remove_selected_categories(self):
        #     selected_categories = [
        #         category for category, checkbox_var in self.category_entries.items() if checkbox_var.get() == 1]

        #     if selected_categories:
        #         confirmation = messagebox.askokcancel(
        #             "Usuwanie kategorii", f"Czy na pewno chcesz usunąć:\n{', '.join(selected_categories)}?")
        #         if confirmation:
        #             for category_name in selected_categories:
        #                 category_path = path.join("categories", category_name)
        #                 if path.exists(category_path):
        #                     rmdir(category_path)
        #                     print(f"Usunięto kategorię: {category_name}")
        #             self.refresh_categories()

    def on_tab_changed(self, event):
        # Zapisz indeks aktywnej zakładki przy zmianie
        self.active_tab_index = self.notebook.index(self.notebook.select())

    # def refresh_categories(self):
    #     for widget in self.notebook.winfo_children():
    #         widget.destroy()
    #     self.create_tab_blog()
    #     self.create_tab_categories()
    #     self.create_tab_settings()

    #     if hasattr(self, 'active_tab_index'):
    #         # Przywróć aktywną zakładkę po odświeżeniu
    #         self.notebook.select(self.active_tab_index)

    # def create_tab_settings(self):
    #     tab_settings = ttk.Frame(self.notebook)
    #     self.notebook.add(tab_settings, text="Ustawienia")

    #     label_frame = ttk.LabelFrame(
    #         tab_settings, text="Ustawienia", bootstyle="primary")
    #     label_frame.grid(row=0, column=0, padx=10, pady=10)

    #     label = ttk.Label(label_frame, text="Tryb ciemny")
    #     label.grid(row=0, column=0, padx=10, pady=10)

    #     self.toggle_dark_button = ttk.Checkbutton(label_frame,
    #                                               bootstyle="primary-round-toggle", command=self.toggle_dark_mode)
    #     self.toggle_dark_button.grid(row=0, column=1, padx=10, pady=10)

    #     label = ttk.Label(label_frame, text="Język")
    #     label.grid(row=1, column=0, padx=10, pady=10)

    #     self.language_combobox = ttk.Combobox(
    #         label_frame, state="readonly", width=28)
    #     self.language_combobox.grid(
    #         row=1, column=1, padx=10, pady=10, columnspan=2)

    #     self.language_combobox["values"] = ["Polski", "Angielski"]
    #     self.language_combobox.bind(
    #         "<<ComboboxSelected>>", self.change_language)

    # def toggle_dark_mode(self):
    #     # Ta funkcja zostanie wywołana po zmianie stanu przycisku trybu ciemnego
    #     dark_mode_enabled = self.toggle_dark_button.instate(['selected'])
    #     if dark_mode_enabled:
    #         # Włącz tryb ciemny
    #         root = ttk.Style(theme="darkly")
    #         # Dodaj tutaj kod do włączenia trybu ciemnego w aplikacji
    #     else:
    #         # Wyłącz tryb ciemny
    #         root = ttk.Style(theme="litera")
    #         # Dodaj tutaj kod do wyłączenia trybu ciemnego w aplikacji

    # def change_language(self, event):
        # # Ta funkcja zostanie wywołana po wybraniu opcji z rozwijanej listy języków
        # selected_language = self.language_combobox.get()
        # # Dodaj tutaj kod do zmiany języka w aplikacji na wybrany

    # def add_entry_to_csv(self):
    #     keyword = self.entry_keyword.get()
    #     meta_title = self.entry_meta_title.get()

    #     if keyword and meta_title:
    #         csv_filename = "blog_entries.csv"

    #         with open(csv_filename, mode='a', newline='') as csv_file:
    #             csv_writer = csv.writer(csv_file)
    #             # Dodaj więcej pól według potrzeb
    #             csv_writer.writerow([keyword, meta_title])

    #         print("Wpis dodany do pliku CSV")


def main():
    # check if file and folders exists if not create them
    if not os.path.exists("blog_entries.csv"):
        with open("blog_entries.csv", "w") as file:
            file.write("keyword;meta_title;meta_description;link\n")

    if not os.path.exists("categories"):
        os.makedirs("categories")

    root_dir = "categories"
    folders = [category for category in listdir(
        root_dir) if path.isdir(path.join(root_dir, category))]

    for folder in folders:
        if not os.listdir(path.join(root_dir, folder)):
            os.makedirs(path.join(root_dir, folder, "images"))
            os.makedirs(path.join(root_dir, folder, "images\\original"))
            os.makedirs(path.join(root_dir, folder, "images\\webp"))
            os.makedirs(path.join(root_dir, folder,
                        "images\\thumbnails_webp"))

        else:
            if not os.listdir(path.join(root_dir, folder, "images")):
                os.makedirs(path.join(root_dir, folder, "images\\original"))
                os.makedirs(path.join(root_dir, folder, "images\\webp"))
                os.makedirs(path.join(root_dir, folder,
                            "images\\thumbnails_webp"))

    image_count = {}

    for folder in folders:
        count = 0
        files = listdir(path.join(root_dir, folder, "images\\webp"))
        for file in files:
            if file[-4:] == "webp":
                count += 1
        image_count.update({folder: count})

    # root = tk.Tk()
    root = ttk.Window(themename="darkly")
    root.geometry("800x800")
    root.minsize(800, 800)
    app = App(root, image_count)
    root.mainloop()


if __name__ == "__main__":
    main()
