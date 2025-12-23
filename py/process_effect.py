#!/usr/bin/env python3
"""
Procesador de efectos - Genera líneas por sílaba con efectos lead-in
Usa el fontsize del estilo para calcular posiciones
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class Syllable:
    text: str
    duration: int
    start_time: int
    end_time: int
    x: float
    y: float


def read_config(config_file: str) -> dict:
    config = {}
    try:
        with open(config_file, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    config[key] = value
    except:
        pass
    return config


def hex_to_ass(hex_color: str) -> str:
    hex_color = hex_color.lstrip('#')
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"&H00{b}{g}{r}&"


def parse_time(time_str: str) -> int:
    match = re.match(r'(\d+):(\d+):(\d+)\.(\d+)', time_str)
    if match:
        h, m, s, cs = map(int, match.groups())
        return (h * 3600 + m * 60 + s) * 1000 + cs * 10
    return 0


def format_time(ms: int) -> str:
    if ms < 0:
        ms = 0
    cs = (ms % 1000) // 10
    s = (ms // 1000) % 60
    m = (ms // 60000) % 60
    h = ms // 3600000
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def parse_styles(ass_file: str) -> Dict[str, dict]:
    """Parsear estilos del archivo ASS"""
    styles = {}
    in_styles = False
    format_fields = []
    
    try:
        with open(ass_file, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line.startswith('[V4'):
                    in_styles = True
                    continue
                elif line.startswith('[') and in_styles:
                    break
                
                if in_styles:
                    if line.startswith('Format:'):
                        format_str = line[7:].strip()
                        format_fields = [f.strip() for f in format_str.split(',')]
                    elif line.startswith('Style:'):
                        style_str = line[6:].strip()
                        values = [v.strip() for v in style_str.split(',')]
                        if format_fields and len(values) >= 3:
                            style = {}
                            for i, field in enumerate(format_fields):
                                if i < len(values):
                                    style[field] = values[i]
                            if 'Name' in style:
                                styles[style['Name']] = style
    except:
        pass
    
    return styles


def get_style_metrics(styles: Dict, style_name: str) -> tuple:
    """Obtener fontsize y spacing del estilo"""
    if style_name in styles:
        style = styles[style_name]
        fontsize = int(style.get('Fontsize', 48))
        spacing = float(style.get('Spacing', 0))
        return fontsize, spacing
    return 48, 0


def estimate_char_width(char: str, fontsize: int, spacing: float = 0) -> float:
    """Estimar ancho de caracter basado en fontsize del estilo"""
    narrow = set('iIlL1|!.,;:\'"')
    wide = set('mMwW')
    
    # Factor base segun tipo de caracter
    if char in narrow:
        factor = 0.3
    elif char in wide:
        factor = 0.6
    elif char == ' ':
        factor = 0.25
    elif ord(char) > 127:  # Caracteres japoneses/unicode
        factor = 1.0
    else:
        factor = 0.5
    
    return fontsize * factor + spacing


def estimate_text_width(text: str, fontsize: int, spacing: float = 0) -> float:
    total = sum(estimate_char_width(c, fontsize, spacing) for c in text)
    return total


def extract_syllables(text: str, fontsize: int, spacing: float, line_y: float) -> List[Syllable]:
    """Extraer sílabas con timing"""
    syllables = []
    pattern = r'\{[^}]*\\[kK]f?(\d+)[^}]*\}([^{]*)'
    
    current_time = 0
    current_x = 10  # margin izquierdo
    
    for match in re.finditer(pattern, text):
        duration_cs = int(match.group(1))
        syl_text = match.group(2)
        
        if not syl_text:
            continue
        
        duration_ms = duration_cs * 10
        syl_width = estimate_text_width(syl_text, fontsize, spacing)
        
        syllable = Syllable(
            text=syl_text,
            duration=duration_cs,
            start_time=current_time,
            end_time=current_time + duration_ms,
            x=current_x + syl_width / 2,
            y=line_y
        )
        
        syllables.append(syllable)
        current_time += duration_ms
        current_x += syl_width
    
    return syllables


def parse_dialogue(line: str):
    match = re.match(
        r'Dialogue:\s*(\d+),([^,]+),([^,]+),([^,]*),([^,]*),(\d+),(\d+),(\d+),([^,]*),(.*)',
        line
    )
    if not match:
        return None
    
    return {
        'layer': int(match.group(1)),
        'start': match.group(2),
        'end': match.group(3),
        'style': match.group(4),
        'actor': match.group(5),
        'margin_l': int(match.group(6)),
        'margin_r': int(match.group(7)),
        'margin_v': int(match.group(8)),
        'effect': match.group(9),
        'text': match.group(10)
    }


def generate_syllable_lines(dialogue: dict, config: dict, styles: Dict) -> List[str]:
    """Generar líneas por sílaba con efecto lead-in"""
    lines = []
    
    entry_duration = int(config.get('ENTRY_DURATION', 300))
    fadeout_duration = int(config.get('FADEOUT_DURATION', 300))
    primary = config.get('PRIMARY_COLOR', '#FFFFFF')
    border_color = config.get('BORDER_COLOR', '#FC76F2')
    shadow_color = config.get('SHADOW_COLOR', '#000000')
    border_size = config.get('BORDER_SIZE', '2')
    shadow_size = config.get('SHADOW_SIZE', '0')
    blur = config.get('BLUR', '3')
    
    # Obtener métricas del estilo
    fontsize, spacing = get_style_metrics(styles, dialogue['style'])
    
    line_start_ms = parse_time(dialogue['start'])
    line_end_ms = parse_time(dialogue['end'])
    
    # Posición Y por defecto (puedes ajustar según el alignment del estilo)
    line_y = 29
    
    syllables = extract_syllables(dialogue['text'], fontsize, spacing, line_y)
    
    if not syllables:
        return lines
    
    for syl in syllables:
        syl_start_abs = line_start_ms + syl.start_time
        syl_end_abs = line_end_ms
        
        tags = (
            f"\\an5\\pos({syl.x:.0f},{syl.y:.0f})"
            f"\\fad({entry_duration},{fadeout_duration})"
            f"\\blur{blur}"
            f"\\bord{border_size}"
            f"\\shad{shadow_size}"
            f"\\c{hex_to_ass(primary)}"
            f"\\3c{hex_to_ass(border_color)}"
            f"\\4c{hex_to_ass(shadow_color)}"
        )
        
        line = (
            f"Dialogue: {dialogue['layer']},"
            f"{format_time(syl_start_abs)},{format_time(syl_end_abs)},"
            f"{dialogue['style']},,0,0,0,fx,"
            f"{{{tags}}}{syl.text}"
        )
        
        lines.append(line)
    
    return lines


def read_dialogue_lines(ass_file: str) -> list:
    lines = []
    try:
        with open(ass_file, 'r', encoding='utf-8-sig') as f:
            for line in f:
                if line.startswith('Dialogue:'):
                    lines.append(line.strip())
    except:
        try:
            with open(ass_file, 'r', encoding='latin-1') as f:
                for line in f:
                    if line.startswith('Dialogue:'):
                        lines.append(line.strip())
        except:
            pass
    return lines


def main():
    if len(sys.argv) < 4:
        print("Uso: process_effect.py <ass_file> <config_file> <output_file>")
        sys.exit(1)
    
    ass_file = sys.argv[1]
    config_file = sys.argv[2]
    output_file = sys.argv[3]
    
    config = read_config(config_file)
    
    if not config:
        print("No se pudo leer la configuracion")
        sys.exit(1)
    
    # Parsear estilos del ASS
    styles = parse_styles(ass_file)
    
    selected_style = config.get('SELECTED_STYLE', '')
    
    dialogue_lines = read_dialogue_lines(ass_file)
    
    all_generated = []
    for line in dialogue_lines:
        dialogue = parse_dialogue(line)
        if dialogue:
            if selected_style and dialogue['style'] != selected_style:
                continue
            
            generated = generate_syllable_lines(dialogue, config, styles)
            all_generated.extend(generated)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_generated:
            f.write(line + '\n')
    
    print(f"Generadas {len(all_generated)} lineas con fontsize del estilo")


if __name__ == "__main__":
    main()
