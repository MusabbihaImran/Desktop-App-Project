"""
Gallery Module for PixelAlchemy.
Displays saved artworks, filters, and patterns in a grid.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import logging
from modules import database
import os

class Gallery(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.photos = [] # keep references
        self.setup_ui()

    def setup_ui(self):
        # Top bar
        top_bar = tk.Frame(self, bg="#313244", height=50)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        
        ttk.Button(top_bar, text="🔄 Refresh Gallery", command=self.load_gallery).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Scrollable Canvas
        self.canvas = tk.Canvas(self, bg="#1e1e2e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e2e")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.load_gallery()

    def load_gallery(self):
        # Clear existing
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.photos.clear()
        
        items = database.get_all_artworks()
        
        if not items:
            ttk.Label(self.scrollable_frame, text="No artworks found. Create something!", 
                      background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 12)).pack(pady=20, padx=20)
            return
            
        row = 0
        col = 0
        max_cols = 4
        
        # Border colors
        colors = {
            "canvas": "#cba6f7",  # Purple
            "filter": "#89dceb",  # Cyan
            "pattern": "#fab387"  # Orange
        }
        
        for item in items:
            db_id, title, img_path, item_type, meta = item
            
            frame_bg = colors.get(item_type, "#cdd6f4")
            
            card = tk.Frame(self.scrollable_frame, bg=frame_bg, bd=2, relief=tk.FLAT)
            card.grid(row=row, column=col, padx=15, pady=15)
            
            inner_card = tk.Frame(card, bg="#313244")
            inner_card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.thumbnail((150, 150))
                    photo = ImageTk.PhotoImage(img)
                    self.photos.append(photo)
                    
                    lbl_img = tk.Label(inner_card, image=photo, bg="#11111b")
                    lbl_img.pack(pady=(5,0), padx=5)
                else:
                    tk.Label(inner_card, text="Image Missing", bg="#11111b", fg="#f38ba8", width=20, height=10).pack(pady=(5,0), padx=5)
            except Exception as e:
                logging.error(f"Failed to load thumbnail {img_path}: {e}")
                
            tk.Label(inner_card, text=title, bg="#313244", fg="#cdd6f4", font=("Segoe UI", 10, "bold")).pack(pady=2)
            tk.Label(inner_card, text=f"Type: {item_type}", bg="#313244", fg="#a6adc8", font=("Segoe UI", 8)).pack()
            
            # Action buttons
            btn_frame = tk.Frame(inner_card, bg="#313244")
            btn_frame.pack(fill=tk.X, pady=5)
            
            ttk.Button(btn_frame, text="Delete", 
                       command=lambda i=db_id: self.delete_item(i)).pack(side=tk.RIGHT, padx=5)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def delete_item(self, item_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this artwork?"):
            database.delete_artwork(item_id)
            self.load_gallery()
