import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Tasks imports
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)
landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

canvas = None
palette = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(0,0,0)]
color_index=0
labels=["Blue","Green","Red","Yellow","Eraser"]
brush_thickness=3
eraser_thickness=80
prev_x, prev_y = 0,0
save_counter=1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # --- DRAW UI PALETTE ---
    for i, color in enumerate(palette):
        x_start = i * 100
        x_end = (i + 1) * 100
        cv2.rectangle(frame, (x_start, 0), (x_end, 100), color, -1)
        cv2.putText(frame, labels[i], (x_start + 10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255) if i != 4 else (200, 200, 200), 2)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect(mp_image)

    # --- HAND TRACKING & DRAWING LOGIC ---
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:

            # 1. Convert landmarks to pixel coordinates
            lm_list = []
            for id, lm in enumerate(hand_landmarks):
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            index_x, index_y = lm_list[8]  # Index Finger Tip
            middle_x, middle_y = lm_list[12]  # Middle Finger Tip
            middle_mcp_y = lm_list[10][1]  # Middle Finger Knuckle

            # Check if middle finger is UP
            middle_is_up = middle_y < middle_mcp_y

            # --- STATE MACHINE ---
            # STATE 1: UI and Color Selection Zone
            if index_y <= 100:
                color_index = int(min(index_x // 100, len(palette) - 1))
                prev_x, prev_y = 0, 0  # Lift pen

            # STATE 2: PAUSE / HOVER MODE (Middle finger is UP)
            elif middle_is_up:
                prev_x, prev_y = 0, 0  # Lift the pen
                cv2.circle(frame, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)  # Pink cursor

            # STATE 3: DRAWING MODE (Only Index finger is UP)
            else:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = index_x, index_y

                # Draw with selected color/eraser
                if color_index == len(palette) - 1:  # Eraser
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), (0, 0, 0), eraser_thickness)
                else:  # Brush
                    cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), palette[color_index], brush_thickness)

                prev_x, prev_y = index_x, index_y
                cv2.circle(frame, (index_x, index_y), 10, (0, 215, 255), cv2.FILLED)  # Gold cursor

            # --- SKELETON DRAWING ---
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
                (5, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
                (9, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
                (13, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                (0, 17), (5, 9), (9, 13), (13, 17)  # Base of palm/knuckles
            ]

            # Lines (Cyan)
            for p1, p2 in connections:
                x1, y1 = lm_list[p1]
                x2, y2 = lm_list[p2]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

            # Dots (White)
            for lm in hand_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 255, 255), cv2.FILLED)

    else:
        # Lift pen if hand is totally off-screen
        prev_x, prev_y = 0, 0

    # --- DISPLAY SIDES-BY-SIDE ---
    combined = np.hstack((frame, canvas))
    cv2.imshow("Hand Drawing", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("c"):  # Added this back so you can clear the canvas with 'c'!
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
cap.release()
cv2.destroyAllWindows()