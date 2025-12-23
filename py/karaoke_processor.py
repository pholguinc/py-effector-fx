"""
Procesador de Karaoke para ASS
Parsea timing {\k##} y calcula posiciones de sílabas/caracteres
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Syllable:
    """Representa una sílaba con su timing y posición"""
    text: str
    duration: int  # en centésimas de segundo (como {\k##})
    start_time: int  # ms desde inicio de línea
    end_time: int  # ms
    x: float  # posición X
    y: float  # posición Y
    index: int  # índice de la sílaba
    char_index: int  # índice del primer caracter


@dataclass 
class KaraokeLine:
    """Representa una línea de karaoke procesada"""
    layer: int
    start_time: str  # formato 0:00:00.00
    end_time: str
    style: str
    name: str
    margin_l: int
    margin_r: int
    margin_v: int
    effect: str
    text: str
    syllables: List[Syllable]
    duration: int  # duración total en ms


class KaraokeProcessor:
    """Procesa líneas de karaoke y extrae sílabas con timing"""
    
    # Ancho aproximado de caracteres (monospace aproximado)
    CHAR_WIDTHS = {
        'default': 0.55,  # factor de fontsize
        'narrow': 0.4,    # i, l, etc.
        'wide': 0.7,      # m, w, etc.
    }
    
    NARROW_CHARS = set('iIlL1|!.,;:\'"')
    WIDE_CHARS = set('mMwWæœ')
    
    def __init__(self, fontsize: int = 48, line_y: float = 29):
        self.fontsize = fontsize
        self.line_y = line_y
        self.margin_left = 10
    
    def parse_time(self, time_str: str) -> int:
        """Convertir tiempo ASS (0:00:00.00) a milisegundos"""
        match = re.match(r'(\d+):(\d+):(\d+)\.(\d+)', time_str)
        if match:
            h, m, s, cs = map(int, match.groups())
            return (h * 3600 + m * 60 + s) * 1000 + cs * 10
        return 0
    
    def format_time(self, ms: int) -> str:
        """Convertir milisegundos a formato ASS (0:00:00.00)"""
        if ms < 0:
            ms = 0
        cs = (ms % 1000) // 10
        s = (ms // 1000) % 60
        m = (ms // 60000) % 60
        h = ms // 3600000
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
    
    def estimate_char_width(self, char: str) -> float:
        """Estimar ancho de un caracter"""
        if char in self.NARROW_CHARS:
            return self.fontsize * self.CHAR_WIDTHS['narrow']
        elif char in self.WIDE_CHARS:
            return self.fontsize * self.CHAR_WIDTHS['wide']
        elif char == ' ':
            return self.fontsize * 0.3
        else:
            return self.fontsize * self.CHAR_WIDTHS['default']
    
    def estimate_text_width(self, text: str) -> float:
        """Estimar ancho total de un texto"""
        return sum(self.estimate_char_width(c) for c in text)
    
    def parse_dialogue_line(self, line: str) -> Optional[KaraokeLine]:
        """Parsear una línea de diálogo ASS"""
        match = re.match(
            r'Dialogue:\s*(\d+),([^,]+),([^,]+),([^,]*),([^,]*),(\d+),(\d+),(\d+),([^,]*),(.*)',
            line
        )
        if not match:
            return None
        
        layer = int(match.group(1))
        start = match.group(2)
        end = match.group(3)
        style = match.group(4)
        name = match.group(5)
        margin_l = int(match.group(6))
        margin_r = int(match.group(7))
        margin_v = int(match.group(8))
        effect = match.group(9)
        text = match.group(10)
        
        start_ms = self.parse_time(start)
        end_ms = self.parse_time(end)
        
        syllables = self.extract_syllables(text, start_ms)
        
        return KaraokeLine(
            layer=layer,
            start_time=start,
            end_time=end,
            style=style,
            name=name,
            margin_l=margin_l,
            margin_r=margin_r,
            margin_v=margin_v,
            effect=effect,
            text=text,
            syllables=syllables,
            duration=end_ms - start_ms
        )
    
    def extract_syllables(self, text: str, line_start_ms: int) -> List[Syllable]:
        """Extraer sílabas con timing de una línea"""
        syllables = []
        
        # Patrón para encontrar {\k##} o {\K##} o {\kf##}
        pattern = r'\{[^}]*\\[kK]f?(\d+)[^}]*\}([^{]*)'
        
        current_time = 0  # en ms
        current_x = self.margin_left
        char_index = 0
        
        for i, match in enumerate(re.finditer(pattern, text)):
            duration_cs = int(match.group(1))  # centésimas de segundo
            syl_text = match.group(2)
            
            if not syl_text.strip():
                continue
            
            duration_ms = duration_cs * 10
            
            syl_width = self.estimate_text_width(syl_text)
            
            syllable = Syllable(
                text=syl_text,
                duration=duration_cs,
                start_time=current_time,
                end_time=current_time + duration_ms,
                x=current_x + syl_width / 2,  # centro de la sílaba
                y=self.line_y,
                index=i,
                char_index=char_index
            )
            
            syllables.append(syllable)
            
            current_time += duration_ms
            current_x += syl_width
            char_index += len(syl_text)
        
        return syllables
    
    def get_clean_text(self, text: str) -> str:
        """Obtener texto sin tags"""
        return re.sub(r'\{[^}]*\}', '', text)


def process_karaoke_line(line: str, fontsize: int = 48, line_y: float = 29) -> Optional[KaraokeLine]:
    """Función helper para procesar una línea"""
    processor = KaraokeProcessor(fontsize, line_y)
    return processor.parse_dialogue_line(line)
