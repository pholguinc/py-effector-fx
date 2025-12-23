"""Clase base para todas las páginas"""

import tkinter as tk
from tkinter import colorchooser


class BasePage(tk.Frame):
    """Clase base que todas las páginas deben heredar"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#1e1e2e")
        self.controller = controller
        self.colors = {
            "primary": "#FFFFFF",
            "secondary": "#000000",
            "border": "#000000",
            "shadow": "#000000"
        }
        self.color_buttons = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Método a implementar por cada página"""
        raise NotImplementedError("Subclases deben implementar create_widgets()")
    
    def create_back_button(self):
        """botón de volver a la página principal"""
        btn = tk.Button(
            self, 
            text="← Volver", 
            command=lambda: self.controller.show_page("MainPage"),
            font=("Segoe UI", 10), 
            fg="#cdd6f4", 
            bg="#313244", 
            padx=15, 
            pady=5
        )
        btn.pack(anchor="nw", padx=20, pady=15)
    
    def create_color_controls(self, parent):
        """Crear controles de colores y tamaño"""
        frame = tk.Frame(parent, bg="#1e1e2e")
        frame.pack(pady=15)
        
        # Tamaño
        size_frame = tk.Frame(frame, bg="#1e1e2e")
        size_frame.pack(pady=5)
        
        tk.Label(size_frame, text="Tamaño:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").pack(side="left", padx=5)
        
        self.size_var = tk.StringVar(value="48")
        tk.Entry(size_frame, textvariable=self.size_var, font=("Segoe UI", 10), 
            width=10, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").pack(side="left", padx=5)
        
        # Colores
        color_frame = tk.Frame(frame, bg="#1e1e2e")
        color_frame.pack(pady=10)
        
        color_labels = [
            ("Primary", "primary"),
            ("Secondary", "secondary"),
            ("Border", "border"),
            ("Shadow", "shadow")
        ]
        
        for i, (label, key) in enumerate(color_labels):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(color_frame, text=label + ":", font=("Segoe UI", 10), 
                fg="#cdd6f4", bg="#1e1e2e").grid(row=row, column=col, sticky="w", padx=5, pady=5)
            
            btn = tk.Button(color_frame, width=6, bg=self.colors[key],
                command=lambda k=key: self.pick_color(k))
            btn.grid(row=row, column=col+1, padx=5, pady=5)
            self.color_buttons[key] = btn
        
        return frame
    
    def pick_color(self, key):
        """Abrir selector de color"""
        color = colorchooser.askcolor(color=self.colors[key], title=f"Seleccionar {key}")
        if color[1]:
            self.colors[key] = color[1]
            self.color_buttons[key].configure(bg=color[1])
