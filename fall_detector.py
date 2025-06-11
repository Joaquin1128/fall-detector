import cv2
import mediapipe as mp
from time import time, strftime
import argparse
import os
import winsound

FALL_DIR = "falls"

def detectPose(frame, pose_model, display=True):
    modified_frame = frame.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_model.process(frame_rgb)
    height, width, _ = frame.shape
    landmarks = []

    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), landmark.z * width))

        connections = mp.solutions.pose.POSE_CONNECTIONS
        for connection in connections:
            start, end = connection
            if start < len(landmarks) and end < len(landmarks):
                cv2.line(modified_frame, (landmarks[start][0], landmarks[start][1]),
                         (landmarks[end][0], landmarks[end][1]), (0, 255, 0), 2)
    else:
        return None, None

    if display:
        cv2.imshow('Pose Landmarks', modified_frame)

    return modified_frame, landmarks

def detectFall(landmarks, previous_avg_shoulder_height):
    if len(landmarks) < 25:
        return False, previous_avg_shoulder_height

    left_shoulder_y = landmarks[11][1]
    right_shoulder_y = landmarks[12][1]
    left_hip_y = landmarks[23][1]
    right_hip_y = landmarks[24][1]

    avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
    avg_hip_y = (left_hip_y + right_hip_y) / 2

    if previous_avg_shoulder_height == 0:
        previous_avg_shoulder_height = avg_shoulder_y
        return False, previous_avg_shoulder_height

    fall_threshold = previous_avg_shoulder_height * 1.5
    horizontal_threshold = 50

    if avg_shoulder_y > fall_threshold or abs(avg_shoulder_y - avg_hip_y) < horizontal_threshold:
        previous_avg_shoulder_height = avg_shoulder_y
        return True, previous_avg_shoulder_height

    previous_avg_shoulder_height = avg_shoulder_y
    return False, previous_avg_shoulder_height

def logFallEvent(frame, timestamp):
    os.makedirs(FALL_DIR, exist_ok=True)

    safe_timestamp = timestamp.replace(":", "-").replace(" ", "_")
    image_path = os.path.join(FALL_DIR, f'fall_{safe_timestamp}.jpg')
    log_path = os.path.join(FALL_DIR, 'fall_log.txt')

    cv2.imwrite(image_path, frame)

    with open(log_path, "a") as log_file:
        log_file.write(f'Caída detectada el {timestamp}\n')

    winsound.Beep(1000, 500)

def main(video_path):
    if not os.path.isfile(video_path):
        print(f"El archivo '{video_path}' no existe.")
        return

    pose_model = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.7, model_complexity=2)
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"No se pudo abrir el video: {video_path}")
        return

    previous_avg_shoulder_height = 0
    time_prev_check = 0

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("No hay más frames o no se pudo leer el video.")
            break

        modified_frame, landmarks = detectPose(frame, pose_model, display=True)

        time_now = time()

        if (time_now - time_prev_check) > 2:
            if landmarks:
                fall_detected, previous_avg_shoulder_height = detectFall(landmarks, previous_avg_shoulder_height)
                if fall_detected:
                    timestamp = strftime('%Y-%m-%d %H:%M:%S')
                    print(f"¡Caída detectada! ({timestamp})")
                    logFallEvent(frame, timestamp)
            time_prev_check = time_now

        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detector de caídas usando un archivo de video.")
    parser.add_argument('--video', type=str, required=True, help='Ruta al archivo de video')
    args = parser.parse_args()

    main(args.video)
