"""
Generador de efectos multi-capa para karaoke ASS
"""

import re
import random
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from karaoke_processor import KaraokeLine, Syllable, KaraokeProcessor


@dataclass
class EffectConfig:
    """Configuración de efectos"""
    # Colores (formato HEX)
    primary_color: str = "#FFFFFF"
    secondary_color: str = "#000000"
    border_color: str = "#FC76F2"
    shadow_color: str = "#000000"
    highlight_border_color: str = "#FFD9C5"
    highlight_shadow_color: str = "#FFB792"
    
    # Tamaños
    border_size: float = 2
    shadow_size: float = 0
    blur: float = 3
    
    # Animaciones
    entry_duration: int = 400  # ms
    highlight_duration: int = 300  # ms
    fade_out_duration: int = 300  # ms
    
    # Tipo de entrada
    entry_type: str = "random_rotate"  # random_rotate, fly_in, scale_in
    
    # Highlight
    highlight_scale_x: int = 135
    highlight_scale_y: int = 150
    highlight_rotation: int = 10
    highlight_perspective_y: int = -40
    highlight_perspective_x: int = -30


class MultiLayerEffectGenerator:
    """Generador de efectos de 3 capas para karaoke"""
    
    def __init__(self, config: EffectConfig = None):
        self.config = config or EffectConfig()
        self.processor = KaraokeProcessor()
    
    def hex_to_ass(self, hex_color: str) -> str:
        """Convertir HEX a formato ASS (&HBBGGRR&)"""
        hex_color = hex_color.lstrip('#')
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"&H00{b}{g}{r}&"
    
    def get_base_tags(self) -> str:
        """Tags base de colores"""
        return (
            f"\\blur{self.config.blur}"
            f"\\bord{self.config.border_size}"
            f"\\shad{self.config.shadow_size}"
            f"\\3c{self.hex_to_ass(self.config.border_color)}"
            f"\\c{self.hex_to_ass(self.config.primary_color)}"
        )
    
    def get_random_entry_position(self, x: float, y: float, distance: int = 50) -> Tuple[float, float]:
        """Generar posición aleatoria de entrada"""
        angle = random.uniform(0, 2 * math.pi)
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)
        return (x + dx, y + dy)
    
    def generate_layer1_main(self, syl: Syllable, line: KaraokeLine, line_end_ms: int) -> str:
        """
        Layer 1: Texto final (aparece después del highlight, permanece hasta el final)
        """
        # Tiempo: desde que termina el highlight hasta el final de la línea
        start_ms = int(syl.start_time + self.config.highlight_duration)
        
        start_time = self.processor.format_time(start_ms)
        end_time = line.end_time
        
        tags = (
            f"{{\\an5\\pos({syl.x:.0f},{syl.y:.0f})"
            f"\\fad(0,{self.config.fade_out_duration})"
            f"{self.get_base_tags()}}}"
        )
        
        return (
            f"Dialogue: 1,{start_time},{end_time},{line.style},,0,0,0,fx,"
            f"{tags}{syl.text}"
        )
    
    def generate_layer2_entry(self, syl: Syllable, line: KaraokeLine) -> List[str]:
        """
        Layer 2: Animación de entrada (cada caracter vuela hacia su posición)
        """
        lines = []
        
        # Tiempo: desde antes del inicio de la sílaba
        entry_start = max(0, syl.start_time - self.config.entry_duration)
        
        # Calcular posición de cada caracter
        char_x = syl.x - self.processor.estimate_text_width(syl.text) / 2
        
        for char in syl.text:
            if char.strip():  # Ignorar espacios
                char_width = self.processor.estimate_char_width(char)
                char_center_x = char_x + char_width / 2
                
                # Posición de entrada aleatoria
                entry_x, entry_y = self.get_random_entry_position(char_center_x, syl.y)
                
                # Rotación aleatoria
                start_rotation = random.randint(-360, 360)
                
                start_time = self.processor.format_time(int(entry_start))
                end_time = self.processor.format_time(int(syl.start_time))
                
                tags = (
                    f"{{{self.get_base_tags()}"
                    f"\\an5\\move({entry_x:.0f},{entry_y:.0f},{char_center_x:.0f},{syl.y:.0f},0,{self.config.entry_duration})"
                    f"\\fad({self.config.entry_duration},0)"
                    f"\\frz{start_rotation}"
                    f"\\t(0,{self.config.entry_duration},\\frz0)}}"
                )
                
                lines.append(
                    f"Dialogue: 2,{start_time},{end_time},{line.style},,0,0,0,fx,"
                    f"{tags}{char}"
                )
            
            char_x += self.processor.estimate_char_width(char)
        
        return lines
    
    def generate_layer3_highlight(self, syl: Syllable, line: KaraokeLine) -> str:
        """
        Layer 3: Efecto de highlight durante el karaoke
        """
        start_time = self.processor.format_time(int(syl.start_time))
        end_time = self.processor.format_time(int(syl.start_time + self.config.highlight_duration))
        
        half_dur = self.config.highlight_duration // 2
        
        tags = (
            f"{{\\an5\\move({syl.x:.0f},{syl.y - 10:.0f},{syl.x:.0f},{syl.y:.0f})"
            f"\\fscx{self.config.highlight_scale_x}\\fscy{self.config.highlight_scale_y}"
            f"\\bord3\\blur4"
            f"\\3c{self.hex_to_ass(self.config.highlight_border_color)}"
            f"\\xshad0\\yshad-4"
            f"\\4c{self.hex_to_ass(self.config.highlight_shadow_color)}"
            f"\\t(0,{half_dur},\\frz{self.config.highlight_rotation}"
            f"\\fry{self.config.highlight_perspective_y}\\frx{self.config.highlight_perspective_x})"
            f"\\t({half_dur},{self.config.highlight_duration},\\c{self.hex_to_ass(self.config.primary_color)})"
            f"\\t(100,{self.config.highlight_duration},\\fscx100\\fscy100\\fry0\\frz0\\frx0)}}"
        )
        
        return (
            f"Dialogue: 3,{start_time},{end_time},{line.style},,0,0,0,fx,"
            f"{tags}{syl.text}"
        )
    
    def generate_all_layers(self, karaoke_line: KaraokeLine) -> List[str]:
        """Generar todas las capas para una línea de karaoke"""
        result_lines = []
        
        line_end_ms = self.processor.parse_time(karaoke_line.end_time)
        
        for syl in karaoke_line.syllables:
            # Layer 1: Main
            result_lines.append(self.generate_layer1_main(syl, karaoke_line, line_end_ms))
            
            # Layer 2: Entry (múltiples líneas, una por caracter)
            result_lines.extend(self.generate_layer2_entry(syl, karaoke_line))
            
            # Layer 3: Highlight
            result_lines.append(self.generate_layer3_highlight(syl, karaoke_line))
        
        return result_lines
    
    def process_line(self, dialogue_line: str) -> List[str]:
        """Procesar una línea de diálogo y generar efectos"""
        karaoke_line = self.processor.parse_dialogue_line(dialogue_line)
        if karaoke_line and karaoke_line.syllables:
            return self.generate_all_layers(karaoke_line)
        return []
        
# Mantener compatibilidad con efectos simples anteriores
class KaraokeEffects:
    """Generador de efectos simples (compatibilidad)"""
    
    LEAD_IN_EFFECTS = {
        "Fade In": "fade_in",
        "Scale In": "scale_in",
        "Move Up": "move_up",
        "Move Down": "move_down",
        "Move Left": "move_left",
        "Move Right": "move_right",
        "Blur In": "blur_in",
        "Rotate In": "rotate_in",
        "Multi-Layer": "multi_layer"
    }
    
    LEAD_OUT_EFFECTS = {
        "Fade Out": "fade_out",
        "Scale Out": "scale_out",
        "Blur Out": "blur_out",
        "Rotate Out": "rotate_out"
    }
    
    def __init__(self, colors: Dict = None, size: int = 48, border_size: int = 2, shadow_size: int = 2):
        self.colors = colors or {
            "primary": "#FFFFFF",
            "secondary": "#000000",
            "border": "#000000",
            "shadow": "#000000"
        }
        self.size = size
        self.border_size = border_size
        self.shadow_size = shadow_size
    
    def hex_to_ass_color(self, hex_color: str) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"&H00{b}{g}{r}&"
    
    def generate_lead_in(self, effect_name: str, duration: int = 300) -> str:
        effect = self.LEAD_IN_EFFECTS.get(effect_name, "fade_in")
        
        if effect == "fade_in":
            return f"{{\\fad({duration},0)}}"
        elif effect == "scale_in":
            return f"{{\\t(0,{duration},\\fscx100\\fscy100)\\fscx0\\fscy0}}"
        elif effect == "move_up":
            return f"{{\\t(0,{duration},\\move($x,$y+50,$x,$y))}}"
        elif effect == "blur_in":
            return f"{{\\t(0,{duration},\\blur0)\\blur10}}"
        elif effect == "rotate_in":
            return f"{{\\t(0,{duration},\\frz0)\\frz360}}"
        
        return f"{{\\fad({duration},0)}}"
    
    def generate_lead_out(self, effect_name: str, duration: int = 300) -> str:
        effect = self.LEAD_OUT_EFFECTS.get(effect_name, "fade_out")
        
        if effect == "fade_out":
            return f"{{\\fad(0,{duration})}}"
        elif effect == "scale_out":
            return f"{{\\t($end-{duration},$end,\\fscx0\\fscy0)}}"
        elif effect == "blur_out":
            return f"{{\\t($end-{duration},$end,\\blur10)}}"
        
        return f"{{\\fad(0,{duration})}}"
    
    def apply_colors(self) -> str:
        tags = []
        tags.append(f"\\1c{self.hex_to_ass_color(self.colors['primary'])}")
        tags.append(f"\\2c{self.hex_to_ass_color(self.colors['secondary'])}")
        tags.append(f"\\3c{self.hex_to_ass_color(self.colors['border'])}")
        tags.append(f"\\4c{self.hex_to_ass_color(self.colors['shadow'])}")
        tags.append(f"\\bord{self.border_size}")
        tags.append(f"\\shad{self.shadow_size}")
        return "{" + "".join(tags) + "}"


def get_available_effects(effect_type: str) -> List[str]:
    if effect_type == "lead_in":
        return list(KaraokeEffects.LEAD_IN_EFFECTS.keys())
    elif effect_type == "lead_out":
        return list(KaraokeEffects.LEAD_OUT_EFFECTS.keys())
    return []
