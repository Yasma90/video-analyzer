# Configuraciones Recomendadas - Video Analyzer v2.1

Esta guía te ayudará a elegir la configuración óptima según tu hardware y necesidades.

## 🖥️ Configuración según Hardware

### GPU NVIDIA con 10GB+ VRAM (RTX 3080, RTX 4090, A6000)
**Rendimiento Máximo**

```
Whisper: large
AI Provider: Ollama (local) o Claude (mejor calidad)
Modelo Ollama: llama3.1:70b o mixtral:8x7b
Modelo Claude: claude-opus-4-5-20251101
GPU: ✅ Activado
Context Window: 16384
Temperature: 0.7
```

**Velocidad:** ~5-8 min por hora de video
**Calidad:** Excelente
**Costo:** Gratis (Ollama) / $$$ (Claude Opus)

---

### GPU NVIDIA con 6-10GB VRAM (RTX 3060, RTX 4060, A4000)
**Balance Óptimo**

```
Whisper: medium
AI Provider: Claude o Ollama
Modelo Ollama: llama3.1:8b o mistral
Modelo Claude: claude-sonnet-4-5-20250929
GPU: ✅ Activado
Context Window: 8192
Temperature: 0.7
```

**Velocidad:** ~3-5 min por hora de video
**Calidad:** Muy buena
**Costo:** Gratis (Ollama) / $ (Claude Sonnet)
**⭐ RECOMENDADO** para la mayoría de usuarios

---

### GPU NVIDIA con 4-6GB VRAM (GTX 1660, RTX 3050, RTX A500)
**Equilibrado**

```
Whisper: small
AI Provider: Ollama
Modelo Ollama: llama3.1:8b o llama2
GPU: ✅ Activado
Context Window: 8192
Temperature: 0.7
```

**Velocidad:** ~2-3 min por hora de video
**Calidad:** Buena
**Costo:** Gratis

---

### CPU / GPU con <4GB VRAM
**Modo CPU Eficiente**

```
Whisper: base o tiny
AI Provider: Claude (recomendado) u Ollama
Modelo Ollama: llama2
Modelo Claude: claude-3-5-haiku-20241022
GPU: ❌ Desactivado
Context Window: 4096
Temperature: 0.7
```

**Velocidad:** ~10-20 min por hora de video (CPU)
**Calidad:** Aceptable
**Costo:** Gratis (Ollama) / muy económico (Claude Haiku)

---

## 🎯 Configuración según Objetivo

### Máxima Calidad (Análisis Profesional)

```
Whisper: large o medium
AI Provider: Claude
Modelo Claude: claude-opus-4-5-20251101
GPU: ✅ Activado (si disponible)
Context Window: 16384
Temperature: 0.3-0.5 (más preciso)
Formato Salida: md
```

**Ideal para:** Análisis técnicos, investigación, transcripciones legales

---

### Máxima Velocidad (Procesamiento Rápido)

```
Whisper: tiny o base
AI Provider: Ollama
Modelo Ollama: llama2
GPU: ✅ Activado
Context Window: 4096
Temperature: 0.7
Eliminar audio: ✅ Activado
```

**Ideal para:** Análisis rápidos, múltiples videos, pruebas

---

### Balance Costo/Calidad (Uso Regular)

```
Whisper: small
AI Provider: Ollama para uso frecuente / Claude para contenido importante
Modelo Ollama: llama3.1:8b
Modelo Claude: claude-sonnet-4-5-20250929
GPU: ✅ Activado
Context Window: 8192
Temperature: 0.7
```

**Ideal para:** Uso diario, análisis de reuniones, contenido educativo

---

### Contenido Técnico/Código

```
Whisper: medium o large
AI Provider: Claude
Modelo Claude: claude-sonnet-4-5-20250929
GPU: ✅ Activado
Context Window: 16384
Temperature: 0.2 (más determinístico)
Idioma: en (si el video es en inglés)
```

**Ideal para:** Tutoriales de programación, charlas técnicas

---

## 📝 Parámetros Avanzados Explicados

### Temperature (0.0 - 1.0)

- **0.0 - 0.3:** Respuestas más precisas y determinísticas
  - Ideal para: Contenido técnico, legal, académico

- **0.4 - 0.7:** Balance entre creatividad y precisión
  - Ideal para: Uso general, reuniones, contenido educativo
  - ⭐ **Valor por defecto recomendado**

- **0.8 - 1.0:** Respuestas más creativas y variadas
  - Ideal para: Contenido artístico, brainstorming

### Context Window

- **4096:** Mínimo, para textos cortos
- **8192:** Recomendado para videos de hasta 30 min
- **16384:** Para videos largos (>30 min) o análisis detallado
- **32768:** Para videos muy largos (>1 hora) - solo si tu modelo lo soporta

### Idioma

- Selecciona el idioma del **contenido del video**, no tu idioma preferido
- Whisper detecta automáticamente, pero especificarlo mejora la precisión
- Para videos multiidioma, usa el idioma predominante

---

## 💡 Tips de Optimización

### 1. Gestión de Memoria GPU

Si recibes errores de CUDA/memoria:
- Reduce el modelo Whisper (ej: medium → small)
- Cierra otras aplicaciones que usen GPU
- Reduce Context Window

### 2. Velocidad de Procesamiento

Para acelerar:
- Usa modelo Whisper más pequeño
- Reduce Context Window a 4096
- Activa "Eliminar audio temporal"
- Usa Ollama en lugar de Claude API

### 3. Calidad de Transcripción

Para mejorar:
- Usa modelo Whisper grande (medium/large)
- Especifica el idioma correcto
- Para audio de baja calidad, considera pre-procesar con audacity

### 4. Ahorro de Costos (con Claude)

- Usa Ollama para análisis preliminares
- Usa Claude Haiku para análisis simples
- Usa Claude Sonnet/Opus solo para contenido importante
- Considera reducir Context Window si no necesitas análisis de videos muy largos

---

## 🔧 Configuración Inicial Recomendada

**Primera vez usando la aplicación:**

1. **Detecta tu GPU:**
   - Abre la app y revisa el indicador "GPU:" en la esquina inferior izquierda

2. **Prueba con un video corto (<5 min):**
   ```
   Whisper: small
   AI Provider: Ollama
   Modelo: llama2 (debe estar instalado)
   ```

3. **Si funciona bien, aumenta gradualmente:**
   - Prueba con `medium` si tienes >5GB VRAM
   - Prueba modelos más grandes de Ollama
   - Experimenta con Claude si quieres mejor calidad

4. **Encuentra tu punto óptimo:**
   - Balance entre velocidad y calidad
   - Monitorea el uso de GPU/CPU
   - Ajusta según tus necesidades

---

## 📊 Comparativa de Modelos IA

### Ollama (Local - Gratis)

| Modelo | VRAM | Velocidad | Calidad | Español |
|--------|------|-----------|---------|---------|
| llama2 | ~4GB | Rápido | Buena | ⭐⭐⭐ |
| llama3.1:8b | ~6GB | Medio | Muy buena | ⭐⭐⭐⭐ |
| llama3.1:70b | ~40GB | Lento | Excelente | ⭐⭐⭐⭐⭐ |
| mistral | ~5GB | Rápido | Muy buena | ⭐⭐⭐⭐ |
| mixtral:8x7b | ~30GB | Medio | Excelente | ⭐⭐⭐⭐⭐ |

### Claude (API - Pago)

| Modelo | Velocidad | Calidad | Costo/1M tokens | Español |
|--------|-----------|---------|-----------------|---------|
| Haiku 3.5 | Muy rápido | Buena | $0.25/$1.25 | ⭐⭐⭐⭐ |
| Sonnet 3.5 | Rápido | Excelente | $3/$15 | ⭐⭐⭐⭐⭐ |
| Sonnet 4.5 | Medio | Superior | $3/$15 | ⭐⭐⭐⭐⭐ |
| Opus 4.5 | Lento | Máxima | $15/$75 | ⭐⭐⭐⭐⭐ |

*Precios aproximados para input/output respectivamente*

---

## ❓ FAQ - Configuración

**P: ¿Qué modelo Whisper debo usar?**
R: Depende de tu GPU. Usa la tabla de "Configuración según Hardware" arriba.

**P: ¿Ollama o Claude?**
R: Ollama si quieres gratis y local. Claude si quieres máxima calidad y no te importa pagar.

**P: ¿Puedo cambiar entre Ollama y Claude?**
R: Sí, en Ajustes → Configuración Avanzada → Proveedor IA

**P: ¿Cuánto cuesta usar Claude?**
R: Depende del modelo y longitud del video. Un video de 30 min puede costar $0.10-$0.50

**P: Mi análisis sale en inglés, ¿por qué?**
R: Verifica que el idioma esté en "es". Los prompts ya están optimizados para español.

**P: ¿Puedo usar modelos de Ollama no listados?**
R: Sí, simplemente escribe el nombre completo en el campo de modelo.

---

## 🚀 Siguiente Paso

Una vez hayas encontrado tu configuración óptima, puedes guardarla yendo a:

**Ajustes → Configuración Avanzada → GUARDAR**

La configuración se guardará automáticamente y se usará en futuros análisis.

¡Feliz análisis! 🎬✨
