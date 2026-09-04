# Video Analyzer v1.0.0

Aplicación para **transcribir y analizar videos** usando IA (Whisper + Ollama/Claude).
Soporta procesamiento 100% local con Ollama o en la nube con Claude AI (Anthropic).

## Novedades v1.0.0

- **🤖 Soporte para Claude AI** - Modelos Claude (Sonnet 4.5, Opus 4.5, 3.5 Sonnet, 3.5 Haiku)
- **🔄 Selector de proveedor IA** - Alterna entre Ollama (local) y Claude (API)
- **🔐 Seguridad de credenciales** - API Key obtenida mediante la UI (en memoria de sesión) o vía `ANTHROPIC_API_KEY`, sin persistencia en texto plano en disco
- **📁 Drag & Drop** - Arrastra videos directamente a la interfaz
- **⚡ Sistema de caché** - Caché de transcripción para reanudar o reanalizar rápidamente
- **📄 Visor de reportes** - Previsualizador integrado con soporte Markdown
- **📜 Changelog & Licencia** - Registro de cambios formal ([CHANGELOG.md](CHANGELOG.md)) y licencia MIT oficial ([LICENSE](LICENSE))

## Novedades v2.0

- **Interfaz moderna** con diseño de cards y layout mejorado
- **Temas Dark/Light** con toggle y persistencia
- **Configuracion automatica** segun GPU detectada
- **Panel de ajustes avanzados** (modelos, temperatura, contexto)
- **Previsualizador de reportes** integrado con formato Markdown
- **Analisis 100% en español** garantizado
- **Estados de botones** claros durante el procesamiento
- **Atajos de teclado** para operaciones rapidas

## Caracteristicas

- **Transcripcion automatica** con OpenAI Whisper (local)
- **Analisis con IA** usando Ollama (local) o Claude AI (API)
- **Modelos Claude**: Sonnet 4.5, Opus 4.5, 3.5 Sonnet, 3.5 Haiku
- **Aceleracion GPU** con CUDA (NVIDIA)
- **Drag & Drop** para cargar videos facilmente
- **Interfaz grafica** intuitiva con progreso por pasos
- **Soporte multi-idioma**: Español, Ingles, Portugues, Frances, Aleman, Italiano
- **Reportes en Markdown/TXT/JSON** con resumen, puntos clave y transcripcion
- **Configuracion persistente** en archivo config.json

## Requisitos

- **Python 3.10+**
- **NVIDIA GPU** (recomendado, 4GB+ VRAM) o CPU
- **Ollama** instalado con modelo descargado (para IA local)
- **O API Key de Claude** (para usar Claude AI)
- **FFmpeg** (incluido en el proyecto)

## Instalacion

### 1. Clonar/Descargar el proyecto

```bash
cd C:\Users\TuUsuario\source\repos
git clone <repo-url> video-analyzer
cd video-analyzer
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Para GPU NVIDIA (recomendado)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade
```

### 4. Configurar proveedor de IA

#### Opcion A: Ollama (Local - Gratis)

```bash
# Instalar Ollama desde https://ollama.com
# Luego descargar un modelo:
ollama pull llama2
# o para mejor calidad:
ollama pull llama3.1:8b
```

#### Opcion B: Claude AI (API - Requiere cuenta)

1. Crear cuenta en [console.anthropic.com](https://console.anthropic.com)
2. Generar API key
3. En la app: **Ajustes** → **Configuracion Avanzada** → Seleccionar "claude" como proveedor
4. Pegar tu API key

## Uso

### Interfaz Grafica (Recomendado)

```bash
# Opcion 1: Doble click o ejecucion desde terminal
scripts\run_gui.bat

# Opcion 2: Con entorno virtual activo
venv\Scripts\activate
python gui.py
```

### Linea de Comandos (CLI)

```bash
# Opcion 1: Usando el script en scripts/
scripts\run.bat "ruta\al\video.mp4" [idioma]

# Opcion 2: Directamente con Python
python analyzer.py "video.mp4" es
```

## Interfaz Grafica

### Ventana Principal

```
+--------------------------------------------------+
|  Video Analyzer              [Tema] [Ajustes]    |
+--------------------------------------------------+
|  +-- VIDEO --+          +-- CONFIGURACION --+    |
|  | Arrastra  |          | Idioma: [es]       |   |
|  | video aqui|          | Whisper: [small]   |   |
|  +-----------+          | Ollama: [llama2]   |   |
|                         +--------------------+   |
|  +-- PROGRESO ---------------------------------+ |
|  | [====60%====                    ] 02:34     | |
|  | [OK] 1. Extraccion de audio      00:12      | |
|  | [OK] 2. Transcripcion            01:45      | |
|  | [>>] 3. Generando resumen        ...        | |
|  | [ ] 4. Extrayendo puntos clave              | |
|  | [ ] 5. Analisis detallado                   | |
|  | [ ] 6. Guardando reporte                    | |
|  +---------------------------------------------+ |
|                                                  |
|  [INICIAR ANALISIS] [CANCELAR]    [Abrir Reporte]|
|                                                  |
|  GPU: NVIDIA RTX A500 (4.0GB)           v2.0    |
+--------------------------------------------------+
```

### Atajos de Teclado

| Atajo | Accion |
|-------|--------|
| `Ctrl+O` | Seleccionar video |
| `Enter` | Iniciar analisis |
| `Esc` | Cancelar proceso |

### Panel de Configuracion Avanzada

Accesible desde el boton **[Ajustes]**:

- **Modelos**:
  - Whisper: tiny/base/small/medium/large
  - Proveedor IA: Ollama o Claude
  - Modelo Ollama: detecta modelos instalados automaticamente
  - Modelo Claude: Sonnet 4.5, Opus 4.5, 3.5 Sonnet, 3.5 Haiku
  - API Key Claude: input seguro con asteriscos
- **Salida**: Carpeta destino, formato (md/txt/json)
- **Procesamiento**: GPU on/off, eliminar audio temporal
- **Ollama Avanzado**: Context window (4096-32768), Temperature (0-1)
- **Claude Avanzado**: Max tokens (2048-8192), Temperature (0-1)

### Previsualizador de Reportes

Al hacer clic en **[Abrir Reporte]** se abre una ventana con:

- Contenido formateado con colores (headers, timestamps, separadores)
- Boton **[Abrir Externo]** para abrir con app del sistema
- Boton **[Copiar Ruta]** para copiar ubicacion al portapapeles
- Informacion de tamaño y ubicacion del archivo

## Configuracion Automatica

En la primera ejecucion, la aplicacion detecta tu GPU y configura automaticamente:

| VRAM GPU | Modelo Whisper |
|----------|----------------|
| >= 10GB | large |
| >= 5GB | medium |
| >= 2GB | small |
| >= 1GB | base |
| < 1GB / CPU | tiny |

La configuracion se guarda en `config.json` y persiste entre sesiones.

## Estructura del Proyecto
 
```
video-analyzer/
├── docs/                            # Documentacion complementaria
│   └── CONFIGURACION_RECOMENDADA.md # Guia de hardware, VRAM y modelos
├── scripts/                         # Scripts de ejecucion y setup
│   ├── run.bat                      # Lanzador CLI para transcripcion y analisis
│   ├── run_gui.bat                  # Lanzador directo de la interfaz grafica
│   └── setup.bat                    # Script de instalacion de dependencias
├── analyzer.py                      # Motor principal de transcripcion y analisis (CLI)
├── gui.py                           # Interfaz grafica moderna v1.0.0
├── requirements.txt                 # Dependencias Python fijadas
├── CHANGELOG.md                     # Historial de versiones (Keep a Changelog)
├── LICENSE                          # Licencia MIT (Yasmany Reyes Gonzalez)
├── README.md                        # Documentacion principal
└── config.json                      # Configuracion local del usuario (ignorado en git)
```

## Modelos Whisper Disponibles

| Modelo | VRAM | Precision | Velocidad |
|--------|------|-----------|-----------|
| tiny | ~1GB | Basica | Muy rapido |
| base | ~1GB | Aceptable | Rapido |
| small | ~2GB | Buena | Medio |
| medium | ~5GB | Muy buena | Lento |
| large | ~10GB | Excelente | Muy lento |

## Formatos de Salida

### Markdown (.md) - Por defecto

```markdown
# ANALISIS DE VIDEO

**Archivo:** reunion_equipo.mp4
**Fecha:** 2024-01-07 20:13
**Duracion:** 16.3 minutos
**Modelos:** Whisper small + llama2

---

## RESUMEN EJECUTIVO

El video presenta una reunion tecnica sobre...

---

## PUNTOS CLAVE

- Punto 1: Descripcion
- Punto 2: Descripcion

---

## ANALISIS DETALLADO

### TEMA PRINCIPAL
...

### IDEAS PRINCIPALES
...

---

## TRANSCRIPCION COMPLETA

[Texto completo]

---

## TRANSCRIPCION CON TIMESTAMPS

[00:00] Primera frase...
[00:15] Segunda frase...
```

### JSON (.json)

Estructura con campos: file, date, duration_min, summary, key_points, analysis, transcription, segments.

### Texto Plano (.txt)

Mismo contenido que Markdown pero sin formato.

## Solucion de Problemas

### "CUDA not available"

- Verifica que tienes GPU NVIDIA
- Reinstala PyTorch con CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

### "FFmpeg not found"

- FFmpeg debe estar en la carpeta del proyecto
- O instalalo globalmente: `winget install ffmpeg`

### "Ollama connection refused"

- Asegurate que Ollama este corriendo: `ollama serve`

### "API Key de Claude no configurada"

- Ve a **Ajustes** → **Configuracion Avanzada**
- Selecciona "claude" como proveedor
- Pega tu API key de Anthropic

### Transcripcion lenta

- Usa modelo `small` o `base` en lugar de `medium`
- Verifica que GPU este activa (ver status bar en GUI)

### Analisis sale en ingles

- v2.1 incluye prompts optimizados para español
- Funciona tanto con Ollama como con Claude

### Drag & Drop no funciona

- Instala `tkinterdnd2`: `pip install tkinterdnd2`
- O usa click para seleccionar archivos

## Licencia
 
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

Copyright (c) 2024-2026 Yasmany Reyes Gonzalez.

## Creditos

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcripcion
- [Ollama](https://ollama.com) - LLMs locales
- [MoviePy](https://zulko.github.io/moviepy/) - Procesamiento de video
