#!/usr/bin/env python3
"""
Py Effector FX - Generador de efectos para Aegisub
Punto de entrada principal de la aplicación
"""

import sys
import tkinter as tk
import subprocess
from pages import MainPage, LeadInPage, LeadOutPage, ShapePage, TranslationPage
from ass_parser import ASSParser


class EffectorApp:
    """Controlador principal de la aplicación"""
    
    def __init__(self, ass_file: str = None):
        self.root = tk.Tk()
        self.root.title("Py Effector FX")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        # Parsear archivo ASS si se proporciona
        self.ass_parser = None
        self.available_styles = ["Default"]
        
        if ass_file:
            try:
                self.ass_parser = ASSParser(ass_file)
                styles = self.ass_parser.get_style_names()
                if styles:
                    self.available_styles = styles
            except Exception as e:
                print(f"Error parseando ASS: {e}")
        
        # Centrar ventana en la pantalla
        self.center_window()
        
        # Container para todas las páginas
        self.container = tk.Frame(self.root, bg="#1e1e2e")
        self.container.pack(fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Registro de páginas
        self.pages = {}
        self._register_pages()
        
        # Mostrar página principal
        self.show_page("MainPage")
        
        # Forzar foco en el escritorio actual (macOS)
        self.root.after(50, self.focus_window)
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 600
        height = 450
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def focus_window(self):
        """Forzar foco en la ventana actual"""
        try:
            subprocess.run(['osascript', '-e', 
                'tell application "System Events" to set frontmost of process "Python" to true'], 
                capture_output=True)
        except:
            pass
        self.root.lift()
        self.root.focus_force()
    
    def _register_pages(self):
        """Registrar todas las páginas de la aplicación"""
        page_classes = [
            MainPage,
            LeadInPage,
            LeadOutPage,
            ShapePage,
            TranslationPage
        ]
        
        for PageClass in page_classes:
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")
    
    def show_page(self, page_name):
        """Mostrar una página por su nombre"""
        page = self.pages[page_name]
        page.tkraise()
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


def main():
    # Obtener archivo ASS de argumentos si existe
    ass_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = EffectorApp(ass_file)
    app.run()


if __name__ == "__main__":
    main()
