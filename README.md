# 🛑 Detector de Caídas

Este proyecto permite detectar caídas humanas en videos mediante el análisis de posturas corporales usando [MediaPipe Pose](https://developers.google.com/mediapipe) de Google. Es especialmente útil para monitorear situaciones de riesgo como caídas en adultos mayores, accidentes domésticos o incidentes en espacios públicos.

El sistema identifica variaciones bruscas en la postura, emite alertas, guarda evidencia visual y registra el evento para su posterior análisis.

---

## 📦 Requisitos

- Python 3.7 o superior  
- OpenCV  
- MediaPipe  
- Windows (para emitir alertas sonoras con `winsound`)  

---

## 📥 Instalación

Cloná este repositorio y asegurate de instalar todas las dependencias necesarias:

```bash
git clone https://github.com/Joaquin1128/fall-detector.git
cd fall-detector
pip install -r requirements.txt
```

---

## ▶️ Uso

Para ejecutar la detección de caídas en un video:

```bash
python fall-detector.py --video ruta/del/video.mp4
```

📌 **Ejemplo:**

```bash
python fall-detector.py --video videos/video1.mp4
```

El proyecto incluye **4 videos de ejemplo** dentro de la carpeta `videos/`:  
- `video1.mp4`  
- `video2.mp4`  
- `video3.mp4`  
- `video4.mp4`

---

## 📁 ¿Qué genera el sistema?

Cuando el sistema detecta una caída, realiza las siguientes acciones automáticamente:

- 🔊 **Alerta sonora:** emite un beep para notificar el evento.  
- 📸 **Captura de pantalla:** guarda una imagen del frame en la carpeta `falls/` con el nombre:  
  `fall_YYYY-MM-DD_HH-MM-SS.jpg`  
- 📝 **Registro del evento:** agrega una línea en el archivo `falls/fall_log.txt` con la fecha y hora del incidente:  
  `Caída detectada el 2025-06-10 21:35:48`

---

## 🧠 ¿Cómo se detectan las caídas?

La lógica de detección se basa en los **landmarks** (puntos clave del cuerpo) que proporciona **MediaPipe Pose**.  
El sistema:

1. Detecta la posición de los hombros y caderas en cada frame.  
2. Calcula la altura promedio de los hombros.  
3. Compara esa altura con la de unos segundos atrás.  
4. Si la diferencia excede un umbral definido (por ejemplo, 1.5x), o si los hombros están muy cerca de las caderas (indicando que el cuerpo está horizontal), se considera una **posible caída**.

---

## 📈 Posibles Aplicaciones

- Monitoreo de **adultos mayores** en hogares o residencias  
- **Vigilancia** en hospitales o centros de salud  
- Supervisión de **áreas laborales de riesgo**  
- Integración con sistemas de **seguridad inteligentes**

---

## ⚠️ Limitaciones

- El modelo puede fallar si la persona está parcialmente oculta o fuera del campo de visión.  
- Requiere videos con buena iluminación y calidad razonable.  
- Actualmente solo funciona en sistemas Windows (por el módulo `winsound`).  

---

## ✅ Próximas mejoras sugeridas

- Soporte multiplataforma (Linux/Mac)  
- Notificaciones por email o mensajería  
- Entrenamiento de modelo personalizado con IA  
- Detección en tiempo real desde cámaras web
