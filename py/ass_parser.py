"""Módulo para parsear archivos ASS de Aegisub"""

import re
from typing import List, Dict, Optional


class ASSParser:
    """Parser para archivos ASS de subtítulos"""
    
    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.styles: List[Dict] = []
        self.script_info: Dict = {}
        
        if filepath:
            self.parse(filepath)
    
    def parse(self, filepath: str) -> None:
        """Parsear un archivo ASS"""
        self.filepath = filepath
        self.styles = []
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        
        self._parse_styles(content)
    
    def _parse_styles(self, content: str) -> None:
        """Extraer estilos de la sección [V4+ Styles]"""
        # Buscar la sección de estilos
        style_section = re.search(r'\[V4\+? Styles\](.*?)(?=\[|\Z)', content, re.DOTALL | re.IGNORECASE)
        
        if not style_section:
            return
        
        section_content = style_section.group(1)
        lines = section_content.strip().split('\n')
        
        format_fields = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('Format:'):
                # Obtener campos del formato
                format_str = line[7:].strip()
                format_fields = [f.strip() for f in format_str.split(',')]
            
            elif line.startswith('Style:'):
                # Parsear estilo
                style_str = line[6:].strip()
                values = [v.strip() for v in style_str.split(',')]
                
                if format_fields and len(values) >= len(format_fields):
                    style = {}
                    for i, field in enumerate(format_fields):
                        style[field] = values[i] if i < len(values) else ''
                    self.styles.append(style)
    
    def get_style_names(self) -> List[str]:
        """Obtener lista de nombres de estilos"""
        return [style.get('Name', '') for style in self.styles if style.get('Name')]
    
    def get_style(self, name: str) -> Optional[Dict]:
        """Obtener un estilo por nombre"""
        for style in self.styles:
            if style.get('Name') == name:
                return style
        return None


def parse_ass_file(filepath: str) -> ASSParser:
    """Función helper para parsear un archivo ASS"""
    return ASSParser(filepath)


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        parser = ASSParser(sys.argv[1])
        print("Estilos encontrados:")
        for name in parser.get_style_names():
            print(f"  - {name}")
