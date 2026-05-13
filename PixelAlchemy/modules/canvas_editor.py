"""
Canvas Editor Module for PixelAlchemy.
Provides grid-based pixel drawing with tools, undo/redo, and saving functionality.
"""
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, simpledialog
from PIL import Image, ImageDraw
import logging
from modules import database
import os

class CanvasEditor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_size = 32
        self.pixel_size = 15
        self.current_color = "#ffffff"
        self.current_tool = "pencil"
        self.history = []
        self.redo_stack = []
        self.max_history = 20
        
        # Grid state: (col, row) -> color
        self.pixels = {} 
        self.rect_ids = {} # (col, row) -> canvas item id
        
        self.setup_ui()
        self.init_grid()
        self.save_state()

    def setup_ui(self):
        """Sets up the toolbar and the drawing canvas."""
        # Toolbar
        self.toolbar = tk.Frame(self, bg="#313244", width=80)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Tools
        tools = [
            ("Pencil", "pencil", "#89b4fa"),
            ("Eraser", "eraser", "#f38ba8"),
            ("Fill", "fill", "#a6e3a1"),
            ("Picker", "picker", "#f9e2af")
        ]
        
        for name, tool_id, color in tools:
            btn = tk.Button(self.toolbar, text=name, bg=color, fg="#11111b", 
                            font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                            command=lambda t=tool_id: self.select_tool(t))
            btn.pack(fill=tk.X, pady=5, padx=5)
            
        # Color preview button
        self.color_btn = tk.Button(self.toolbar, bg=self.current_color, relief=tk.RAISED,
                                   command=self.choose_color, height=2)
        self.color_btn.pack(fill=tk.X, pady=15, padx=5)
        
        # Grid Size Control
        self.size_var = tk.IntVar(value=32)
        ttk.Label(self.toolbar, text="Size:", background="#313244", foreground="#cdd6f4").pack(pady=(10,0))
        size_scale = ttk.Scale(self.toolbar, from_=16, to=64, variable=self.size_var, 
                               orient=tk.HORIZONTAL, command=self.update_size)
        size_scale.pack(fill=tk.X, padx=5)
        
        # Actions
        ttk.Button(self.toolbar, text="Undo", command=self.undo).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.toolbar, text="Redo", command=self.redo).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas).pack(fill=tk.X, pady=2, padx=5)
        ttk.Button(self.toolbar, text="Save Art", command=self.save_artwork).pack(fill=tk.X, pady=20, padx=5)
        
        # Canvas Frame
        self.canvas_frame = tk.Frame(self, bg="#1e1e2e")
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#11111b", highlightthickness=2, 
                                highlightbackground="#cba6f7", highlightcolor="#cba6f7")
        self.canvas.pack(expand=True)
        
        # Events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.save_state())

    def update_size(self, val):
        new_size = int(float(val))
        if new_size != self.grid_size:
            self.grid_size = new_size
            self.init_grid()
            self.save_state()

    def select_tool(self, tool):
        self.current_tool = tool

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color
            self.color_btn.config(bg=color)
            self.current_tool = "pencil"

    def init_grid(self):
        self.canvas.delete("all")
        self.pixels.clear()
        self.rect_ids.clear()
        
        canvas_width = self.grid_size * self.pixel_size
        self.canvas.config(width=canvas_width, height=canvas_width)
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.pixel_size
                y1 = row * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="#313244")
                self.rect_ids[(col, row)] = rect

    def paint(self, event):
        col = event.x // self.pixel_size
        row = event.y // self.pixel_size
        
        if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
            if self.current_tool == "pencil":
                self.set_pixel(col, row, self.current_color)
            elif self.current_tool == "eraser":
                self.set_pixel(col, row, "")
            elif self.current_tool == "fill":
                self.flood_fill(col, row, self.pixels.get((col, row), ""), self.current_color)
            elif self.current_tool == "picker":
                color = self.pixels.get((col, row), "")
                if color:
                    self.current_color = color
                    self.color_btn.config(bg=color)
                    self.current_tool = "pencil"

    def set_pixel(self, col, row, color):
        if self.pixels.get((col, row), "") != color:
            self.pixels[(col, row)] = color
            rect_id = self.rect_ids.get((col, row))
            if rect_id:
                self.canvas.itemconfig(rect_id, fill=color)

    def flood_fill(self, x, y, target_color, replacement_color):
        if target_color == replacement_color:
            return
            
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self.pixels.get((cx, cy), "") == target_color:
                self.set_pixel(cx, cy, replacement_color)
                if cx > 0: stack.append((cx - 1, cy))
                if cx < self.grid_size - 1: stack.append((cx + 1, cy))
                if cy > 0: stack.append((cx, cy - 1))
                if cy < self.grid_size - 1: stack.append((cx, cy + 1))

    def clear_canvas(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.set_pixel(col, row, "")
        self.save_state()

    def save_state(self):
        state = self.pixels.copy()
        if not self.history or self.history[-1] != state:
            self.history.append(state)
            if len(self.history) > self.max_history:
                self.history.pop(0)
            self.redo_stack.clear()

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.restore_state(self.history[-1])

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.history.append(state)
            self.restore_state(state)

    def restore_state(self, state):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = state.get((col, row), "")
                self.set_pixel(col, row, color)

    def save_artwork(self):
        title = simpledialog.askstring("Save Artwork", "Enter a title for your artwork:")
        if not title:
            return
            
        try:
            # Create image
            img_size = self.grid_size * self.pixel_size
            img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            for (col, row), color in self.pixels.items():
                if color:
                    x0 = col * self.pixel_size
                    y0 = row * self.pixel_size
                    draw.rectangle([x0, y0, x0 + self.pixel_size, y0 + self.pixel_size], fill=color)
            
            os.makedirs("saved_art", exist_ok=True)
            filename = f"saved_art/{title.replace(' ', '_')}.png"
            img.save(filename)
            
            # Save to db
            metadata = f"{self.grid_size}x{self.grid_size}"
            database.save_artwork(title, filename, "canvas", metadata)
            
            messagebox.showinfo("Success", f"Artwork '{title}' saved successfully!")
            logging.info(f"Exported canvas to {filename}")
        except Exception as e:
            logging.error(f"Failed to save artwork: {e}")
            messagebox.showerror("Error", f"Failed to save artwork.\n{str(e)}")
