import cv2
import mediapipe as mp
from time import time
import sys

previous_avg_shoulder_height = 0

def detectPose(frame, pose_model, display=True):
    modified_frame = frame.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose_model.process(frame_rgb)
    height, width, _ = frame.shape
    landmarks = []
    
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))
        
        connections = mp.solutions.pose.POSE_CONNECTIONS
        for connection in connections:
            start_point = connection[0]
            end_point = connection[1]
            cv2.line(modified_frame, (landmarks[start_point][0], landmarks[start_point][1]),
                     (landmarks[end_point][0], landmarks[end_point][1]), (0, 255, 0), 3)
    else:
        return None, None
    
    if display:
        cv2.imshow('Pose Landmarks', modified_frame)
    
    return modified_frame, landmarks

def detectFall(landmarks, previous_avg_shoulder_height):
    left_shoulder_y = landmarks[11][1]
    right_shoulder_y = landmarks[12][1]
    
    avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2

    if previous_avg_shoulder_height == 0:
        previous_avg_shoulder_height = avg_shoulder_y
        return False, previous_avg_shoulder_height
    
    fall_threshold = previous_avg_shoulder_height * 1.5
    
    if avg_shoulder_y > fall_threshold:
        previous_avg_shoulder_height = avg_shoulder_y
        return True, previous_avg_shoulder_height
    else:
        previous_avg_shoulder_height = avg_shoulder_y
        return False, previous_avg_shoulder_height

def main(video_path=0):
    global previous_avg_shoulder_height

    pose_model = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.7, model_complexity=2)
    video = cv2.VideoCapture(video_path)
    time1 = 0
    fall_detected = False

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("No hay mas frames o no se pudo abrir el video.")
            break

        modified_frame, landmarks = detectPose(frame, pose_model, display=True)

        time2 = time()

        if (time2 - time1) > 2:
            if landmarks is not None:
                fall_detected, previous_avg_shoulder_height = detectFall(landmarks, previous_avg_shoulder_height)
                if fall_detected:
                    print("Caida detectada!")
            time1 = time2

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Si paso argumento, uso ese como video, sino la webcam (0)
    video_source = sys.argv[1] if len(sys.argv) > 1 else 0
    main(video_source)
