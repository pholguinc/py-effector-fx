"""Página de efectos Shape"""

import tkinter as tk
from pages.base_page import BasePage


class ShapePage(BasePage):
    """Configuración de formas y figuras"""
    
    def create_widgets(self):
        self.create_back_button()
        
        tk.Label(self, text="🔷 Shape", font=("Segoe UI", 20, "bold"),
            fg="#89b4fa", bg="#1e1e2e").pack(pady=30)
        
        tk.Label(self, text="Configuración de formas y figuras",
            font=("Segoe UI", 11), fg="#cdd6f4", bg="#1e1e2e").pack()
        
        # Botón aplicar
        tk.Button(self, text="Aplicar", command=self.aplicar,
            font=("Segoe UI", 11, "bold"), fg="#1e1e2e", bg="#89b4fa",
            padx=25, pady=6).pack(pady=40)
    
    def aplicar(self):
        print(f"Shape aplicado")
