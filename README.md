# 🛑 Detección de Caídas con MediaPipe

Este proyecto detecta caídas humanas en videos utilizando [MediaPipe Pose](https://developers.google.com/mediapipe) de Google. Analiza los movimientos corporales en tiempo real, detecta descensos bruscos en la posición de los hombros y registra automáticamente posibles caídas mediante capturas de pantalla y logs.

## 📦 Requisitos

- Python 3.7 o superior  
- OpenCV  
- MediaPipe  

## 📥 Instalación

Cloná el repositorio y asegurate de instalar las dependencias necesarias:

```bash
git clone https://github.com/tu_usuario/fall-detection-mediapipe.git
cd fall-detection-mediapipe
pip install -r requirements.txt
```

## ▶️ Uso

🎥 Para ejecutar la detección en un video:

```bash
python fall-detector.py --video video.mp4
```
Reemplazá video.mp4 con la ruta del archivo de video que quieras analizar. El proyecto incluye dos videos de ejemplo: video1.mp4 y video2.mp4.

## 📁 Qué genera el sistema

Cuando se detecta una caída, el sistema realiza automáticamente lo siguiente:

- 🔊 Emite una alerta sonora
- 📸 Guarda una captura del frame en la carpeta falls/ con el nombre: fall_YYYY-MM-DD_HH-MM-SS.jpg
- 📝 Escribe una entrada en el archivo falls/fall_log.txt con la marca de tiempo, por ejemplo: Caída detectada el 2025-06-10 21:35:48

## 🧠 ¿Cómo se detectan las caídas?

- Utiliza los landmarks corporales proporcionados por MediaPipe Pose
- Calcula la altura promedio de ambos hombros en tiempo real
- Compara la altura actual con la de unos segundos atrás
- Si se detecta una disminución brusca mayor a un umbral predefinido (por ejemplo, 1.5 veces), se considera una caída
