"""
Filters Lab Module for PixelAlchemy.
Applies Pillow-based image filters.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageOps, UnidentifiedImageError
import logging
from modules import database
import os

class FiltersLab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_image = None
        self.filtered_image = None
        self.original_photo = None
        self.filtered_photo = None
        
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#313244", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(self.sidebar, text="Load Image", command=self.load_image).pack(fill=tk.X, pady=10, padx=10)
        
        self.filter_var = tk.StringVar(value="grayscale")
        filters = ["grayscale", "invert", "blur", "sharpen", "emboss", "edge_detect", "sepia", "pixelate"]
        
        for f in filters:
            tk.Radiobutton(self.sidebar, text=f.capitalize(), variable=self.filter_var, value=f, 
                           bg="#313244", fg="#cdd6f4", selectcolor="#45475a", 
                           activebackground="#313244", activeforeground="#cba6f7",
                           command=self.apply_filter).pack(anchor=tk.W, padx=10, pady=2)
                           
        ttk.Button(self.sidebar, text="Save Image", command=self.save_image).pack(fill=tk.X, pady=20, padx=10)
        
        # Preview Area
        self.preview_frame = tk.Frame(self, bg="#1e1e2e")
        self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_orig = tk.Canvas(self.preview_frame, bg="#11111b", highlightthickness=2, highlightbackground="#89dceb")
        self.canvas_orig.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas_filt = tk.Canvas(self.preview_frame, bg="#11111b", highlightthickness=2, highlightbackground="#f38ba8")
        self.canvas_filt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # REVIEW: Developer A - Consider adding a loading spinner here for large images.

    def load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not filepath:
            return
            
        try:
            self.original_image = Image.open(filepath).convert("RGB")
            self.filtered_image = self.original_image.copy()
            self.update_previews()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            logging.error(f"File not found: {filepath}")
        except UnidentifiedImageError:
            messagebox.showerror("Error", "Invalid image format.")
            logging.error(f"Unidentified image error: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            logging.error(f"Error loading image: {e}")

    def update_previews(self):
        if not self.original_image:
            return
            
        # Get canvas size
        self.update()
        cw = max(100, self.canvas_orig.winfo_width() - 10)
        ch = max(100, self.canvas_orig.winfo_height() - 10)
        
        # Resize for preview
        orig_preview = self.original_image.copy()
        orig_preview.thumbnail((cw, ch))
        self.original_photo = ImageTk.PhotoImage(orig_preview)
        
        self.canvas_orig.delete("all")
        self.canvas_orig.create_image(cw//2 + 5, ch//2 + 5, anchor=tk.CENTER, image=self.original_photo)
        
        if self.filtered_image:
            filt_preview = self.filtered_image.copy()
            filt_preview.thumbnail((cw, ch))
            self.filtered_photo = ImageTk.PhotoImage(filt_preview)
            
            self.canvas_filt.delete("all")
            self.canvas_filt.create_image(cw//2 + 5, ch//2 + 5, anchor=tk.CENTER, image=self.filtered_photo)

    def apply_filter(self):
        if not self.original_image:
            return
            
        filter_name = self.filter_var.get()
        
        # REFACTORED CODE (using dictionary dispatch)
        filter_actions = {
            "grayscale": lambda img: ImageOps.grayscale(img).convert("RGB"),
            "invert": lambda img: ImageOps.invert(img),
            "blur": lambda img: img.filter(ImageFilter.BLUR),
            "sharpen": lambda img: img.filter(ImageFilter.SHARPEN),
            "emboss": lambda img: img.filter(ImageFilter.EMBOSS),
            "edge_detect": lambda img: img.filter(ImageFilter.FIND_EDGES),
            "sepia": self._apply_sepia,
            "pixelate": self._apply_pixelate
        }
        
        if filter_name in filter_actions:
            try:
                self.filtered_image = filter_actions[filter_name](self.original_image.copy())
                self.update_previews()
            except Exception as e:
                logging.error(f"Error applying filter {filter_name}: {e}")
                messagebox.showerror("Filter Error", f"Could not apply filter: {e}")

        # LEGACY CODE (before refactor)
        # if filter_name == "grayscale":
        #     self.filtered_image = ImageOps.grayscale(self.original_image).convert("RGB")
        # elif filter_name == "invert":
        #     self.filtered_image = ImageOps.invert(self.original_image)
        # elif filter_name == "blur":
        #     self.filtered_image = self.original_image.filter(ImageFilter.BLUR)
        # elif filter_name == "sharpen":
        #     self.filtered_image = self.original_image.filter(ImageFilter.SHARPEN)
        # elif filter_name == "emboss":
        #     self.filtered_image = self.original_image.filter(ImageFilter.EMBOSS)
        # elif filter_name == "edge_detect":
        #     self.filtered_image = self.original_image.filter(ImageFilter.FIND_EDGES)
        # elif filter_name == "sepia":
        #     self.filtered_image = self._apply_sepia(self.original_image)
        # elif filter_name == "pixelate":
        #     self.filtered_image = self._apply_pixelate(self.original_image)
        # self.update_previews()

    def _apply_sepia(self, img):
        # Optimized sepia formula using PIL's color matrix for speed
        sepia_matrix = (
            0.393, 0.769, 0.189, 0,
            0.349, 0.686, 0.168, 0,
            0.272, 0.534, 0.131, 0
        )
        return img.convert("RGB", sepia_matrix)

    def _apply_pixelate(self, img):
        pixel_size = 10
        img_small = img.resize(
            (img.size[0] // pixel_size, img.size[1] // pixel_size),
            resample=Image.Resampling.BILINEAR
        )
        return img_small.resize(img.size, Image.Resampling.NEAREST)

    def save_image(self):
        if not self.filtered_image:
            return
            
        title = simpledialog.askstring("Save Filtered Image", "Enter a title:")
        if not title:
            return
            
        try:
            os.makedirs("saved_art", exist_ok=True)
            filename = f"saved_art/filter_{title.replace(' ', '_')}.png"
            self.filtered_image.save(filename)
            
            # Save to db
            database.save_artwork(title, filename, "filter", self.filter_var.get())
            
            messagebox.showinfo("Success", f"Image saved successfully!")
            logging.info(f"Exported filtered image to {filename}")
        except Exception as e:
            logging.error(f"Failed to save image: {e}")
            messagebox.showerror("Error", f"Failed to save image.\n{str(e)}")
