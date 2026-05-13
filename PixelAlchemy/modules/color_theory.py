"""
Color Theory Module for PixelAlchemy.
Provides lessons, an interactive color wheel, and quizzes.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import math
import logging
from modules import database

class ColorTheoryPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # We use a nested notebook for lessons
        self.lessons_notebook = ttk.Notebook(self)
        self.lessons_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab_wheel = ttk.Frame(self.lessons_notebook)
        self.tab_basics = ttk.Frame(self.lessons_notebook)
        self.tab_schemes = ttk.Frame(self.lessons_notebook)
        self.tab_quiz = ttk.Frame(self.lessons_notebook)
        
        self.lessons_notebook.add(self.tab_wheel, text="🎨 Color Wheel")
        self.lessons_notebook.add(self.tab_basics, text="📚 Basics")
        self.lessons_notebook.add(self.tab_schemes, text="🌈 Schemes")
        self.lessons_notebook.add(self.tab_quiz, text="📝 Quiz")
        
        self.build_color_wheel()
        self.build_basics()
        self.build_schemes()
        self.build_quiz()

    def build_color_wheel(self):
        canvas = tk.Canvas(self.tab_wheel, bg="#1e1e2e", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Draw a simple color wheel
        colors = [
            "#ff0000", "#ff8000", "#ffff00", 
            "#80ff00", "#00ff00", "#00ff80", 
            "#00ffff", "#0080ff", "#0000ff", 
            "#8000ff", "#ff00ff", "#ff0080"
        ]
        
        # REVIEW: Designer B - The color wheel arcs look great, but maybe we can add a hover effect in v2?
        cx, cy = 300, 250
        r = 150
        angle = 360 / len(colors)
        
        for i, color in enumerate(colors):
            start = i * angle
            canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=angle, fill=color, outline="")
            
        # Center circle
        canvas.create_oval(cx-50, cy-50, cx+50, cy+50, fill="#1e1e2e", outline="")
        canvas.create_text(cx, cy, text="Color Wheel", fill="#cdd6f4", font=("Segoe UI", 12, "bold"))

    def build_basics(self):
        text = tk.Text(self.tab_basics, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 12), wrap=tk.WORD, borderwidth=0)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content = """Primary Colors: Red, Blue, Yellow. These cannot be made by mixing other colors.
        
Secondary Colors: Green, Orange, Purple. These are created by mixing two primary colors.

Tertiary Colors: Red-Orange, Yellow-Orange, Yellow-Green, Blue-Green, Blue-Purple, Red-Purple.

Warm vs Cool:
- Warm colors (Red, Orange, Yellow) evoke warmth and energy.
- Cool colors (Blue, Green, Purple) evoke calmness and peace."""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)

    def build_schemes(self):
        text = tk.Text(self.tab_schemes, bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 12), wrap=tk.WORD, borderwidth=0)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content = """Complementary: Colors opposite each other on the color wheel (e.g., Red and Green). High contrast.

Analogous: Colors next to each other on the color wheel (e.g., Red, Red-Orange, Orange). Harmonious.

Triadic: Three colors evenly spaced around the color wheel (e.g., Red, Yellow, Blue). Vibrant."""
        
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)

    def build_quiz(self):
        self.quiz_score = 0
        
        ttk.Label(self.tab_quiz, text="Color Theory Quiz", font=("Segoe UI", 16, "bold"), foreground="#89b4fa", background="#1e1e2e").pack(pady=20)
        
        # Q1
        ttk.Label(self.tab_quiz, text="1. What do you get when you mix Red and Yellow?", foreground="#cdd6f4", background="#1e1e2e").pack(anchor=tk.W, padx=20)
        self.q1_var = tk.StringVar(value="")
        for opt in ["Orange", "Green", "Purple"]:
            tk.Radiobutton(self.tab_quiz, text=opt, variable=self.q1_var, value=opt, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244").pack(anchor=tk.W, padx=40)
            
        # Q2
        ttk.Label(self.tab_quiz, text="2. Which scheme uses opposite colors?", foreground="#cdd6f4", background="#1e1e2e").pack(anchor=tk.W, padx=20, pady=(10,0))
        self.q2_var = tk.StringVar(value="")
        for opt in ["Analogous", "Complementary", "Triadic"]:
            tk.Radiobutton(self.tab_quiz, text=opt, variable=self.q2_var, value=opt, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244").pack(anchor=tk.W, padx=40)
            
        # Q3
        ttk.Label(self.tab_quiz, text="3. Which of these is a cool color?", foreground="#cdd6f4", background="#1e1e2e").pack(anchor=tk.W, padx=20, pady=(10,0))
        self.q3_var = tk.StringVar(value="")
        for opt in ["Red", "Orange", "Blue"]:
            tk.Radiobutton(self.tab_quiz, text=opt, variable=self.q3_var, value=opt, bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244").pack(anchor=tk.W, padx=40)
            
        ttk.Button(self.tab_quiz, text="Submit Quiz", command=self.submit_quiz).pack(pady=20)

    def submit_quiz(self):
        score = 0
        if self.q1_var.get() == "Orange": score += 1
        if self.q2_var.get() == "Complementary": score += 1
        if self.q3_var.get() == "Blue": score += 1
        
        messagebox.showinfo("Quiz Result", f"You scored {score}/3!")
        
        # Save to DB
        success = database.save_quiz_score("Color Theory 101", score)
        if success:
            logging.info(f"Quiz score {score}/3 saved to DB.")
        else:
            messagebox.showwarning("Database Error", "Failed to save quiz score.")
