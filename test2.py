import tkinter as tk
from tkinter import ttk, filedialog, font
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Zarządzanie blogiem")

# Creating a Font object of "TkDefaultFont"
defaultFont = font.nametofont("TkDefaultFont")

# Overriding default-font with custom settings
# i.e changing font-family, size and weight
defaultFont.configure(family="Roboto", size=14)

style = ttk.Style(root)
style.theme_use("default")
style.configure("TButton", foreground="white",
                background="#b2abfb",
                font=("Roboto", 44),
                padding=[10, 10, 10, 10])

style.map("TButton", background=[
          ("active", "#c3bcgc")], foreground=[("active", "#ffffff")])

button1 = ttk.Button(root, text="Test", style="My.TButton")
button1.pack(padx=10, pady=10)

# def create_widgets():
#     notebook = ttk.Notebook(root)
#     notebook_styled = ttk.Style()
#     # Ustaw kolor tła na #21252B
#     notebook_styled.configure("TNotebook", background="#21252B")
#     notebook.pack(fill="both", expand=True)

#     create_tab_blog(notebook)
#     # .create_tab2()


# def create_tab_blog(notebook):
#     tab_blog = ttk.Frame(notebook)
#     tab_blog_styled = ttk.Style()

#     tab_blog_styled.configure("TFrame", background="#21252B")
#     tab_blog_styled.configure("TLabel", background="#21252B")
#     # tab_blog_styled.configure("TButton", background="#21252B")
#     # tab_blog_styled.configure("TCheckbutton", background="#21252B")
#     # tab_blog_styled.configure(
#     #     "TEntry", background="#21252B", foreground="#FFFFFF", width=30, borderwidth=0, fieldbackground="#21252B")

#     notebook.add(tab_blog, text="Blog")

#     label1 = ttk.Label(
#         tab_blog, text="Słowo kluczowe")
#     label1.grid(row=0, column=0, padx=10, pady=10)

#     entry1 = ttk.Entry(tab_blog, style="TEntry")
#     entry1.grid(row=0, column=1, padx=10, pady=10)

#     label2 = ttk.Label(tab_blog, text="Tytuł")
#     label2.grid(row=1, column=0, padx=10, pady=10)

#     entry2 = ttk.Entry(tab_blog, style="My.TEntry")
#     entry2.grid(row=1, column=1, padx=10, pady=10)

#     label3 = ttk.Label(tab_blog, text="Zdjęcie")
#     label3.grid(row=2, column=0, padx=10, pady=10, rowspan=2)

#     button1 = ttk.Button(
#         tab_blog, text="Wybierz plik", style="My.TButton")
#     button1.grid(row=2, column=1, padx=10, pady=10, rowspan=2)

#     label4 = ttk.Label(tab_blog, text="Miniaturka")
#     label4.grid(row=2, column=2, padx=10, pady=10)

#     # Zmienna do przechowywania stanu Checkbutton
#     checkbutton1_var = tk.IntVar()
#     checkbutton1 = ttk.Checkbutton(
#         tab_blog, variable=checkbutton1_var)
#     checkbutton1.grid(row=2, column=3, padx=10, pady=10)

#     # Początkowo dezaktywowane
#     label5 = ttk.Label(tab_blog, text="Rozmiar", state=tk.DISABLED)
#     label5.grid(row=3, column=2, padx=10, pady=10)

#     # Początkowo dezaktywowane
#     entry_widht = ttk.Entry(
#         tab_blog, style="My.TEntry", width=5, state=tk.DISABLED)
#     entry_widht.grid(row=3, column=3, padx=10, pady=10)

#     # Początkowo dezaktywowane
#     entry_height = ttk.Entry(
#         tab_blog, style="My.TEntry", width=5, state=tk.DISABLED)
#     entry_height.grid(row=3, column=4, padx=10, pady=10)

#     checkbutton1.config(command=lambda: toggle_checkbutton1(
#         checkbutton1_var, label5, entry_widht, entry_height))

#     label6 = ttk.Label(tab_blog)
#     label6.grid(row=4, column=0, padx=10, pady=10, columnspan=5)
#     button1.config(command=lambda: load_image(label6))

#     button2 = ttk.Button(tab_blog, text="Wpisz do bazy")
#     button2.grid(row=5, column=0, padx=10, pady=10, columnspan=5)

# # def create_tab2():
# #     tab2 = ttk.Frame(.notebook)
# #     .notebook.add(tab2, text="Zakładka 2")

# #     label2 = tk.Label(tab2, text="To jest zawartość zakładki 2")
# #     label2.pack(padx=10, pady=10)


# def load_image(label6):
#     file_path = filedialog.askopenfilename(
#         filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
#     if file_path:
#         image = Image.open(file_path)
#         # Zmniejsz obraz do wymiarów 100x100 (możesz dostosować rozmiar)
#         image.thumbnail((300, 300))
#         photo = ImageTk.PhotoImage(image)
#         label6.config(image=photo)
#         label6.image = photo


# def toggle_checkbutton1(checkbutton1_var, label5, entry_widht, entry_height):
#     if checkbutton1_var.get() == 1:  # Jeśli Checkbutton jest zaznaczony
#         state = tk.NORMAL  # Ustawiamy stan na NORMAL (aktywny)
#     else:
#         # W przeciwnym razie ustawiamy stan na DISABLED (dezaktywowany)
#         state = tk.DISABLED

#     # Ustawiamy stan elementów interfejsu
#     label5.config(state=state)
#     entry_widht.config(state=state)
#     entry_height.config(state=state)

# # def create_gradient(, size, color1, color2):
# #     gradient = Image.new("RGB", size)
# #     for y in range(size[1]):
# #         r = int((y / size[1]) * (int(color2[1:3], 16) -
# #                 int(color1[1:3], 16)) + int(color1[1:3], 16))
# #         g = int((y / size[1]) * (int(color2[3:5], 16) -
# #                 int(color1[3:5], 16)) + int(color1[3:5], 16))
# #         b = int((y / size[1]) * (int(color2[5:7], 16) -
# #                 int(color1[5:7], 16)) + int(color1[5:7], 16))
# #         for x in range(size[0]):
# #             gradient.putpixel((x, y), (r, g, b))
# #     return gradient


# create_widgets()
root.mainloop()
