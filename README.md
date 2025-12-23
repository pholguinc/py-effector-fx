# Py Effector FX 🎤✨

Librería Python para generar efectos avanzados de karaoke en formato ASS (Advanced SubStation Alpha), diseñada para integrarse con Aegisub 3.4.2.

## 📋 Descripción

Py Effector FX es un generador de efectos multi-capa para subtítulos de karaoke. Permite crear animaciones complejas incluyendo:

- **Lead In**: Efectos de entrada (fade, scale, movimientos)
- **Lead Out**: Efectos de salida
- **Highlight**: Efectos de resaltado durante el karaoke
- **Efectos de 3 capas**: Generación simultánea de múltiples capas de animación

## 🚀 Características

- GUI intuitiva con Tkinter (tema oscuro)
- Integración directa con Aegisub mediante macro Lua
- Procesamiento automático de timing `{\k##}`
- Cálculo de posiciones de sílabas
- Múltiples efectos predefinidos
- Configuración de colores personalizable
- Soporte para múltiples estilos ASS

## 📁 Estructura del Proyecto

```
py-effector-fx/
├── py/
│   ├── gui_script.py        # Punto de entrada principal (GUI Tkinter)
│   ├── effects.py           # Generador de efectos multi-capa
│   ├── karaoke_processor.py # Parser de karaoke y timing
│   ├── process_effect.py    # Procesador de efectos por sílaba
│   ├── ass_parser.py        # Parser de archivos ASS
│   ├── run_gui.lua          # Macro para Aegisub
│   ├── run_gui.sh           # Script de inicio (macOS)
│   └── pages/               # Páginas de la GUI
│       ├── main_page.py         # Página principal
│       ├── lead_in_page.py      # Configuración Lead In
│       ├── lead_out_page.py     # Configuración Lead Out
│       ├── shape_page.py        # Configuración de formas
│       └── translation_page.py  # Configuración de traducción
├── kelibs/                  # Librerías auxiliares Lua
├── requireffi/              # FFI para Lua
└── ILL/                     # Librerías adicionales
```

## 📦 Requisitos

- **Python 3.10+**
- **Aegisub 3.4.2+**
- **Tkinter** (incluido en Python estándar)
- **macOS/Linux** (Windows con adaptaciones)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/pholguinc/py-effector-fx.git
cd py-effector-fx
```

### 2. Configurar macro en Aegisub

1. Copia el archivo `py/run_gui.lua` a la carpeta de automatización de Aegisub:
   - **macOS**: `~/Library/Application Support/Aegisub/automation/autoload/`
   - **Linux**: `~/.aegisub/automation/autoload/`
   - **Windows**: `%APPDATA%\Aegisub\automation\autoload\`

2. Edita `run_gui.lua` y ajusta las rutas:

```lua
local PYTHON = "/ruta/a/python3"
local SCRIPT_DIR = "/ruta/a/py-effector-fx/py"
```

3. Reinicia Aegisub

## 🎯 Uso

### Desde Aegisub

1. Abre tu archivo `.ass` con timing de karaoke
2. Ve a `Automation` → `Py Effector FX`
3. Configura los efectos en la GUI
4. Haz clic en "Generar" para aplicar los efectos

### Ejecución directa

```bash
cd py-effector-fx/py
python3 gui_script.py [archivo.ass]
```

## 🎨 Efectos Disponibles

### Lead In (Entrada)
| Efecto | Descripción |
|--------|-------------|
| Fade In | Aparecer gradualmente |
| Scale In | Crecer desde el centro |
| Move Up | Subir desde abajo |
| Move Down | Bajar desde arriba |
| Rotate In | Rotar al aparecer |
| Random Rotate | Rotación aleatoria |
| Zoom Bounce | Zoom con rebote |
| Slide Left | Deslizar desde izquierda |
| Slide Right | Deslizar desde derecha |

### Lead Out (Salida)
| Efecto | Descripción |
|--------|-------------|
| Fade Out | Desaparecer gradualmente |
| Scale Out | Reducir al centro |
| Move Up | Subir y desaparecer |
| Move Down | Bajar y desaparecer |
| Rotate Out | Rotar al desaparecer |

## 🔌 API Python

### Clases principales

#### `KaraokeProcessor`
Procesa líneas de karaoke y extrae sílabas con timing.

```python
from karaoke_processor import KaraokeProcessor, process_karaoke_line

processor = KaraokeProcessor(fontsize=48, line_y=29)
karaoke_line = processor.parse_dialogue_line(dialogue_line)

for syllable in karaoke_line.syllables:
    print(f"{syllable.text}: {syllable.start_time}ms - {syllable.end_time}ms")
```

#### `MultiLayerEffectGenerator`
Genera efectos de 3 capas para karaoke.

```python
from effects import MultiLayerEffectGenerator, EffectConfig

config = EffectConfig(
    primary_color="#FFFFFF",
    secondary_color="#000000",
    border_color="#FC76F2",
    highlight_border_color="#FFD9C5",
    fade_in_duration=300,
    fade_out_duration=300,
    entry_type="random_rotate"
)

generator = MultiLayerEffectGenerator(config)
layers = generator.process_line(dialogue_line)
```

#### `KaraokeEffects`
Generador de efectos simples (compatibilidad).

```python
from effects import KaraokeEffects, get_available_effects

effects = KaraokeEffects(
    colors={"primary": "#FFFFFF", "border": "#FC76F2"},
    size=48
)

lead_in_tags = effects.generate_lead_in("fade_in", duration=300)
lead_out_tags = effects.generate_lead_out("fade_out", duration=300)
```

### Dataclasses

#### `Syllable`
```python
@dataclass
class Syllable:
    text: str           # Texto de la sílaba
    duration: int       # Duración en centésimas
    start_time: int     # Tiempo de inicio (ms)
    end_time: int       # Tiempo de fin (ms)
    x: float            # Posición X
    y: float            # Posición Y
    index: int          # Índice de sílaba
    char_index: int     # Índice del primer caracter
```

#### `KaraokeLine`
```python
@dataclass
class KaraokeLine:
    layer: int
    start_time: str     # Formato 0:00:00.00
    end_time: str
    style: str
    name: str
    margin_l: int
    margin_r: int
    margin_v: int
    effect: str
    text: str
    syllables: List[Syllable]
    duration: int       # Duración total en ms
```

## 📝 Formato ASS

La librería trabaja con el estándar ASS para timing de karaoke:

```ass
Dialogue: 0,0:00:10.00,0:00:15.00,Default,,0,0,0,,{\k50}Ho{\k30}la {\k70}mun{\k40}do
```

Donde `{\k##}` indica la duración en centésimas de segundo de cada sílaba.

## 🛠️ Desarrollo

### Ejecutar en modo desarrollo

```bash
cd py-effector-fx/py
python3 gui_script.py
```

### Estructura de páginas

Las páginas de la GUI heredan de `BasePage` y se registran automáticamente:

```python
from pages.base_page import BasePage

class CustomPage(BasePage):
    def create_widgets(self):
        # Crear widgets aquí
        pass
```

## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

## 📧 Contacto

- **Autor**: pholguinc
- **Repositorio**: [py-effector-fx](https://github.com/pholguinc/py-effector-fx)

---

> ⚠️ **Nota**: Esta es una versión beta en desarrollo activo. Algunas funciones pueden cambiar.
