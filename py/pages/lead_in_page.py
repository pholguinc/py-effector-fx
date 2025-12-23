"""Página de efectos Lead In con soporte multi-capa"""

import tkinter as tk
from tkinter import ttk
from pages.base_page import BasePage
from effects import KaraokeEffects, MultiLayerEffectGenerator, EffectConfig, get_available_effects


class LeadInPage(BasePage):
    """Configuración de efectos de entrada"""
    
    def create_widgets(self):
        self.create_back_button()
        
        tk.Label(self, text="⏩ Lead In", font=("Segoe UI", 18, "bold"),
            fg="#a6e3a1", bg="#1e1e2e").pack(pady=10)
        
        tk.Label(self, text="Efectos de entrada para karaoke",
            font=("Segoe UI", 10), fg="#cdd6f4", bg="#1e1e2e").pack()
        
        # Frame principal
        main_frame = tk.Frame(self, bg="#1e1e2e")
        main_frame.pack(pady=15, fill="x", padx=20)
        
        # Selector de efecto
        tk.Label(main_frame, text="Tipo de efecto:", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.effect_var = tk.StringVar(value="Multi-Layer")
        effects = get_available_effects("lead_in")
        ttk.Combobox(main_frame, textvariable=self.effect_var,
            values=effects, state="readonly", font=("Segoe UI", 10), 
            width=18).grid(row=0, column=1, padx=5, pady=5)
        
        # Duración de entrada
        tk.Label(main_frame, text="Duración entrada (ms):", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.entry_duration_var = tk.StringVar(value="400")
        tk.Entry(main_frame, textvariable=self.entry_duration_var, font=("Segoe UI", 10),
            width=20, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=1, column=1, padx=5, pady=5)
        
        # Duración de highlight
        tk.Label(main_frame, text="Duración highlight (ms):", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.highlight_duration_var = tk.StringVar(value="300")
        tk.Entry(main_frame, textvariable=self.highlight_duration_var, font=("Segoe UI", 10),
            width=20, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=2, column=1, padx=5, pady=5)
        
        # Fade out
        tk.Label(main_frame, text="Fade out (ms):", font=("Segoe UI", 11),
            fg="#cdd6f4", bg="#1e1e2e").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        self.fadeout_var = tk.StringVar(value="300")
        tk.Entry(main_frame, textvariable=self.fadeout_var, font=("Segoe UI", 10),
            width=20, bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4").grid(row=3, column=1, padx=5, pady=5)
        
        # Información
        info_text = """Capas generadas:
• Layer 1 (Main): Texto final con posición y fade out
• Layer 2 (Entry): Animación de entrada por caracter
• Layer 3 (Highlight): Efecto de resaltado karaoke"""
        
        tk.Label(self, text=info_text, font=("Segoe UI", 9),
            fg="#6c7086", bg="#1e1e2e", justify="left").pack(pady=10)
        
        # Frame para botones
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=15)
        
        # Botón aplicar
        tk.Button(btn_frame, text="✓ Aplicar Efecto", command=self.aplicar,
            font=("Segoe UI", 11, "bold"), fg="#1e1e2e", bg="#a6e3a1",
            padx=20, pady=8).pack(side="left", padx=10)
        
        # Botón cancelar
        tk.Button(btn_frame, text="Cancelar", command=self.cancelar,
            font=("Segoe UI", 10), fg="#cdd6f4", bg="#45475a",
            padx=15, pady=8).pack(side="left", padx=10)
    
    def cancelar(self):
        """Cerrar sin aplicar"""
        self.controller.root.destroy()
    
    def aplicar(self):
        """Aplicar efecto multi-capa"""
        try:
            entry_duration = int(self.entry_duration_var.get())
            highlight_duration = int(self.highlight_duration_var.get())
            fadeout_duration = int(self.fadeout_var.get())
        except:
            entry_duration = 400
            highlight_duration = 300
            fadeout_duration = 300
        
        # Obtener colores del controller
        colors = getattr(self.controller, 'colors', {
            "primary": "#FFFFFF",
            "secondary": "#000000",
            "border": "#FC76F2",
            "shadow": "#000000"
        })
        
        border_size = float(getattr(self.controller, 'border_size', 2))
        shadow_size = float(getattr(self.controller, 'shadow_size', 0))
        
        # Crear configuración
        config = EffectConfig(
            primary_color=colors.get("primary", "#FFFFFF"),
            border_color=colors.get("border", "#FC76F2"),
            shadow_color=colors.get("shadow", "#000000"),
            border_size=border_size,
            shadow_size=shadow_size,
            entry_duration=entry_duration,
            highlight_duration=highlight_duration,
            fade_out_duration=fadeout_duration,
            entry_type="random_rotate"
        )
        
        # Guardar configuración para Lua
        result_file = "/tmp/aegisub_effect_result.txt"
        
        # Obtener estilo seleccionado
        selected_style = getattr(self.controller, 'selected_style', '')
        
        with open(result_file, 'w') as f:
            f.write(f"EFFECT_TYPE:multi_layer\n")
            f.write(f"EFFECT_NAME:Multi-Layer Karaoke\n")
            f.write(f"SELECTED_STYLE:{selected_style}\n")
            f.write(f"ENTRY_DURATION:{entry_duration}\n")
            f.write(f"HIGHLIGHT_DURATION:{highlight_duration}\n")
            f.write(f"FADEOUT_DURATION:{fadeout_duration}\n")
            f.write(f"PRIMARY_COLOR:{colors.get('primary', '#FFFFFF')}\n")
            f.write(f"BORDER_COLOR:{colors.get('border', '#FC76F2')}\n")
            f.write(f"SHADOW_COLOR:{colors.get('shadow', '#000000')}\n")
            f.write(f"BORDER_SIZE:{border_size}\n")
            f.write(f"SHADOW_SIZE:{shadow_size}\n")
            f.write(f"BLUR:3\n")
        
        print(f"Multi-Layer effect configurado")
        
        # Cerrar ventana
        self.controller.root.destroy()
