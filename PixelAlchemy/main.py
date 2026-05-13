"""
Main entry point for PixelAlchemy.
Sets up the main Tkinter window, vibrant dark theme, and tabbed Notebook layout.
"""
import tkinter as tk
from tkinter import ttk
import logging
from modules import database
from modules.canvas_editor import CanvasEditor
from modules.filters_lab import FiltersLab
from modules.color_theory import ColorTheoryPanel
from modules.pattern_maker import PatternMaker
from modules.gallery import Gallery

# Define theme colors
BG_COLOR = "#1e1e2e"
FG_COLOR = "#cdd6f4"
ACCENT_BLUE = "#89b4fa"
ACCENT_PURPLE = "#cba6f7"
ACCENT_CYAN = "#89dceb"
ACCENT_ORANGE = "#fab387"
ACCENT_MAGENTA = "#f38ba8"

class PixelAlchemyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("PixelAlchemy")
        self.geometry("1100x700")
        self.minsize(1100, 700)
        self.configure(bg=BG_COLOR)
        
        # Initialize Database
        database.init_db()
        logging.info("Application started")
        
        self.setup_styles()
        self.create_header()
        self.create_notebook()
        self.create_status_bar()

    def setup_styles(self):
        """Sets up the custom dark theme with vibrant accents."""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Notebook style
        style.configure('TNotebook', background=BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab', 
                        background="#313244", 
                        foreground=FG_COLOR, 
                        padding=[15, 5], 
                        font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                  background=[('selected', ACCENT_BLUE)],
                  foreground=[('selected', '#11111b')])
        
        # Frame style
        style.configure('TFrame', background=BG_COLOR)
        
        # Button style
        style.configure('Accent.TButton', 
                        background=ACCENT_PURPLE, 
                        foreground='#11111b', 
                        font=('Segoe UI', 10, 'bold'),
                        padding=5)
        style.map('Accent.TButton',
                  background=[('active', ACCENT_MAGENTA)])

    def create_header(self):
        """Creates a vibrant gradient-style banner header."""
        header_frame = tk.Frame(self, bg=BG_COLOR, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        canvas = tk.Canvas(header_frame, height=80, bg=BG_COLOR, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Simple gradient simulation
        colors = ["#1e1e2e", "#313244", "#45475a", "#585b70"]
        for i in range(4):
            canvas.create_rectangle(0, i*20, 3000, (i+1)*20, fill=colors[i], outline="")
            
        # Vibrant text effect
        canvas.create_text(50, 40, text="Pixel", font=("Segoe UI", 32, "bold"), fill=ACCENT_CYAN, anchor=tk.W)
        canvas.create_text(165, 40, text="Alchemy", font=("Segoe UI", 32, "bold"), fill=ACCENT_ORANGE, anchor=tk.W)
        canvas.create_text(50, 65, text="Create, Filter, Learn, Generate", font=("Segoe UI", 10, "italic"), fill=FG_COLOR, anchor=tk.W)

    def create_notebook(self):
        """Creates the tabbed navigation for modules."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Instantiate modules
        self.canvas_frame = CanvasEditor(self.notebook)
        self.filters_frame = FiltersLab(self.notebook)
        self.theory_frame = ColorTheoryPanel(self.notebook)
        self.patterns_frame = PatternMaker(self.notebook)
        self.gallery_frame = Gallery(self.notebook)
        
        self.notebook.add(self.canvas_frame, text="🖌️ Canvas Editor")
        self.notebook.add(self.filters_frame, text="🎛️ Filters Lab")
        self.notebook.add(self.theory_frame, text="🎨 Color Theory")
        self.notebook.add(self.patterns_frame, text="✨ Pattern Maker")
        self.notebook.add(self.gallery_frame, text="🖼️ Gallery")
        
        # We will populate these frames in the respective modules

    def create_status_bar(self):
        """Creates a status bar at the bottom."""
        status_frame = tk.Frame(self, bg="#11111b", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg="#11111b", fg=FG_COLOR, font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    app = PixelAlchemyApp()
    app.mainloop()
