"""Página de efectos Translation"""

import tkinter as tk
from pages.base_page import BasePage


class TranslationPage(BasePage):
    """Configuración de movimientos y traslaciones"""
    
    def create_widgets(self):
        self.create_back_button()
        
        tk.Label(self, text="↔️ Translation", font=("Segoe UI", 20, "bold"),
            fg="#fab387", bg="#1e1e2e").pack(pady=30)
        
        tk.Label(self, text="Configuración de movimientos",
            font=("Segoe UI", 11), fg="#cdd6f4", bg="#1e1e2e").pack()
        
        # Aquí va la lógica específica de Translation
        
        # Botón aplicar
        tk.Button(self, text="Aplicar", command=self.aplicar,
            font=("Segoe UI", 11, "bold"), fg="#1e1e2e", bg="#fab387",
            padx=25, pady=6).pack(pady=40)
    
    def aplicar(self):
        print(f"Translation aplicado")
