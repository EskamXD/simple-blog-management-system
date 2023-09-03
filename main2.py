import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ParentWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("JPG/PNG to WebP Converter with Compression")
        self.master.geometry("700x500")
        self.master.configure(bg="#f0f0f0")

        self.custom_font = ("Arial", 10)

        # Variables for storing folder paths and compression quality
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.quality_slider = tk.Scale(self.master, from_=0, to=100, orient="horizontal",
                                       label="Compression Quality (%)", length=300, font=self.custom_font)
        self.quality_slider.set(80)

        # Title label
        self.title_label = tk.Label(self.master, text="JPG/PNG to WebP Converter", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frame for selecting source folder
        self.source_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.source_frame.pack(pady=10)

        # Label and entry for selecting the source folder
        self.input_label = tk.Label(self.source_frame, text="Select Folder with Images:", font=self.custom_font,
                                    bg="#f0f0f0")
        self.input_label.pack(side=tk.LEFT, padx=10)
        self.txt_browse1 = tk.Entry(self.source_frame, width=50, font=self.custom_font)
        self.txt_browse1.pack(side=tk.LEFT, padx=10)

        # Button to browse the source folder
        self.input_folder_button = tk.Button(self.source_frame, text="Browse...", command=self.select_input_folder,
                                             bg="#007bff", fg="white", font=self.custom_font)
        self.input_folder_button.pack(side=tk.RIGHT, padx=10)

        # "Or" separator
        self.or_label = tk.Label(self.master, text="OR", font=self.custom_font, bg="#f0f0f0")
        self.or_label.pack(padx=10)

        # Frame for selecting the image file
        self.image_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.image_frame.pack(pady=10)

        # Label and entry for selecting the image file
        self.image_label = tk.Label(self.image_frame, text="Select Image File:", font=self.custom_font, bg="#f0f0f0")
        self.image_label.pack(side=tk.LEFT, padx=10)
        self.txt_browse2 = tk.Entry(self.image_frame, width=50, font=self.custom_font)
        self.txt_browse2.pack(side=tk.LEFT, padx=10)

        # Button to browse the image file
        self.image_button = tk.Button(self.image_frame, text="Browse...", command=self.select_image_file,
                                      bg="#007bff", fg="white", font=self.custom_font)
        self.image_button.pack(side=tk.RIGHT, padx=10)

        # Label to display selected source folder or image file
        self.selected_source_label = tk.Label(self.master, text="", font=self.custom_font, bg="#f0f0f0")
        self.selected_source_label.pack(pady=5)

        # Separator
        self.separator = tk.Frame(self.master, height=2, width=400, bg="#999999")
        self.separator.pack(fill="x", pady=10)

        # Frame for selecting destination folder
        self.destination_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.destination_frame.pack(pady=10)

        # Label and entry for selecting the destination folder
        self.output_label = tk.Label(self.destination_frame, text="Select Destination Folder:", font=self.custom_font,
                                     bg="#f0f0f0")
        self.output_label.pack(side=tk.LEFT, padx=10)
        self.txt_browse3 = tk.Entry(self.destination_frame, width=50, font=self.custom_font)
        self.txt_browse3.pack(side=tk.LEFT, padx=10)

        # Button to browse the destination folder
        self.output_folder_button = tk.Button(self.destination_frame, text="Browse...",
                                              command=self.select_output_folder, bg="#007bff", fg="white",
                                              font=self.custom_font)
        self.output_folder_button.pack(side=tk.RIGHT, padx=10)

        # Label to display selected destination folder
        self.selected_destination_label = tk.Label(self.master, text="", font=self.custom_font, bg="#f0f0f0")
        self.selected_destination_label.pack(pady=5)

        # Scale widget to set compression quality
        self.quality_slider.pack(pady=10)

        # Convert button
        self.convert_button = tk.Button(self.master, text="Convert Images", command=self.process_images,
                                        bg="#007bff", fg="white", font=("Arial", 12, "bold"))
        self.convert_button.pack(pady=20)

    def select_input_folder(self):
        """Opens a folder dialog to select the input folder with images."""
        dirname = filedialog.askdirectory()
        self.txt_browse1.delete("1", tk.END)
        self.txt_browse1.insert("1", dirname)

    def select_image_file(self):
        """Opens a file dialog to select an image file."""
        filename = filedialog.askopenfilename(title="Select Image File",
                                              filetypes=[("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"), ("PNG Files", "*.png"), ("All Files", "*.*")])
        self.txt_browse2.delete("1", tk.END)
        self.txt_browse2.insert("1", filename)

    def select_output_folder(self):
        """Opens a folder dialog to select the output destination folder."""
        dirname = filedialog.askdirectory()
        self.txt_browse3.delete("1", tk.END)
        self.txt_browse3.insert("1", dirname)

    def process_images(self):
        """Processes the images based on the selected source and destination, either a folder or an image file."""
        source_path = self.txt_browse1.get()
        destination_folder = self.txt_browse3.get()

        if not source_path or not destination_folder:
            tk.messagebox.showerror("Error", "Please select source and destination folders.")
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        if os.path.isfile(source_path):  # A single image file is selected
            image_name = os.path.basename(source_path)
            output_path = os.path.join(destination_folder, os.path.splitext(image_name)[0] + ".webp")
            self.convert_to_webp(source_path, output_path, quality=self.quality_slider.get())
        else:  # A folder with images is selected
            self.batch_convert_to_webp(source_path, destination_folder, quality=self.quality_slider.get())

        tk.messagebox.showinfo("Conversion Complete", "Photo to WebP conversion with compression is complete!")

    def convert_to_webp(self, input_path, output_path, quality=80):
        """Converts an image from JPG to WebP format and applies compression."""
        img = Image.open(input_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        webp_output_path = os.path.splitext(output_path)[0] + ".webp"
        img.save(webp_output_path, "WebP", quality=quality)
        print(f"Converted {input_path} to {webp_output_path} with quality {quality}%.")

    def batch_convert_to_webp(self, input_dir, output_dir, quality=80):
        """Batch converts JPG/PNG images to WebP format and applies compression."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file in os.listdir(input_dir):
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png"):
                input_path = os.path.join(input_dir, file)
                output_path = os.path.join(output_dir, file)
                self.convert_to_webp(input_path, output_path, quality)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParentWindow(root)
    app.mainloop()
