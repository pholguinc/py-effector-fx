"""Página de efectos Lead Out"""

import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from effects import KaraokeEffects, get_available_effects


class LeadOutPage(BasePage):
    """Configuración de efectos de salida"""
    
    def create_widgets(self):
        self.create_back_button()
        
        tk.Label(self, text="⏪ Lead Out", font=("Segoe UI", 20, "bold"),
            fg="#f38ba8", bg="#1e1e2e").pack(pady=15)
        
        tk.Label(self, text="Efectos de salida para karaoke",
            font=("Segoe UI", 11), fg="#cdd6f4", bg="#1e1e2e").pack()
        
        # Frame para opciones
        options_frame = tk.Frame(self, bg="#1e1e2e")
        options_frame.pack(pady=20)
        
        # Selector de efecto
        tk.Label(options_frame, text="Efecto:", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        
        self.effect_var = tk.StringVar(value="Fade Out")
        effects = get_available_effects("lead_out")
        ttk.Combobox(options_frame, textvariable=self.effect_var,
            values=effects, state="readonly", font=("Segoe UI", 10), 
            width=20).grid(row=0, column=1, padx=10, pady=8)
        
        # Duración
        tk.Label(options_frame, text="Duración (ms):", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        
        self.duration_var = tk.StringVar(value="300")
        tk.Entry(options_frame, textvariable=self.duration_var, font=("Segoe UI", 10),
            width=22, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=1, column=1, padx=10, pady=8)
        
        # Preview del efecto
        tk.Label(self, text="Preview del tag:", font=("Segoe UI", 10),
            fg="#6c7086", bg="#1e1e2e").pack(pady=(20, 5))
        
        self.preview_label = tk.Label(self, text="", font=("Consolas", 10),
            fg="#f38ba8", bg="#313244", padx=10, pady=5, wraplength=500)
        self.preview_label.pack(padx=20)
        
        # Actualizar preview
        self.effect_var.trace('w', lambda *args: self.update_preview())
        self.duration_var.trace('w', lambda *args: self.update_preview())
        self.update_preview()
        
        # Frame para botones
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=25)
        
        tk.Button(btn_frame, text="✓ Aplicar Efecto", command=self.aplicar,
            font=("Segoe UI", 11, "bold"), fg="#1e1e2e", bg="#f38ba8",
            padx=20, pady=8).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="📋 Copiar Tag", command=self.copiar_tag,
            font=("Segoe UI", 10), fg="#cdd6f4", bg="#45475a",
            padx=15, pady=8).pack(side="left", padx=10)
    
    def update_preview(self):
        try:
            duration = int(self.duration_var.get())
        except:
            duration = 300
        
        colors = getattr(self.controller, 'colors', None)
        effects = KaraokeEffects(colors=colors)
        tag = effects.generate_lead_out(self.effect_var.get(), duration)
        self.preview_label.config(text=tag)
    
    def copiar_tag(self):
        tag = self.preview_label.cget("text")
        self.controller.root.clipboard_clear()
        self.controller.root.clipboard_append(tag)
        self.preview_label.config(text=tag + " ✓ Copiado!")
        self.after(1500, self.update_preview)
    
    def aplicar(self):
        try:
            duration = int(self.duration_var.get())
        except:
            duration = 300
        
        colors = getattr(self.controller, 'colors', None)
        effects = KaraokeEffects(
            colors=colors,
            border_size=int(getattr(self.controller, 'border_size', 2)),
            shadow_size=int(getattr(self.controller, 'shadow_size', 2))
        )
        
        tag = effects.generate_lead_out(self.effect_var.get(), duration)
        color_tag = effects.apply_colors()
        full_tag = tag + color_tag
        
        result_file = "/tmp/aegisub_effect_result.txt"
        with open(result_file, 'w') as f:
            f.write(f"EFFECT_TYPE:lead_out\n")
            f.write(f"EFFECT_NAME:{self.effect_var.get()}\n")
            f.write(f"DURATION:{duration}\n")
            f.write(f"TAG:{full_tag}\n")
        
        print(f"Lead Out aplicado: {full_tag}")
        self.controller.root.destroy()
