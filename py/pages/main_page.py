"""Página principal con selección de tipo de efecto"""

import tkinter as tk
from tkinter import ttk, colorchooser
from pages.base_page import BasePage


class MainPage(BasePage):
    """Página de inicio con selección de tipo de efecto y estilo"""
    
    def create_widgets(self):
        # Título
        tk.Label(
            self, 
            text="✨ Py Effector FX",
            font=("Segoe UI", 18, "bold"), 
            fg="#cba6f7", 
            bg="#1e1e2e"
        ).pack(pady=(15, 5))
        
        tk.Label(
            self, 
            text="Generador de efectos para Aegisub",
            font=("Segoe UI", 10), 
            fg="#a6adc8", 
            bg="#1e1e2e"
        ).pack(pady=(0, 15))
        
        # Frame para los combos
        form_frame = tk.Frame(self, bg="#1e1e2e")
        form_frame.pack(pady=5)
        
        # Tipo de efecto
        tk.Label(form_frame, text="Tipo de efecto:", font=("Segoe UI", 11), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        
        self.tipo_var = tk.StringVar(value="Lead In")
        ttk.Combobox(form_frame, textvariable=self.tipo_var,
            values=["Lead In", "Lead Out", "Shape", "Translation"],
            state="readonly", font=("Segoe UI", 10), width=20).grid(row=0, column=1, padx=10, pady=8)
        
        # Estilo (desde el archivo ASS)
        tk.Label(form_frame, text="Estilo:", font=("Segoe UI", 11), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        
        # Obtener estilos disponibles del controller
        available_styles = getattr(self.controller, 'available_styles', ["Default"])
        self.estilo_var = tk.StringVar(value=available_styles[0] if available_styles else "Default")
        self.estilo_combo = ttk.Combobox(form_frame, textvariable=self.estilo_var,
            values=available_styles,
            state="readonly", font=("Segoe UI", 10), width=20)
        self.estilo_combo.grid(row=1, column=1, padx=10, pady=8)
        
        # Tamaño
        tk.Label(form_frame, text="Tamaño:", font=("Segoe UI", 11), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        
        self.size_var = tk.StringVar(value="48")
        tk.Entry(form_frame, textvariable=self.size_var, font=("Segoe UI", 10), 
            width=22, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=2, column=1, padx=10, pady=8)
        
        # Frame para colores
        color_frame = tk.Frame(self, bg="#1e1e2e")
        color_frame.pack(pady=10)
        
        # Inicializar colores
        self.colors = {
            "primary": "#FFFFFF",
            "secondary": "#000000",
            "border": "#000000",
            "shadow": "#000000"
        }
        self.color_labels = {}
        
        # Primary y Secondary (fila 0)
        tk.Label(color_frame, text="Primary:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        color_box = tk.Frame(color_frame, width=50, height=25, bg=self.colors["primary"],
            relief="solid", borderwidth=1, cursor="hand2")
        color_box.grid(row=0, column=1, padx=5, pady=5)
        color_box.pack_propagate(False)
        color_box.bind("<Button-1>", lambda e: self.pick_color("primary"))
        self.color_labels["primary"] = color_box
        
        tk.Label(color_frame, text="Secondary:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        color_box = tk.Frame(color_frame, width=50, height=25, bg=self.colors["secondary"],
            relief="solid", borderwidth=1, cursor="hand2")
        color_box.grid(row=0, column=3, padx=5, pady=5)
        color_box.pack_propagate(False)
        color_box.bind("<Button-1>", lambda e: self.pick_color("secondary"))
        self.color_labels["secondary"] = color_box
        
        # Border color (fila 1)
        tk.Label(color_frame, text="Border:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        color_box = tk.Frame(color_frame, width=50, height=25, bg=self.colors["border"],
            relief="solid", borderwidth=1, cursor="hand2")
        color_box.grid(row=1, column=1, padx=5, pady=5)
        color_box.pack_propagate(False)
        color_box.bind("<Button-1>", lambda e: self.pick_color("border"))
        self.color_labels["border"] = color_box
        
        # Shadow color (fila 1, columna 2-3)
        tk.Label(color_frame, text="Shadow:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        color_box = tk.Frame(color_frame, width=50, height=25, bg=self.colors["shadow"],
            relief="solid", borderwidth=1, cursor="hand2")
        color_box.grid(row=1, column=3, padx=5, pady=5)
        color_box.pack_propagate(False)
        color_box.bind("<Button-1>", lambda e: self.pick_color("shadow"))
        self.color_labels["shadow"] = color_box
        
        # Border size (fila 2, debajo de Border) 
        tk.Label(color_frame, text="Border size:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.border_size_var = tk.StringVar(value="2")
        tk.Entry(color_frame, textvariable=self.border_size_var, font=("Segoe UI", 10), 
            width=8, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=2, column=1, padx=5, pady=5)
        
        # Shadow size (fila 2, debajo de Shadow)
        tk.Label(color_frame, text="Shadow size:", font=("Segoe UI", 10), 
            fg="#cdd6f4", bg="#1e1e2e").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.shadow_size_var = tk.StringVar(value="2")
        tk.Entry(color_frame, textvariable=self.shadow_size_var, font=("Segoe UI", 10), 
            width=8, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=2, column=3, padx=5, pady=5)
        
        # Botón continuar
        tk.Button(self, text="Continuar →", command=self.navegar,
            font=("Segoe UI", 11, "bold"), fg="#1e1e2e", bg="#a6e3a1",
            activebackground="#94e2d5", padx=25, pady=6).pack(pady=15)
    
    def pick_color(self, key):
        """Abrir selector de color y actualizar"""
        result = colorchooser.askcolor(color=self.colors[key], title=f"Seleccionar {key}")
        if result[1]:
            self.colors[key] = result[1]
            self.color_labels[key].configure(bg=result[1])
    
    def navegar(self):
        """Navegar a la página seleccionada"""
        tipo_map = {
            "Lead In": "LeadInPage",
            "Lead Out": "LeadOutPage",
            "Shape": "ShapePage",
            "Translation": "TranslationPage"
        }
        page_name = tipo_map.get(self.tipo_var.get(), "LeadInPage")
        
        # Guardar configuración
        self.controller.selected_style = self.estilo_var.get()
        self.controller.size = self.size_var.get()
        self.controller.colors = self.colors.copy()
        self.controller.border_size = self.border_size_var.get()
        self.controller.shadow_size = self.shadow_size_var.get()
        
        self.controller.show_page(page_name)
