"""
Generative Pattern Maker Module for PixelAlchemy.
Generates complex patterns using NumPy and PIL.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import logging
from modules import database
import os

class PatternMaker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pattern_image = None
        self.photo = None
        self.setup_ui()
        self.generate_pattern()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#313244", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Label(self.sidebar, text="Pattern Type:", background="#313244", foreground="#cdd6f4").pack(pady=(10, 2))
        self.type_var = tk.StringVar(value="waves")
        types = ["waves", "checkerboard", "mandala", "truchet"]
        
        for t in types:
            tk.Radiobutton(self.sidebar, text=t.capitalize(), variable=self.type_var, value=t,
                           bg="#313244", fg="#cdd6f4", selectcolor="#45475a",
                           command=self.generate_pattern).pack(anchor=tk.W, padx=10)
                           
        ttk.Label(self.sidebar, text="Complexity:", background="#313244", foreground="#cdd6f4").pack(pady=(15, 2))
        self.complexity_var = tk.DoubleVar(value=5.0)
        ttk.Scale(self.sidebar, from_=1.0, to=20.0, variable=self.complexity_var, command=lambda e: self.generate_pattern()).pack(fill=tk.X, padx=10)
        
        ttk.Label(self.sidebar, text="Color Shift:", background="#313244", foreground="#cdd6f4").pack(pady=(15, 2))
        self.color_var = tk.DoubleVar(value=0.0)
        ttk.Scale(self.sidebar, from_=0.0, to=255.0, variable=self.color_var, command=lambda e: self.generate_pattern()).pack(fill=tk.X, padx=10)
        
        ttk.Button(self.sidebar, text="Save Pattern", command=self.save_pattern).pack(fill=tk.X, pady=30, padx=10)
        
        # Preview
        self.preview_frame = tk.Frame(self, bg="#1e1e2e")
        self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.preview_frame, bg="#11111b", highlightthickness=2, highlightbackground="#fab387")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Throttle resize updates if needed
        pass

    def generate_pattern(self):
        try:
            width, height = 400, 400
            pattern_type = self.type_var.get()
            complexity = self.complexity_var.get()
            color_shift = self.color_var.get()
            
            # REFACTORED CODE (Dictionary mapping for algorithms)
            generators = {
                "waves": self._gen_waves,
                "checkerboard": self._gen_checkerboard,
                "mandala": self._gen_mandala,
                "truchet": self._gen_truchet
            }
            
            if pattern_type in generators:
                arr = generators[pattern_type](width, height, complexity, color_shift)
                self.pattern_image = Image.fromarray(arr, 'RGB')
                self.display_image()
                
            # LEGACY CODE (before refactor)
            # if pattern_type == "waves":
            #     arr = self._gen_waves(width, height, complexity, color_shift)
            # elif pattern_type == "checkerboard":
            #     arr = self._gen_checkerboard(width, height, complexity, color_shift)
            # elif pattern_type == "mandala":
            #     arr = self._gen_mandala(width, height, complexity, color_shift)
            # elif pattern_type == "truchet":
            #     arr = self._gen_truchet(width, height, complexity, color_shift)
            # self.pattern_image = Image.fromarray(arr, 'RGB')
            # self.display_image()
            
        except Exception as e:
            logging.error(f"Error generating pattern: {e}")

    def _gen_waves(self, w, h, comp, shift):
        # REVIEW: Scientist C - Numpy meshgrid is much faster here than nested Python loops!
        y, x = np.ogrid[0:h, 0:w]
        center_x, center_y = w/2, h/2
        dist1 = np.sqrt((x - center_x + 50)**2 + (y - center_y)**2)
        dist2 = np.sqrt((x - center_x - 50)**2 + (y - center_y)**2)
        
        wave1 = np.sin(dist1 / (21 - comp))
        wave2 = np.sin(dist2 / (21 - comp))
        
        val = (wave1 + wave2) / 2.0  # -1 to 1
        val = (val + 1) / 2 * 255
        
        r = (val + shift) % 255
        g = (val * 0.5 + shift * 1.5) % 255
        b = 255 - val
        
        return np.dstack((r, g, b)).astype(np.uint8)

    def _gen_checkerboard(self, w, h, comp, shift):
        y, x = np.mgrid[0:h, 0:w]
        size = max(5, int(50 - comp * 2))
        
        checkX = (x // size) % 2
        checkY = (y // size) % 2
        
        board = (checkX ^ checkY) * 255
        
        # Gradient
        grad = np.linspace(0, 255, w).reshape(1, -1)
        r = (board + grad + shift) % 255
        g = (board * 0.5) % 255
        b = (255 - grad + shift) % 255
        b = np.broadcast_to(b, (h, w))
        
        return np.dstack((r, g, b)).astype(np.uint8)

    def _gen_mandala(self, w, h, comp, shift):
        y, x = np.ogrid[0:h, 0:w]
        center_x, center_y = w/2, h/2
        
        dx = x - center_x
        dy = y - center_y
        
        dist = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        petals = int(comp) * 2
        val = np.sin(dist / 10.0) * np.cos(angle * petals)
        val = (val + 1) / 2 * 255
        
        r = (val + shift * 2) % 255
        g = 128 + np.sin(dist / 20.0) * 127
        b = 255 - val
        
        return np.dstack((r, g, b)).astype(np.uint8)

    def _gen_truchet(self, w, h, comp, shift):
        # A simple visual approximation using numpy noise
        arr = np.random.rand(h // 10, w // 10) > 0.5
        arr = np.kron(arr, np.ones((10, 10))) * 255
        
        r = (arr + shift) % 255
        g = 255 - arr
        b = (arr + comp * 10) % 255
        
        return np.dstack((r, g, b)).astype(np.uint8)

    def display_image(self):
        if self.pattern_image:
            self.photo = ImageTk.PhotoImage(self.pattern_image)
            self.canvas.delete("all")
            
            self.update()
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            
            # Center image
            self.canvas.create_image(max(cw//2, 200), max(ch//2, 200), image=self.photo, anchor=tk.CENTER)

    def save_pattern(self):
        if not self.pattern_image:
            return
            
        title = simpledialog.askstring("Save Pattern", "Enter a title:")
        if not title:
            return
            
        try:
            os.makedirs("saved_art", exist_ok=True)
            filename = f"saved_art/pattern_{title.replace(' ', '_')}.png"
            self.pattern_image.save(filename)
            
            config = f"Type: {self.type_var.get()}, Comp: {self.complexity_var.get()}, Shift: {self.color_var.get()}"
            database.save_artwork(title, filename, "pattern", config)
            
            messagebox.showinfo("Success", f"Pattern saved successfully!")
            logging.info(f"Exported pattern to {filename}")
        except Exception as e:
            logging.error(f"Failed to save pattern: {e}")
            messagebox.showerror("Error", f"Failed to save pattern.\n{str(e)}")
