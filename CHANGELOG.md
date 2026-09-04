# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

## [1.0.0] - 2026-09-04

### Added
- Soporte para Claude AI (Anthropic) con modelos Sonnet 4.5, Opus 4.5, 3.5 Sonnet y 3.5 Haiku.
- Selector dinámico de proveedor de IA (Ollama local / Claude API).
- Manejo seguro de credenciales: API Key obtenida mediante la UI (en memoria de sesión) sin exponer datos sensibles en disco, con soporte para variable de entorno `ANTHROPIC_API_KEY`.
- Sistema de caché de transcripción para recuperación y reanudación automática sin reprocesar audio.
- Detección automática del modelo Whisper recomendado según la VRAM del sistema.
- Control avanzado de temperatura y límite de tokens para Claude y Ollama.
- Soporte Drag & Drop para carga directa de videos en la interfaz.
- Previsualizador integrado de reportes Markdown en la ventana principal.
- Función de limpieza de caché y temporales desde la GUI.
- Documentación de configuración recomendada (`CONFIGURACION_RECOMENDADA.md`).
- Licencia MIT a nombre de Yasmany Reyes Gonzalez.

### Changed
- Interfaz gráfica rediseñada con componentes tipo card y temas Dark y Light.
- Rutas de audio temporal generadas por hash/nombre de video para evitar colisiones.
- Dependencias con versiones mínimas fijadas en `requirements.txt` para compilaciones reproducibles.
- Tipado estático (type hints) en métodos públicos de `analyzer.py`.
- Ignorado de archivos de depuración y temporales (`*_temp_audio.mp3`, `error_log.txt`, `*_cache.json`).

### Fixed
- Corrección de modelo mostrado en encabezado de reporte cuando el proveedor activo es Claude.
- Sustitución de 9 cláusulas `except:` genéricas por captura de excepciones específicas.
- Eliminación de importaciones redundantes (`json` en procesamiento).
- Visibilidad condicional de campos de configuración según el proveedor de IA activo.

## [0.1.0] - 2024-05-10

### Added
- Lanzamiento inicial con OpenAI Whisper y Ollama local.
- Extracción de audio y transcripción automática.
- Generación de resúmenes y puntos clave estructurados.
