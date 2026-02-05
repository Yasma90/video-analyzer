"""
Video Analyzer - Interfaz Grafica Moderna
Analisis de video con IA local (Whisper + Ollama)
Version 2.0 - UX Mejorada
"""

import os
import sys
import json
import ctypes
from pathlib import Path

# DPI Awareness modo 2 - Per Monitor v2
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

# Add FFmpeg to PATH
script_dir = Path(__file__).parent
ffmpeg_path = script_dir / "ffmpeg-8.0.1-essentials_build" / "bin"
if ffmpeg_path.exists():
    os.environ["PATH"] = str(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime

# ============================================================================
# CONFIGURACION Y TEMAS
# ============================================================================

CONFIG_FILE = script_dir / "config.json"

DEFAULT_CONFIG = {
    "theme": "dark",
    "whisper_model": "small",
    "ai_provider": "ollama",  # "ollama" or "claude"
    "ollama_model": "llama2",
    "claude_model": "claude-sonnet-4-5-20250929",
    "claude_api_key": "",
    "language": "es",
    "output_dir": "",
    "output_format": "md",
    "use_gpu": True,
    "delete_temp_audio": True,
    "ollama_ctx": 8192,
    "ollama_temp": 0.7,
    "claude_max_tokens": 4096,
    "claude_temp": 0.5
}

THEMES = {
    'dark': {
        'bg': '#1a1a2e',
        'bg_light': '#16213e',
        'card': '#232946',
        'accent': '#0f3460',
        'highlight': '#e94560',
        'text': '#eaeaea',
        'text_dim': '#a0a0a0',
        'success': '#00d26a',
        'warning': '#ffb830',
        'error': '#ff6b6b',
        'border': '#394867',
        'input_bg': '#0d1117',
        'input_fg': '#c9d1d9'
    },
    'light': {
        'bg': '#f0f2f5',
        'bg_light': '#ffffff',
        'card': '#ffffff',
        'accent': '#e4e6eb',
        'highlight': '#e94560',
        'text': '#1c1e21',
        'text_dim': '#65676b',
        'success': '#31a24c',
        'warning': '#f7b928',
        'error': '#f02849',
        'border': '#dadde1',
        'input_bg': '#ffffff',
        'input_fg': '#1c1e21'
    }
}

LANGUAGES = {
    "es": "Espanol",
    "en": "English",
    "pt": "Portugues",
    "fr": "Francais",
    "de": "Deutsch",
    "it": "Italiano"
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_recommended_config():
    """Detecta hardware y devuelve configuracion optima"""
    config = DEFAULT_CONFIG.copy()

    try:
        import torch
        if torch.cuda.is_available():
            # Detectar VRAM
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)

            # Seleccionar modelo Whisper segun VRAM
            if vram_gb >= 10:
                config['whisper_model'] = 'large'
            elif vram_gb >= 5:
                config['whisper_model'] = 'medium'
            elif vram_gb >= 2:
                config['whisper_model'] = 'small'
            elif vram_gb >= 1:
                config['whisper_model'] = 'base'
            else:
                config['whisper_model'] = 'tiny'

            config['use_gpu'] = True
        else:
            config['whisper_model'] = 'base'
            config['use_gpu'] = False
    except:
        config['whisper_model'] = 'small'

    return config

def load_config():
    """Carga configuracion desde archivo o genera recomendada"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(saved)
                return config
        except:
            pass

    # Primera ejecucion: generar config recomendada
    config = get_recommended_config()
    save_config(config)
    return config

def save_config(config):
    """Guarda configuracion a archivo"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_ollama_models():
    """Obtiene lista de modelos Ollama instalados"""
    try:
        import ollama
        models = ollama.list()
        return [m['name'].split(':')[0] for m in models.get('models', [])]
    except:
        return ["llama2", "llama3", "mistral", "codellama"]

def format_time(seconds):
    """Formatea segundos a MM:SS"""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

# ============================================================================
# DIALOGO DE CONFIGURACION
# ============================================================================

class SettingsDialog:
    """Dialogo de configuracion avanzada"""

    def __init__(self, parent, config, theme):
        self.result = None
        self.config = config.copy()
        self.theme = theme

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configuracion Avanzada")

        # Tamaño completo para mostrar todo sin scroll
        win_w = 580
        win_h = 920

        # Centrar sobre la ventana padre (misma pantalla)
        parent.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        x = px + (pw - win_w) // 2
        y = py + (ph - win_h) // 2

        self.dialog.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.dialog.resizable(True, True)
        self.dialog.minsize(550, 850)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Fondo fijo para mejor visibilidad
        self.dialog.configure(bg='#2d2d2d')

        self._create_ui()

    def _create_ui(self):
        # Colores fijos de alto contraste
        bg = '#2d2d2d'
        fg = '#ffffff'
        fg_dim = '#b0b0b0'
        input_bg = '#3d3d3d'
        border = '#555555'

        # Canvas con scroll para pantallas pequeñas
        canvas = tk.Canvas(self.dialog, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)

        main = tk.Frame(canvas, bg=bg, padx=20, pady=15)

        main.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=main, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scroll con rueda del mouse
        def on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass

        # Bind mousewheel solo a este canvas
        canvas.bind("<MouseWheel>", on_mousewheel)
        # También bind a los widgets internos para que funcione cuando el mouse está sobre ellos
        main.bind("<MouseWheel>", on_mousewheel)

        # Guardar referencias para cleanup
        self.canvas = canvas
        self.main_frame = main

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Titulo
        tk.Label(main, text="Configuracion Avanzada",
                font=('Segoe UI', 16, 'bold'), bg=bg, fg=fg).pack(anchor='w', pady=(0,15))

        # === SECCION: MODELOS ===
        self._section(main, "MODELOS", bg, fg_dim, border)

        # Whisper
        row = tk.Frame(main, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Modelo Whisper:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.whisper_var = tk.StringVar(value=self.config['whisper_model'])
        whisper_combo = ttk.Combobox(row, textvariable=self.whisper_var,
                                      values=["tiny", "base", "small", "medium", "large"],
                                      width=18, state='readonly')
        whisper_combo.pack(side=tk.LEFT)

        # AI Provider
        row = tk.Frame(main, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Proveedor IA:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.provider_var = tk.StringVar(value=self.config.get('ai_provider', 'ollama'))
        provider_combo = ttk.Combobox(row, textvariable=self.provider_var,
                                      values=["ollama", "claude"],
                                      width=18, state='readonly')
        provider_combo.pack(side=tk.LEFT)
        provider_combo.bind('<<ComboboxSelected>>', self._on_provider_change)

        # Ollama
        self.ollama_row = tk.Frame(main, bg=bg)
        self.ollama_row.pack(fill=tk.X, pady=5)
        tk.Label(self.ollama_row, text="Modelo Ollama:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.ollama_var = tk.StringVar(value=self.config['ollama_model'])
        ollama_models = get_ollama_models()
        if self.config['ollama_model'] not in ollama_models:
            ollama_models.insert(0, self.config['ollama_model'])
        ollama_combo = ttk.Combobox(self.ollama_row, textvariable=self.ollama_var,
                                     values=ollama_models, width=18)
        ollama_combo.pack(side=tk.LEFT)

        # Claude
        self.claude_row = tk.Frame(main, bg=bg)
        self.claude_row.pack(fill=tk.X, pady=5)
        tk.Label(self.claude_row, text="Modelo Claude:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.claude_model_var = tk.StringVar(value=self.config.get('claude_model', 'claude-sonnet-4-5-20250929'))
        claude_combo = ttk.Combobox(self.claude_row, textvariable=self.claude_model_var,
                                     values=[
                                         "claude-sonnet-4-5-20250929",
                                         "claude-opus-4-5-20251101",
                                         "claude-3-5-sonnet-20241022",
                                         "claude-3-5-haiku-20241022"
                                     ], width=18)
        claude_combo.pack(side=tk.LEFT)

        # Claude API Key
        self.api_key_row = tk.Frame(main, bg=bg)
        self.api_key_row.pack(fill=tk.X, pady=5)
        tk.Label(self.api_key_row, text="API Key Claude:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar(value=self.config.get('claude_api_key', ''))
        tk.Entry(self.api_key_row, textvariable=self.api_key_var, width=22,
                bg=input_bg, fg=fg, insertbackground=fg, show='*',
                relief=tk.SOLID, bd=1).pack(side=tk.LEFT)

        # Actualizar visibilidad inicial
        self._on_provider_change()

        # === SECCION: SALIDA ===
        self._section(main, "SALIDA", bg, fg_dim, border)

        # Carpeta
        row = tk.Frame(main, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Carpeta destino:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value=self.config['output_dir'])
        tk.Entry(row, textvariable=self.output_var, width=22,
                bg=input_bg, fg=fg, insertbackground=fg,
                relief=tk.SOLID, bd=1).pack(side=tk.LEFT, padx=(0,5))
        tk.Button(row, text="...", command=self._browse_output, width=4,
                 bg='#4a4a4a', fg=fg, relief=tk.RAISED,
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)

        # Formato
        row = tk.Frame(main, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Formato salida:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value=self.config['output_format'])
        format_combo = ttk.Combobox(row, textvariable=self.format_var,
                                     values=["md", "txt", "json"], width=18, state='readonly')
        format_combo.pack(side=tk.LEFT)

        # === SECCION: PROCESAMIENTO ===
        self._section(main, "PROCESAMIENTO", bg, fg_dim, border)

        # GPU
        self.gpu_var = tk.BooleanVar(value=self.config['use_gpu'])
        tk.Checkbutton(main, text="Usar GPU si esta disponible", variable=self.gpu_var,
                      bg=bg, fg=fg, selectcolor='#4a4a4a',
                      activebackground=bg, activeforeground=fg,
                      font=('Segoe UI', 11)).pack(anchor='w', pady=3)

        # Temp audio
        self.temp_var = tk.BooleanVar(value=self.config['delete_temp_audio'])
        tk.Checkbutton(main, text="Eliminar audio temporal despues de procesar", variable=self.temp_var,
                      bg=bg, fg=fg, selectcolor='#4a4a4a',
                      activebackground=bg, activeforeground=fg,
                      font=('Segoe UI', 11)).pack(anchor='w', pady=3)

        # === SECCION: OLLAMA AVANZADO ===
        self.ollama_advanced_section = tk.Frame(main, bg=bg)
        self.ollama_advanced_section.pack(fill=tk.X)

        self._section(self.ollama_advanced_section, "OLLAMA AVANZADO", bg, fg_dim, border)

        # Context
        row = tk.Frame(self.ollama_advanced_section, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Context Window:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.ctx_var = tk.StringVar(value=str(self.config['ollama_ctx']))
        ctx_combo = ttk.Combobox(row, textvariable=self.ctx_var,
                                  values=["4096", "8192", "16384", "32768"], width=18)
        ctx_combo.pack(side=tk.LEFT)

        # Temperature Ollama
        row = tk.Frame(self.ollama_advanced_section, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Temperature:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.ollama_temp_slider = tk.Scale(row, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                                    length=180, bg=bg, fg=fg, highlightthickness=0,
                                    troughcolor='#4a4a4a', activebackground='#e94560')
        self.ollama_temp_slider.set(self.config['ollama_temp'])
        self.ollama_temp_slider.pack(side=tk.LEFT)

        # === SECCION: CLAUDE AVANZADO ===
        self.claude_advanced_section = tk.Frame(main, bg=bg)
        self.claude_advanced_section.pack(fill=tk.X)

        self._section(self.claude_advanced_section, "CLAUDE AVANZADO", bg, fg_dim, border)

        # Max Tokens
        row = tk.Frame(self.claude_advanced_section, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Max Tokens:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.max_tokens_var = tk.StringVar(value=str(self.config.get('claude_max_tokens', 4096)))
        tokens_combo = ttk.Combobox(row, textvariable=self.max_tokens_var,
                                    values=["2048", "4096", "8192"], width=18)
        tokens_combo.pack(side=tk.LEFT)

        # Temperature Claude
        row = tk.Frame(self.claude_advanced_section, bg=bg)
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text="Temperature:", width=18, anchor='w',
                bg=bg, fg=fg, font=('Segoe UI', 11)).pack(side=tk.LEFT)
        self.claude_temp_slider = tk.Scale(row, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                                    length=180, bg=bg, fg=fg, highlightthickness=0,
                                    troughcolor='#4a4a4a', activebackground='#e94560')
        self.claude_temp_slider.set(self.config.get('claude_temp', 0.5))
        self.claude_temp_slider.pack(side=tk.LEFT)

        # === BOTONES ===
        btn_frame = tk.Frame(main, bg=bg)
        btn_frame.pack(fill=tk.X, pady=(20, 20))

        # GUARDAR primero, CANCELAR segundo
        btn_save = tk.Button(btn_frame, text="GUARDAR", command=self._save,
                            width=10, padx=8, pady=5,
                            bg='#28a745', fg='white',
                            font=('Segoe UI', 9, 'bold'),
                            relief=tk.RAISED, cursor='hand2',
                            activebackground='#218838', activeforeground='white')
        btn_save.pack(side=tk.LEFT, padx=(0, 8))

        btn_cancel = tk.Button(btn_frame, text="CANCELAR", command=self._cleanup_and_close,
                              width=10, padx=8, pady=5,
                              bg='#dc3545', fg='white',
                              font=('Segoe UI', 9, 'bold'),
                              relief=tk.RAISED, cursor='hand2',
                              activebackground='#c82333', activeforeground='white')
        btn_cancel.pack(side=tk.LEFT)

        # Forzar actualizacion del scrollregion para incluir los botones
        main.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _section(self, parent, title, bg, fg_dim, border):
        """Crea encabezado de seccion"""
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill=tk.X, pady=(12, 6))
        tk.Label(frame, text=title, font=('Segoe UI', 9, 'bold'),
                bg=bg, fg=fg_dim).pack(side=tk.LEFT)
        tk.Frame(frame, bg=border, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10,0))

    def _on_provider_change(self, event=None):
        """Muestra/oculta controles según el proveedor seleccionado"""
        provider = self.provider_var.get()
        if provider == "ollama":
            # Mostrar controles de Ollama
            self.ollama_row.pack(fill=tk.X, pady=5)
            self.ollama_advanced_section.pack(fill=tk.X)
            # Ocultar controles de Claude
            self.claude_row.pack_forget()
            self.api_key_row.pack_forget()
            self.claude_advanced_section.pack_forget()
        else:  # claude
            # Ocultar controles de Ollama
            self.ollama_row.pack_forget()
            self.ollama_advanced_section.pack_forget()
            # Mostrar controles de Claude
            self.claude_row.pack(fill=tk.X, pady=5)
            self.api_key_row.pack(fill=tk.X, pady=5)
            self.claude_advanced_section.pack(fill=tk.X)

        # Actualizar scrollregion despues de cambiar visibilidad
        self.main_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _browse_output(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if path:
            self.output_var.set(path)

    def _save(self):
        self.result = {
            'whisper_model': self.whisper_var.get(),
            'ai_provider': self.provider_var.get(),
            'ollama_model': self.ollama_var.get(),
            'claude_model': self.claude_model_var.get(),
            'claude_api_key': self.api_key_var.get(),
            'output_dir': self.output_var.get(),
            'output_format': self.format_var.get(),
            'use_gpu': self.gpu_var.get(),
            'delete_temp_audio': self.temp_var.get(),
            'ollama_ctx': int(self.ctx_var.get()),
            'ollama_temp': self.ollama_temp_slider.get(),
            'claude_max_tokens': int(self.max_tokens_var.get()),
            'claude_temp': self.claude_temp_slider.get()
        }
        self._cleanup_and_close()

    def _cleanup_and_close(self):
        """Cleanup bindings and close dialog"""
        try:
            self.canvas.unbind("<MouseWheel>")
            self.main_frame.unbind("<MouseWheel>")
        except:
            pass
        self.dialog.destroy()

# ============================================================================
# GUI PRINCIPAL
# ============================================================================

class VideoAnalyzerGUI:
    """Interfaz grafica moderna para Video Analyzer"""

    VERSION = "2.0"

    def __init__(self):
        self.config = load_config()
        self.root = tk.Tk()
        self.root.title("Video Analyzer")

        # Tamaño base más pequeño para caber en HD (1920x1080)
        # Con DPI awareness modo 2, escalar según DPI
        try:
            dpi = self.root.winfo_fpixels('1i')
            scale = dpi / 96.0
        except:
            scale = 1.0

        # Tamaño más conservador
        base_w, base_h = 780, 530
        win_w = int(base_w * scale)
        win_h = int(base_h * scale)

        # Limitar al 85% de la pantalla
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = min(win_w, int(screen_w * 0.85))
        win_h = min(win_h, int(screen_h * 0.85))

        # Centrar
        x = (screen_w - win_w) // 2
        y = max(10, (screen_h - win_h) // 2 - 40)

        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.minsize(int(600 * scale), int(350 * scale))
        self.root.resizable(True, True)

        self.video_path = None
        self.video_duration = None
        self.is_processing = False
        self.step_times = {}

        # Aplicar tema
        self._apply_theme()
        self._create_ui()
        self._bind_shortcuts()
        self._check_gpu()

        # Drag and drop
        self._setup_dnd()

    def _apply_theme(self):
        """Aplica el tema actual"""
        self.theme = THEMES[self.config['theme']]
        self.root.configure(bg=self.theme['bg'])

        # Configurar estilos ttk
        style = ttk.Style()
        style.theme_use('clam')

        t = self.theme
        style.configure("TFrame", background=t['bg'])
        style.configure("Card.TFrame", background=t['card'])
        style.configure("TLabel", background=t['bg'], foreground=t['text'], font=('Segoe UI', 10))
        style.configure("Card.TLabel", background=t['card'], foreground=t['text'])
        style.configure("Title.TLabel", font=('Segoe UI', 22, 'bold'), foreground=t['highlight'])
        style.configure("Subtitle.TLabel", font=('Segoe UI', 11), foreground=t['text_dim'])
        style.configure("Section.TLabel", font=('Segoe UI', 11, 'bold'), foreground=t['text'])
        style.configure("TButton", padding=10, font=('Segoe UI', 10))
        style.configure("Accent.TButton", background=t['highlight'], foreground='white')
        style.configure("TProgressbar", thickness=12, troughcolor=t['accent'], background=t['highlight'])
        style.configure("TCombobox", fieldbackground=t['input_bg'], background=t['accent'])
        style.map("TButton", background=[('active', t['accent'])])

    def _create_ui(self):
        """Crea la interfaz de usuario - layout fijo compacto"""
        t = self.theme

        # Frame principal
        main = tk.Frame(self.root, bg=t['bg'], padx=8, pady=5)
        main.pack(fill=tk.BOTH, expand=True)

        # === HEADER (arriba) ===
        header = tk.Frame(main, bg=t['bg'])
        header.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        title_frame = tk.Frame(header, bg=t['bg'])
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="Video Analyzer", font=('Segoe UI', 14, 'bold', 'italic'),
                bg=t['bg'], fg=t['highlight']).pack(anchor='w')
        tk.Label(title_frame, text="Transcribe y analiza videos con IA local",
                bg=t['bg'], fg=t['text_dim'], font=('Segoe UI', 8)).pack(anchor='w')

        btn_frame = tk.Frame(header, bg=t['bg'])
        btn_frame.pack(side=tk.RIGHT)

        self.theme_btn = tk.Button(btn_frame, text="Tema", width=6,
                                   command=self._toggle_theme,
                                   bg=t['accent'], fg=t['text'], relief=tk.FLAT,
                                   font=('Segoe UI', 8), cursor='hand2')
        self.theme_btn.pack(side=tk.LEFT, padx=3)

        tk.Button(btn_frame, text="Ajustes", width=6,
                 command=self._open_settings,
                 bg=t['accent'], fg=t['text'], relief=tk.FLAT,
                 font=('Segoe UI', 8), cursor='hand2').pack(side=tk.LEFT)

        # === STATUS BAR (abajo - empaquetar PRIMERO) ===
        status = tk.Frame(main, bg=t['bg'])
        status.pack(side=tk.BOTTOM, fill=tk.X, pady=(3, 0))

        self.gpu_label = tk.Label(status, text="GPU: Verificando...",
                                  bg=t['bg'], fg=t['text_dim'], font=('Segoe UI', 8))
        self.gpu_label.pack(side=tk.LEFT)

        tk.Label(status, text=f"v{self.VERSION}",
                bg=t['bg'], fg=t['text_dim'], font=('Segoe UI', 8)).pack(side=tk.RIGHT)

        self.time_label = tk.Label(status, text="",
                                   bg=t['bg'], fg=t['text_dim'], font=('Segoe UI', 8))
        self.time_label.pack(side=tk.RIGHT, padx=15)

        # === FOOTER/BOTONES (abajo - empaquetar SEGUNDO) ===
        footer = tk.Frame(main, bg=t['bg'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 3))

        self.btn_process = tk.Button(footer,
                                     text="INICIAR ANALISIS",
                                     command=self._start_processing,
                                     bg='#e94560', fg='white',
                                     font=('Segoe UI', 9, 'bold'),
                                     width=14, pady=3,
                                     relief=tk.RAISED, cursor='hand2',
                                     activebackground='#d63850', activeforeground='white',
                                     disabledforeground='#888888')
        self.btn_process.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_cancel = tk.Button(footer,
                                    text="CANCELAR",
                                    command=self._cancel_processing,
                                    bg='#495057', fg='#adb5bd',
                                    font=('Segoe UI', 8),
                                    width=9, pady=3,
                                    relief=tk.RAISED, state=tk.DISABLED,
                                    disabledforeground='#6c757d',
                                    cursor='hand2')
        self.btn_cancel.pack(side=tk.LEFT)

        self.btn_open = tk.Button(footer,
                                  text="Abrir Reporte",
                                  command=self._open_report,
                                  bg='#17a2b8', fg='white',
                                  font=('Segoe UI', 8),
                                  width=10, pady=3,
                                  relief=tk.RAISED, state=tk.DISABLED,
                                  cursor='hand2')
        self.btn_open.pack(side=tk.RIGHT)

        # === CONTENIDO (2 columnas - empaquetar AL FINAL) ===
        content = tk.Frame(main, bg=t['bg'])
        content.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))

        # Columna izquierda
        left_col = tk.Frame(content, bg=t['bg'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self._create_video_card(left_col)
        self._create_progress_card(left_col)

        # Columna derecha
        right_col = tk.Frame(content, bg=t['bg'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self._create_config_card(right_col)
        self._create_result_card(right_col)

    def _create_card(self, parent, title, height=None):
        """Crea un frame estilo card muy compacto"""
        t = self.theme

        card = tk.Frame(parent, bg=t['card'], relief=tk.FLAT,
                       highlightbackground=t['border'], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=(height is None), pady=1)

        if height:
            card.configure(height=height)
            card.pack_propagate(False)

        # Header compacto
        header = tk.Frame(card, bg=t['card'])
        header.pack(fill=tk.X, padx=6, pady=(3, 1))
        tk.Label(header, text=title, font=('Segoe UI', 8, 'bold'),
                bg=t['card'], fg=t['text']).pack(side=tk.LEFT)

        # Content frame
        content = tk.Frame(card, bg=t['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 3))

        return content

    def _create_video_card(self, parent):
        """Card de seleccion de video"""
        t = self.theme
        content = self._create_card(parent, "VIDEO", height=115)

        # Drop zone
        self.drop_zone = tk.Frame(content, bg=t['accent'], relief=tk.FLAT,
                                  highlightbackground=t['border'], highlightthickness=2)
        self.drop_zone.pack(fill=tk.BOTH, expand=True)

        self.drop_label = tk.Label(self.drop_zone,
                                   text="Arrastra un video aqui\no haz clic para seleccionar",
                                   bg=t['accent'], fg=t['text_dim'],
                                   font=('Segoe UI', 10), justify=tk.CENTER)
        self.drop_label.pack(expand=True)

        # Bind click
        self.drop_zone.bind('<Button-1>', lambda e: self._select_video())
        self.drop_label.bind('<Button-1>', lambda e: self._select_video())

        # Info del video
        self.video_info = tk.Label(content, text="", bg=t['card'], fg=t['text'],
                                   font=('Segoe UI', 10))

    def _create_config_card(self, parent):
        """Card de configuracion rapida"""
        t = self.theme
        content = self._create_card(parent, "CONFIGURACION", height=145)

        # Idioma
        row = tk.Frame(content, bg=t['card'])
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text="Idioma del video:", bg=t['card'], fg=t['text'],
                font=('Segoe UI', 10), width=16, anchor='w').pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value=self.config['language'])
        lang_combo = ttk.Combobox(row, textvariable=self.language_var,
                                   values=list(LANGUAGES.keys()), width=10, state='readonly')
        lang_combo.pack(side=tk.LEFT)
        self.lang_name = tk.Label(row, text=LANGUAGES.get(self.config['language'], ''),
                                  bg=t['card'], fg=t['text_dim'], font=('Segoe UI', 9))
        self.lang_name.pack(side=tk.LEFT, padx=5)
        lang_combo.bind('<<ComboboxSelected>>', self._on_language_change)

        # Modelo Whisper
        row = tk.Frame(content, bg=t['card'])
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text="Modelo Whisper:", bg=t['card'], fg=t['text'],
                font=('Segoe UI', 10), width=16, anchor='w').pack(side=tk.LEFT)
        self.whisper_var = tk.StringVar(value=self.config['whisper_model'])
        ttk.Combobox(row, textvariable=self.whisper_var,
                     values=["tiny", "base", "small", "medium", "large"], width=10,
                     state='readonly').pack(side=tk.LEFT)

        # AI Provider & Model
        row = tk.Frame(content, bg=t['card'])
        row.pack(fill=tk.X, pady=3)
        provider = self.config.get('ai_provider', 'ollama')
        if provider == 'ollama':
            model_name = self.config['ollama_model']
        else:
            model_name = self.config.get('claude_model', 'claude')[:20]

        self.ai_provider_display = tk.Label(row, text=f"IA: {provider.title()}",
                                           bg=t['card'], fg=t['text'],
                                           font=('Segoe UI', 10), width=16, anchor='w')
        self.ai_provider_display.pack(side=tk.LEFT)
        self.ai_model_display = tk.Label(row, text=model_name,
                                         bg=t['card'], fg=t['text'],
                                         font=('Segoe UI', 9, 'bold'))
        self.ai_model_display.pack(side=tk.LEFT)

        # Carpeta salida
        row = tk.Frame(content, bg=t['card'])
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text="Carpeta salida:", bg=t['card'], fg=t['text'],
                font=('Segoe UI', 10), width=16, anchor='w').pack(side=tk.LEFT)
        self.output_display = tk.Label(row, text="(junto al video)",
                                       bg=t['card'], fg=t['text_dim'],
                                       font=('Segoe UI', 9))
        self.output_display.pack(side=tk.LEFT)

    def _create_progress_card(self, parent):
        """Card de progreso"""
        t = self.theme
        content = self._create_card(parent, "PROGRESO")

        # Barra de progreso principal
        prog_frame = tk.Frame(content, bg=t['card'])
        prog_frame.pack(fill=tk.X, pady=(0, 6))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(prog_frame, variable=self.progress_var,
                                             maximum=100, mode='determinate', length=300)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.progress_pct = tk.Label(prog_frame, text="0%", bg=t['card'], fg=t['text'],
                                     font=('Segoe UI', 10, 'bold'), width=5)
        self.progress_pct.pack(side=tk.RIGHT, padx=(10, 0))

        # Descripcion actual
        self.progress_text = tk.Label(content, text="Listo para procesar",
                                      bg=t['card'], fg=t['text_dim'],
                                      font=('Segoe UI', 9), anchor='w')
        self.progress_text.pack(fill=tk.X, pady=(0, 5))

        # Lista de pasos
        self.steps = [
            {"name": "Extraccion de audio", "key": "audio"},
            {"name": "Transcripcion con Whisper", "key": "transcribe"},
            {"name": "Generando resumen", "key": "summary"},
            {"name": "Extrayendo puntos clave", "key": "keypoints"},
            {"name": "Analisis detallado", "key": "analysis"},
            {"name": "Guardando reporte", "key": "save"}
        ]

        self.step_frames = []
        self.step_indicators = []
        self.step_status = []
        self.step_time_labels = []

        for i, step in enumerate(self.steps):
            row = tk.Frame(content, bg=t['card'])
            row.pack(fill=tk.X, pady=1)

            # Indicador
            indicator = tk.Label(row, text="[ ]", font=('Consolas', 9),
                               bg=t['card'], fg=t['text_dim'], width=4)
            indicator.pack(side=tk.LEFT)
            self.step_indicators.append(indicator)

            # Nombre
            tk.Label(row, text=f"{i+1}. {step['name']}", bg=t['card'], fg=t['text'],
                    font=('Segoe UI', 9), anchor='w').pack(side=tk.LEFT, padx=3)

            # Tiempo
            time_lbl = tk.Label(row, text="", bg=t['card'], fg=t['text_dim'],
                               font=('Segoe UI', 8))
            time_lbl.pack(side=tk.RIGHT)
            self.step_time_labels.append(time_lbl)

            # Status
            status = tk.Label(row, text="", bg=t['card'], fg=t['text_dim'],
                            font=('Segoe UI', 8), width=12, anchor='e')
            status.pack(side=tk.RIGHT, padx=3)
            self.step_status.append(status)

            self.step_frames.append(row)

    def _create_result_card(self, parent):
        """Card de resultado"""
        t = self.theme
        content = self._create_card(parent, "SALIDA")

        self.result_text = scrolledtext.ScrolledText(
            content,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg=t['input_bg'],
            fg=t['input_fg'],
            insertbackground=t['text'],
            selectbackground=t['accent'],
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def _bind_shortcuts(self):
        """Configura atajos de teclado"""
        self.root.bind('<Control-o>', lambda e: self._select_video())
        self.root.bind('<Return>', lambda e: self._start_processing() if not self.is_processing else None)
        self.root.bind('<Escape>', lambda e: self._cancel_processing() if self.is_processing else None)

    def _setup_dnd(self):
        """Configura drag and drop"""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            # Habilitar DnD en el drop zone
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind('<<Drop>>', self._on_drop)
        except ImportError:
            # Si no está instalado tkinterdnd2, solo usar click
            pass

    def _on_drop(self, event):
        """Maneja el evento de arrastrar y soltar"""
        # Limpiar el path (viene entre llaves en Windows)
        file_path = event.data.strip('{}')
        path = Path(file_path)

        # Verificar que sea un archivo de video
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.wmv', '.flv']
        if path.suffix.lower() in video_extensions:
            self._set_video(path)
        else:
            messagebox.showwarning("Advertencia", "Por favor arrastra un archivo de video válido")

    def _on_language_change(self, event=None):
        """Actualiza nombre del idioma"""
        lang = self.language_var.get()
        self.lang_name.config(text=LANGUAGES.get(lang, ''))

    def _toggle_theme(self):
        """Cambia entre tema claro y oscuro"""
        self.config['theme'] = 'light' if self.config['theme'] == 'dark' else 'dark'
        save_config(self.config)

        # Reiniciar UI
        for widget in self.root.winfo_children():
            widget.destroy()

        self._apply_theme()
        self._create_ui()
        self._bind_shortcuts()
        self._check_gpu()

    def _open_settings(self):
        """Abre dialogo de configuracion"""
        dialog = SettingsDialog(self.root, self.config, self.theme)
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            self.config.update(dialog.result)
            save_config(self.config)

            # Actualizar UI
            self.whisper_var.set(self.config['whisper_model'])

            # Actualizar display del proveedor y modelo de IA
            provider = self.config.get('ai_provider', 'ollama')
            if provider == 'ollama':
                model_name = self.config['ollama_model']
            else:
                model_name = self.config.get('claude_model', 'claude')[:20]

            self.ai_provider_display.config(text=f"IA: {provider.title()}")
            self.ai_model_display.config(text=model_name)

            if self.config['output_dir']:
                self.output_display.config(text=Path(self.config['output_dir']).name)

    def _check_gpu(self):
        """Verifica GPU disponible"""
        def check():
            try:
                import torch
                if torch.cuda.is_available():
                    name = torch.cuda.get_device_name(0)
                    mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    text = f"GPU: {name} ({mem:.1f}GB)"
                    color = self.theme['success']
                else:
                    text = "GPU: No disponible (usando CPU)"
                    color = self.theme['warning']
            except:
                text = "GPU: Error al verificar"
                color = self.theme['error']

            self.root.after(0, lambda: self.gpu_label.config(text=text, fg=color))

        threading.Thread(target=check, daemon=True).start()

    def _select_video(self):
        """Selecciona archivo de video"""
        path = filedialog.askopenfilename(
            title="Seleccionar Video",
            filetypes=[
                ("Videos", "*.mp4 *.avi *.mkv *.mov *.webm *.wmv *.flv"),
                ("Todos", "*.*")
            ]
        )
        if path:
            self._set_video(Path(path))

    def _set_video(self, path):
        """Configura el video seleccionado"""
        t = self.theme
        self.video_path = path

        # Actualizar drop zone
        self.drop_label.config(text=path.name, fg=t['text'])

        # Obtener duracion
        def get_duration():
            try:
                from moviepy import VideoFileClip
                video = VideoFileClip(str(path))
                self.video_duration = video.duration
                video.close()

                mins = int(self.video_duration // 60)
                secs = int(self.video_duration % 60)
                size_mb = path.stat().st_size / (1024 * 1024)

                info = f"Duracion: {mins}:{secs:02d} | Tamano: {size_mb:.1f} MB"
                self.root.after(0, lambda: self._show_video_info(info))
            except Exception as e:
                self.root.after(0, lambda: self._show_video_info(f"Error: {e}"))

        threading.Thread(target=get_duration, daemon=True).start()

        # Reset
        self._reset_progress()
        self.btn_open.config(state=tk.DISABLED)

    def _show_video_info(self, text):
        """Muestra info del video"""
        t = self.theme
        self.video_info.config(text=text)
        self.video_info.pack(fill=tk.X, pady=(5, 0))

    def _reset_progress(self):
        """Reinicia indicadores de progreso"""
        t = self.theme
        for i in range(len(self.steps)):
            self.step_indicators[i].config(text="[ ]", fg=t['text_dim'])
            self.step_status[i].config(text="")
            self.step_time_labels[i].config(text="")

        self.progress_var.set(0)
        self.progress_pct.config(text="0%")
        self.progress_text.config(text="Listo para procesar")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.step_times = {}

    def _update_step(self, index, status, message=""):
        """Actualiza estado de un paso"""
        t = self.theme

        def update():
            if status == "running":
                self.step_indicators[index].config(text="[>>]", fg=t['warning'])
                self.step_status[index].config(text="En progreso...", fg=t['warning'])
                self.step_times[index] = time.time()
            elif status == "completed":
                self.step_indicators[index].config(text="[OK]", fg=t['success'])
                self.step_status[index].config(text=message or "Completado", fg=t['success'])
                if index in self.step_times:
                    elapsed = time.time() - self.step_times[index]
                    self.step_time_labels[index].config(text=format_time(elapsed))
            elif status == "error":
                self.step_indicators[index].config(text="[X]", fg=t['error'])
                self.step_status[index].config(text=message[:20] or "Error", fg=t['error'])

            # Actualizar progreso general
            completed = sum(1 for ind in self.step_indicators if ind.cget('text') == "[OK]")
            pct = int((completed / len(self.steps)) * 100)
            self.progress_var.set(pct)
            self.progress_pct.config(text=f"{pct}%")

        self.root.after(0, update)

    def _update_progress_text(self, text):
        """Actualiza texto de progreso"""
        self.root.after(0, lambda: self.progress_text.config(text=text))

    def _append_result(self, text):
        """Agrega texto al resultado (solo lectura para usuario)"""
        def append():
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, text + "\n")
            self.result_text.see(tk.END)
            self.result_text.config(state=tk.DISABLED)
        self.root.after(0, append)

    def _start_processing(self):
        """Inicia procesamiento"""
        if not self.video_path:
            messagebox.showwarning("Advertencia", "Selecciona un video primero")
            return

        if not self.video_path.exists():
            messagebox.showerror("Error", f"Archivo no encontrado:\n{self.video_path}")
            return

        self.is_processing = True
        self._reset_progress()

        # Deshabilitar boton INICIAR y cambiar apariencia
        self.btn_process.config(state=tk.DISABLED, bg='#666666', text="PROCESANDO...")
        # Habilitar boton CANCELAR
        self.btn_cancel.config(state=tk.NORMAL, bg='#dc3545', fg='white')
        # Asegurar que Abrir Reporte este deshabilitado
        self.btn_open.config(state=tk.DISABLED)

        self.start_time = time.time()
        self._update_timer()

        # Guardar config actual (solo whisper y language, ya que AI provider se guarda en settings)
        self.config['whisper_model'] = self.whisper_var.get()
        self.config['language'] = self.language_var.get()
        save_config(self.config)

        threading.Thread(target=self._process_video, daemon=True).start()

    def _update_timer(self):
        """Actualiza timer"""
        if self.is_processing:
            elapsed = time.time() - self.start_time
            self.time_label.config(text=f"Tiempo: {format_time(elapsed)}")
            self.root.after(1000, self._update_timer)

    def _process_video(self):
        """Procesa el video"""
        try:
            import torch
            import whisper
            from moviepy import VideoFileClip
            import ollama

            cfg = self.config
            device = "cuda" if (cfg['use_gpu'] and torch.cuda.is_available()) else "cpu"

            self._append_result("=" * 50)
            self._append_result("INICIANDO ANALISIS")
            self._append_result("=" * 50)
            self._append_result(f"\nArchivo: {self.video_path.name}")
            self._append_result(f"Dispositivo: {device.upper()}")
            self._append_result(f"Whisper: {cfg['whisper_model']}")
            provider = cfg.get('ai_provider', 'ollama')
            if provider == 'ollama':
                self._append_result(f"IA: Ollama ({cfg['ollama_model']})\n")
            else:
                self._append_result(f"IA: Claude ({cfg.get('claude_model', 'sonnet')})\n")

            # === PASO 1: Audio ===
            self._update_step(0, "running")
            self._update_progress_text("Extrayendo audio del video...")

            # Usar el nombre del video para el archivo de audio
            audio_filename = f"{self.video_path.stem}_audio.mp3" if not cfg['delete_temp_audio'] else "temp_audio.mp3"
            audio_path = self.video_path.parent / audio_filename
            video = VideoFileClip(str(self.video_path))
            duration = video.duration
            video.audio.write_audiofile(str(audio_path))
            video.close()

            self._update_step(0, "completed", f"{duration/60:.1f} min")
            self._append_result(f"Audio extraido ({duration/60:.1f} min)")

            if not self.is_processing: return

            # === PASO 2: Transcribir ===
            self._update_step(1, "running")
            self._update_progress_text("Transcribiendo con Whisper...")
            self._append_result(f"\n[PASO 2/6] Cargando modelo Whisper '{cfg['whisper_model']}'...")

            model = whisper.load_model(cfg['whisper_model'], device=device)
            self._append_result(f"Modelo cargado. Iniciando transcripcion...")
            result = model.transcribe(str(audio_path), language=cfg['language'],
                                      fp16=(device == "cuda"))

            transcription = result["text"]
            segments = result["segments"]

            # Limpiar
            if cfg['delete_temp_audio']:
                audio_path.unlink(missing_ok=True)
            if device == "cuda":
                torch.cuda.empty_cache()
            del model

            self._update_step(1, "completed", f"{len(transcription)} chars")
            self._append_result(f"Transcripcion: {len(transcription)} caracteres")

            if not self.is_processing: return

            # === PASO 3: Resumen ===
            self._update_step(2, "running")
            self._update_progress_text("Generando resumen con IA...")
            self._append_result(f"\n[PASO 3/6] Generando resumen ejecutivo con {provider.title()}...")

            summary = self._query_ai(
                """IMPORTANTE: Responde UNICAMENTE en español.
Genera un RESUMEN EJECUTIVO conciso del siguiente contenido.
- Maximo 3 parrafos
- Lenguaje claro y profesional
- Captura la esencia del contenido""",
                transcription
            )
            self._update_step(2, "completed")
            self._append_result("Resumen generado")

            if not self.is_processing: return

            # === PASO 4: Puntos clave ===
            self._update_step(3, "running")
            self._update_progress_text("Extrayendo puntos clave...")
            self._append_result(f"\n[PASO 4/6] Extrayendo puntos clave del contenido...")

            key_points = self._query_ai(
                """IMPORTANTE: Responde UNICAMENTE en español.
Extrae los 8-10 PUNTOS CLAVE mas importantes del contenido.
- Usa vinetas (-)
- Se conciso pero informativo
- Ordena por relevancia""",
                transcription
            )
            self._update_step(3, "completed")
            self._append_result("Puntos clave extraidos")

            if not self.is_processing: return

            # === PASO 5: Analisis ===
            self._update_step(4, "running")
            self._update_progress_text("Generando analisis detallado...")
            self._append_result(f"\n[PASO 5/6] Generando analisis detallado del video...")

            analysis = self._query_ai(
                """IMPORTANTE: Responde UNICAMENTE en español.
Realiza un ANALISIS DETALLADO del contenido con la siguiente estructura:

## TEMA PRINCIPAL
Describe el tema central del contenido.

## IDEAS PRINCIPALES
Lista las ideas mas importantes con breve explicacion.

## ARGUMENTOS Y DATOS
Menciona argumentos, cifras o evidencias presentadas.

## CONCLUSIONES
Resume las conclusiones o llamados a accion.

## AUDIENCIA
A quien va dirigido este contenido.""",
                transcription
            )
            self._update_step(4, "completed")
            self._append_result("Analisis completado")

            if not self.is_processing: return

            # === PASO 6: Guardar ===
            self._update_step(5, "running")
            self._update_progress_text("Guardando reporte...")
            self._append_result(f"\n[PASO 6/6] Generando reporte final...")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Formato del reporte
            if cfg['output_format'] == 'json':
                import json
                report_content = json.dumps({
                    "file": self.video_path.name,
                    "date": timestamp,
                    "duration_min": duration / 60,
                    "summary": summary,
                    "key_points": key_points,
                    "analysis": analysis,
                    "transcription": transcription,
                    "segments": [{"start": s['start'], "text": s['text']} for s in segments]
                }, ensure_ascii=False, indent=2)
                ext = "json"
            else:
                report_content = f"""# ANALISIS DE VIDEO

**Archivo:** {self.video_path.name}
**Fecha:** {timestamp}
**Duracion:** {duration/60:.1f} minutos
**Modelos:** Whisper {cfg['whisper_model']} + {cfg['ollama_model']}

---

## RESUMEN EJECUTIVO

{summary}

---

## PUNTOS CLAVE

{key_points}

---

## ANALISIS DETALLADO

{analysis}

---

## TRANSCRIPCION COMPLETA

{transcription}

---

## TRANSCRIPCION CON TIMESTAMPS

"""
                for seg in segments:
                    mins = int(seg['start'] // 60)
                    secs = int(seg['start'] % 60)
                    report_content += f"[{mins:02d}:{secs:02d}] {seg['text'].strip()}\n"

                ext = "md" if cfg['output_format'] == 'md' else 'txt'

            # Determinar ruta de salida
            if cfg['output_dir']:
                output_dir = Path(cfg['output_dir'])
            else:
                output_dir = self.video_path.parent

            self.report_path = output_dir / f"{self.video_path.stem}_analisis.{ext}"
            self.report_path.write_text(report_content, encoding='utf-8')

            self._update_step(5, "completed")

            # Finalizar
            elapsed = time.time() - self.start_time
            self._update_progress_text(f"Completado en {format_time(elapsed)}")

            self._append_result("\n" + "=" * 50)
            self._append_result("ANALISIS COMPLETADO")
            self._append_result("=" * 50)
            self._append_result(f"\nReporte: {self.report_path}")
            self._append_result(f"Tiempo total: {format_time(elapsed)}")

            self.root.after(0, lambda: self.btn_open.config(state=tk.NORMAL))

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()

            # Mostrar en el panel
            self._append_result(f"\n\n{'='*50}")
            self._append_result("ERROR DURANTE EL PROCESAMIENTO")
            self._append_result(f"{'='*50}")
            self._append_result(f"\nError: {str(e)}")
            self._append_result(f"\nVer detalles completos en: error_log.txt")
            self._update_progress_text(f"Error: {str(e)[:40]}...")

            # Guardar log de error
            try:
                log_file = self.video_path.parent / "error_log.txt" if self.video_path else Path("error_log.txt")
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write(f"ERROR EN VIDEO ANALYZER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(f"Video: {self.video_path if self.video_path else 'N/A'}\n")
                    f.write(f"Configuracion:\n")
                    f.write(f"  - Whisper: {cfg.get('whisper_model', 'N/A')}\n")
                    f.write(f"  - AI Provider: {cfg.get('ai_provider', 'N/A')}\n")
                    f.write(f"  - GPU: {cfg.get('use_gpu', 'N/A')}\n\n")
                    f.write(f"ERROR:\n{error_details}\n")
            except:
                pass  # Si falla guardar el log, no es crítico

            # Marcar paso actual como error
            for i, ind in enumerate(self.step_indicators):
                if ind.cget('text') == "[>>]":
                    self._update_step(i, "error", str(e)[:20])
                    break

        finally:
            self.is_processing = False
            self.root.after(0, self._processing_finished)

    def _query_ai(self, instruction, text):
        """Consulta el proveedor de IA configurado (Ollama o Claude)"""
        cfg = self.config
        provider = cfg.get('ai_provider', 'ollama')

        if provider == 'claude':
            return self._query_claude(instruction, text)
        else:
            return self._query_ollama(instruction, text)

    def _query_claude(self, instruction, text):
        """Consulta Claude API"""
        cfg = self.config
        api_key = cfg.get('claude_api_key', '')

        if not api_key:
            raise ValueError("API Key de Claude no configurada. Ve a Ajustes > Configuracion Avanzada.")

        try:
            import anthropic
        except ImportError:
            raise ValueError("Instala el paquete 'anthropic': pip install anthropic")

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model=cfg.get('claude_model', 'claude-sonnet-4-5-20250929'),
            max_tokens=cfg.get('claude_max_tokens', 4096),
            temperature=cfg.get('claude_temp', 0.5),
            messages=[{
                "role": "user",
                "content": f"{instruction}\n\nTEXTO:\n{text}"
            }]
        )

        return message.content[0].text

    def _query_ollama(self, instruction, text):
        """Consulta Ollama"""
        import ollama
        cfg = self.config
        response = ollama.chat(
            model=cfg['ollama_model'],
            messages=[{
                "role": "user",
                "content": f"{instruction}\n\nTEXTO:\n{text}"
            }],
            options={
                "num_ctx": cfg['ollama_ctx'],
                "temperature": cfg['ollama_temp'],
                "num_gpu": 99
            }
        )
        return response["message"]["content"]

    def _processing_finished(self):
        """Restaura UI despues del procesamiento"""
        # Restaurar boton INICIAR
        self.btn_process.config(state=tk.NORMAL, bg='#e94560', text="INICIAR ANALISIS")
        # Deshabilitar boton CANCELAR
        self.btn_cancel.config(state=tk.DISABLED, bg='#495057', fg='#adb5bd')

    def _cancel_processing(self):
        """Cancela procesamiento"""
        self.is_processing = False
        self._update_progress_text("Cancelado")
        self._append_result("\n--- CANCELADO ---")

    def _open_report(self):
        """Abre previsualizador del reporte"""
        if hasattr(self, 'report_path') and self.report_path.exists():
            self._show_report_preview()

    def _show_report_preview(self):
        """Muestra ventana de previsualizacion del reporte"""
        t = self.theme

        # Crear ventana
        preview = tk.Toplevel(self.root)
        preview.title(f"Reporte: {self.report_path.name}")
        preview.geometry("900x700")
        preview.configure(bg='#1e1e1e')

        # Centrar
        preview.update_idletasks()
        x = (preview.winfo_screenwidth() - 900) // 2
        y = (preview.winfo_screenheight() - 700) // 2
        preview.geometry(f"+{x}+{y}")

        # Frame principal
        main = tk.Frame(preview, bg='#1e1e1e', padx=15, pady=15)
        main.pack(fill=tk.BOTH, expand=True)

        # Header con titulo y botones
        header = tk.Frame(main, bg='#1e1e1e')
        header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(header, text=self.report_path.name,
                font=('Segoe UI', 14, 'bold'), bg='#1e1e1e', fg='white').pack(side=tk.LEFT)

        # Boton abrir con app externa
        tk.Button(header, text="Abrir Externo",
                 command=lambda: os.startfile(self.report_path),
                 bg='#0d6efd', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.RAISED, width=12, cursor='hand2').pack(side=tk.RIGHT, padx=5)

        # Boton copiar ruta
        tk.Button(header, text="Copiar Ruta",
                 command=lambda: self._copy_to_clipboard(str(self.report_path)),
                 bg='#6c757d', fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.RAISED, width=12, cursor='hand2').pack(side=tk.RIGHT, padx=5)

        # Area de texto con scroll
        text_frame = tk.Frame(main, bg='#1e1e1e')
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Texto con formato
        text_widget = tk.Text(text_frame,
                             wrap=tk.WORD,
                             font=('Consolas', 10),
                             bg='#0d1117',
                             fg='#c9d1d9',
                             insertbackground='white',
                             selectbackground='#264f78',
                             relief=tk.FLAT,
                             padx=15,
                             pady=15,
                             yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Cargar y formatear contenido
        content = self.report_path.read_text(encoding='utf-8')

        # Configurar tags para formato
        text_widget.tag_configure('h1', font=('Segoe UI', 18, 'bold'), foreground='#e94560')
        text_widget.tag_configure('h2', font=('Segoe UI', 14, 'bold'), foreground='#58a6ff')
        text_widget.tag_configure('h3', font=('Segoe UI', 12, 'bold'), foreground='#7ee787')
        text_widget.tag_configure('bold', font=('Consolas', 10, 'bold'), foreground='#ffa657')
        text_widget.tag_configure('separator', foreground='#484f58')
        text_widget.tag_configure('timestamp', foreground='#8b949e')
        text_widget.tag_configure('normal', font=('Consolas', 10), foreground='#c9d1d9')

        # Insertar contenido con formato basico
        for line in content.split('\n'):
            if line.startswith('# '):
                text_widget.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.startswith('## '):
                text_widget.insert(tk.END, '\n' + line[3:] + '\n', 'h2')
            elif line.startswith('### '):
                text_widget.insert(tk.END, line[4:] + '\n', 'h3')
            elif line.startswith('**') and line.endswith('**'):
                text_widget.insert(tk.END, line.strip('*') + '\n', 'bold')
            elif line.startswith('---'):
                text_widget.insert(tk.END, '─' * 60 + '\n', 'separator')
            elif line.startswith('['):
                text_widget.insert(tk.END, line + '\n', 'timestamp')
            else:
                text_widget.insert(tk.END, line + '\n', 'normal')

        # Solo lectura
        text_widget.config(state=tk.DISABLED)

        # Footer con info
        footer = tk.Frame(main, bg='#1e1e1e')
        footer.pack(fill=tk.X, pady=(10, 0))

        file_size = self.report_path.stat().st_size / 1024
        tk.Label(footer, text=f"Ubicacion: {self.report_path.parent}",
                font=('Segoe UI', 9), bg='#1e1e1e', fg='#8b949e').pack(side=tk.LEFT)
        tk.Label(footer, text=f"Tamano: {file_size:.1f} KB",
                font=('Segoe UI', 9), bg='#1e1e1e', fg='#8b949e').pack(side=tk.RIGHT)

    def _copy_to_clipboard(self, text):
        """Copia texto al portapapeles"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def run(self):
        """Ejecuta la aplicacion"""
        self.root.mainloop()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    app = VideoAnalyzerGUI()
    app.run()
