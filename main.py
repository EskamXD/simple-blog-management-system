import tkinter as tk
from tkinter import filedialog, font, messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
import csv
from os import listdir, rmdir, path, mkdir
import os


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Zarządzanie blogiem")
        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Roboto",
                                   size=14)

        self.create_widgets()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True)

        self.create_tab_blog_old()
        self.create_tab_blog()
        # self.create_tab_categories()
        # self.create_tab_settings()

    def create_tab_blog_old(self):
        tab_blog = ttk.Frame(self.notebook)
        tab_blog.pack(fill="both", expand=True)

        self.notebook.add(tab_blog, text="Blog.old")

        """
        Dodaj ramkę z etykietami i polami do wprowadzania danych
        """
        label_frame_text = ttk.LabelFrame(
            tab_blog, text="Metadane", bootstyle="primary")
        label_frame_text.grid(row=0, column=0, padx=10, pady=10)

        self.label_folder = ttk.Label(label_frame_text, text="Kategoria")
        self.label_folder.grid(row=0, column=0, padx=10, pady=10)

        """
        Dodaj Combobox do wyboru kategorii
        """
        self.folder_combobox = ttk.Combobox(
            label_frame_text, state="readonly", width=28)
        self.folder_combobox.grid(
            row=0, column=1, padx=10, pady=10, columnspan=2)

        """
        Dodaj opcje do Combobox
        """
        root_dir = "categories"
        folders = [category for category in listdir(
            root_dir) if path.isdir(path.join(root_dir, category))]

        self.folder_combobox["values"] = folders

        """
        Dodaj etykiety i pola do wprowadzania danych słów kluczowych"""
        self.label_keyword = ttk.Label(
            label_frame_text, text="Słowo kluczowe")
        self.label_keyword.grid(row=1, column=0, padx=10, pady=10)

        self.entry_keyword = ttk.Entry(label_frame_text, width=30)
        self.entry_keyword.grid(
            row=1, column=1, padx=10, pady=10, columnspan=2)

        """
        Dodaj etykiety i pola do wprowadzania danych meta tytułu
        """
        self.label_meta_title = ttk.Label(label_frame_text, text="Tytuł")
        self.label_meta_title.grid(
            row=2, column=0, padx=10, pady=10, rowspan=2)

        self.entry_meta_title = ttk.Entry(label_frame_text)
        self.entry_meta_title.grid(
            row=2, column=1, padx=10, pady=10, rowspan=2)
        self.entry_meta_title.bind("<KeyRelease>", self.calculate_width)

        """
        Dodaj etykiety szerokości tytułu i progessbar
        """
        self.width_label = ttk.Label(
            label_frame_text, text="0 / 60 (0px / 600px)", font=("Roboto", 10))
        self.width_label.grid(row=2, column=2, padx=10, pady=1)

        # self.progress_bar = ttk.Progressbar(
        #     label_frame_text, mode="determinate", maximum=60)
        # self.progress_bar.grid(row=3, column=2,
        #                        padx=10, pady=1, sticky="w")

        """
        Frame for photo
        """
        label_frame_photo = ttk.LabelFrame(
            tab_blog, text="Zdjęcie", bootstyle="primary")
        label_frame_photo.grid(row=1, column=0, padx=10, pady=10)

        self.label_photo = ttk.Label(label_frame_photo, text="Zdjęcie")
        self.label_photo.grid(row=2, column=0,
                              padx=10, pady=10, rowspan=2)

        self.button_choose_photo = ttk.Button(
            label_frame_photo, text="Wybierz plik", command=self.load_image)
        self.button_choose_photo.grid(
            row=2, column=1, padx=10, pady=10, rowspan=2)

        self.label_thumbnail = ttk.Label(label_frame_photo, text="Miniaturka")
        self.label_thumbnail.grid(row=2, column=2, padx=10, pady=10)

        # Zmienna do przechowywania stanu Checkbutton
        # self.checkbutton1_var = tk.IntVar()
        # self.checkbutton1 = ttk.Checkbutton(
        #     label_frame_photo, variable=self.checkbutton1_var, command=self.toggle_checkbutton1)
        # self.checkbutton1.grid(row=2, column=3, padx=10, pady=10)

        # Początkowo dezaktywowane
        self.label_thumbnail_size = ttk.Label(
            label_frame_photo, text="Rozmiar", state=tk.DISABLED, bootstyle="secondary")
        self.label_thumbnail_size.grid(
            row=3, column=2, padx=10, pady=10)

        # Początkowo dezaktywowane
        self.entry_thumbnail_widht = ttk.Entry(
            label_frame_photo, width=5, state=tk.DISABLED, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"), bootstyle="disabled")
        self.entry_thumbnail_widht.grid(
            row=3, column=3, padx=10, pady=10)

        # Początkowo dezaktywowane
        self.entry_thumbnail_height = ttk.Entry(
            label_frame_photo, width=5, state=tk.DISABLED, validate="key", validatecommand=(self.root.register(self.validate_number), "%P"), bootstyle="disabled")
        self.entry_thumbnail_height.grid(
            row=3, column=4, padx=10, pady=10)

        self.label_for_photo = ttk.Label(label_frame_photo)
        self.label_for_photo.grid(
            row=4, column=0, padx=10, pady=10, columnspan=5)

        # self.button_save_to_csv = ttk.Button(
        # tab_blog, text="Wpisz do bazy", command=self.add_entry_to_csv)
        # self.button_save_to_csv.grid(
        #     row=5, column=0, padx=10, pady=10, columnspan=5)

    def create_tab_blog(self):
        # Notebook tab about blog title, metadata, photo
        notebook_tab_blog = ttk.Frame(self.notebook)
        notebook_tab_blog.pack(fill="both", expand=True)
        self.notebook.add(notebook_tab_blog, text="Blog")

        """begin of lebalframes for blog tab"""

        # label frames
        metadata_labelframe = ttk.LabelFrame(notebook_tab_blog, text="Metadane",
                                             bootstyle="primary")
        metadata_labelframe.place(relwidth=1, relheight=0.3, relx=0, rely=0)

        photo_labelframe = ttk.LabelFrame(notebook_tab_blog, text="Zdjęcie",
                                          bootstyle="primary")
        photo_labelframe.place(relwidth=1, relheight=0.6, relx=0, rely=0.3)

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

        ###############################################################
        # begin of widgets in left_frame_metadata
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

        ###############################################################
        # widgets for keyword_frame
        keyword_label = ttk.Label(keyword_frame, text="Słowo kluczowe")
        keyword_label.place(relwidth=0.25, relx=0.05, rely=0)

        self.keyword_entry = ttk.Entry(keyword_frame)
        self.keyword_entry.place(
            relwidth=0.65, relx=0.3, rely=0)

        ###############################################################
        # widgets for title_frame
        title_label = ttk.Label(title_frame, text="Tytuł")
        title_label.place(relwidth=0.25, relx=0.05, rely=0)

        self.title_entry = ttk.Entry(title_frame)
        self.title_entry.place(
            relwidth=0.65, relx=0.3, rely=0)
        self.title_entry.bind("<KeyRelease>", self.calculate_width)
        # end of widgets in left_frame_metadata
        ###############################################################

        ###############################################################
        # widgets in right_frame_metadata
        self.word_counter_label = ttk.Label(
            right_frame_metadata, text="0 / 60 (0px / 600px)", font=("Roboto", 9), justify="right")
        self.word_counter_label.place(
            relwidth=0.95, relx=0, rely=0.63)

        self.progress_bar = ttk.Progressbar(
            right_frame_metadata, mode="determinate", maximum=60)
        self.progress_bar.place(relwidth=0.95,
                                relx=0., rely=0.77)
        # end of widgets in right_frame_metadata
        ###############################################################

        """end of widgets in labelframe "Metadane" """

        """begin of widgets in labelframe "Zdjęcie" """

        ###############################################################
        # begin of widgets in left_frame_photos
        # splitting left_frame_photos into 2 frames
        top_left_frame_photos = ttk.Frame(left_frame_photos)
        top_left_frame_photos.place(relwidth=1, relheight=0.2, relx=0, rely=0)

        bottom_left_frame_photos = ttk.Frame(left_frame_photos)
        bottom_left_frame_photos.place(
            relwidth=1, relheight=0.8, relx=0, rely=0.2)

        ###############################################################
        # widgets in left_frame_photos
        photo_label = ttk.Label(top_left_frame_photos, text="Zdjęcie")
        photo_label.place(relwidth=0.25, relx=0.05, rely=0.1)

        self.photo_button = ttk.Button(
            top_left_frame_photos, text="Wybierz plik", command=self.load_image)
        self.photo_button.place(
            relwidth=0.2, relx=0.3, rely=0)

        thumbnail_frame = ttk.Frame(top_left_frame_photos)
        thumbnail_frame.place(relwidth=0.2, relheight=1, relx=0.55, rely=0.1)

        thumbnail_label = ttk.Label(thumbnail_frame, text="Miniaturka")
        thumbnail_label.place(relwidth=0.8, relx=0, rely=0)

        self.thumbnail_checkbutton_variable = tk.IntVar()
        self.thumbnail_checkbutton = ttk.Checkbutton(
            thumbnail_frame, variable=self.thumbnail_checkbutton_variable, command=self.thumbnail_checkbutton_action, bootstyle="primary-round-toggle")
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
        # end of widgets in left_frame_photos
        ###############################################################

        ###############################################################
        # begin of widgets in right_frame_photos
        # splitting right_frame_photos into 2 frames
        top_right_frame_photos = ttk.Frame(right_frame_photos)
        top_right_frame_photos.place(relwidth=1, relheight=0.2, relx=0, rely=0)

        bottom_right_frame_photos = ttk.Frame(right_frame_photos)
        bottom_right_frame_photos.place(
            relwidth=1, relheight=0.8, relx=0, rely=0.2)

        ###############################################################
        # widgets in right_frame_photos
        self.label_jpeg = ttk.Label(top_right_frame_photos,
                                    text="JPEG", font=("Roboto", 9))
        self.label_jpeg.place(relwidth=0.25, relx=0.05, rely=0.1)

        self.toggle_jpeg_webp_checkbutton = ttk.Checkbutton(
            top_right_frame_photos, bootstyle="primary-round-toggle", command=self.toggle_photo_format)
        self.toggle_jpeg_webp_checkbutton.place(
            relwidth=0.2, relx=0.3, rely=0.1)

        self.label_webp = ttk.Label(top_right_frame_photos, text="WEBP", font=(
            "Roboto", 9), bootstyle="secondary")
        self.label_webp.place(relwidth=0.25, relx=0.5, rely=0.1)

        # 2 label frames for pohoto specs

    ###############################################################
    # Buttons events

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            image = Image.open(file_path)
            # Zmniejsz obraz do wymiarów 100x100 (możesz dostosować rozmiar)
            width = self.loaded_photo_label.winfo_width()
            height = self.loaded_photo_label.winfo_height()
            image.thumbnail((width-width*0.05, height-height*0.05))
            photo = ImageTk.PhotoImage(image)
            self.loaded_photo_label.config(image=photo, anchor="center")
            self.loaded_photo_label.image = photo
    ###############################################################

    ###############################################################
    # Checkbutton events
    def thumbnail_checkbutton_action(self):
        if self.thumbnail_checkbutton_variable.get() == 1:
            state = tk.NORMAL
            style = "primary"
        else:
            state = tk.DISABLED
            style = "disabled"

        self.thb_width_entry.config(state=state, bootstyle=style)
        self.thb_height_entry.config(state=state, bootstyle=style)

    def toggle_photo_format(self):
        if self.toggle_jpeg_webp_checkbutton.instate(['selected']):
            self.label_webp.config(bootstyle="default")
            self.label_jpeg.config(bootstyle="secondary")
        else:
            self.label_webp.config(bootstyle="secondary")
            self.label_jpeg.config(bootstyle="default")
    ###############################################################

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
        # Ta funkcja zostanie wywołana po wybraniu opcji z rozwijanej listy języków
        selected_language = self.language_combobox.get()
        # Dodaj tutaj kod do zmiany języka w aplikacji na wybrany

    # def add_entry_to_csv(self):
        keyword = self.entry_keyword.get()
        meta_title = self.entry_meta_title.get()

        if keyword and meta_title:
            csv_filename = "blog_entries.csv"

            with open(csv_filename, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Dodaj więcej pól według potrzeb
                csv_writer.writerow([keyword, meta_title])

            print("Wpis dodany do pliku CSV")


def main():
    # check if file and folders exists if not create them
    if not os.path.exists("blog_entries.csv"):
        with open("blog_entries.csv", "w") as file:
            file.write("keyword;meta_title;meta_description;link\n")

    if not os.path.exists("images"):
        os.makedirs("images")

    if not os.path.exists("images/originals"):
        os.makedirs("images/originals")
    if not os.path.exists("images/webp"):
        os.makedirs("images/webp")

    if not os.path.exists("categories"):
        os.makedirs("categories")

    # root = tk.Tk()
    root = ttk.Window(themename="darkly")
    root.geometry("800x600")
    root.minsize(800, 600)
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
