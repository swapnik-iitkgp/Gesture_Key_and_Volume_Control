# import cv2
# import mediapipe as mp
# import pyautogui
# cap = cv2.VideoCapture(0)
# hand_detector = mp.solutions.hands.Hands()
# drawing_utils = mp.solutions.drawing_utils
# screen_width, screen_height = pyautogui.size()
# index_y = 0
# while True:
#     _, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#     frame_height, frame_width, _ = frame.shape
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = hand_detector.process(rgb_frame)
#     hands = output.multi_hand_landmarks
#     if hands:
#         for hand in hands:
#             drawing_utils.draw_landmarks(frame, hand)
#             landmarks = hand.landmark
#             for id, landmark in enumerate(landmarks):
#                 x = int(landmark.x*frame_width)
#                 y = int(landmark.y*frame_height)
#                 if id == 8:
#                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
#                     index_x = screen_width/frame_width*x
#                     index_y = screen_height/frame_height*y

#                 if id == 4:
#                     cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
#                     thumb_x = screen_width/frame_width*x
#                     thumb_y = screen_height/frame_height*y
#                     print('outside', abs(index_y - thumb_y))
#                     if abs(index_y - thumb_y) < 20:
#                         pyautogui.click()
#                         pyautogui.sleep(1)
#                     elif abs(index_y - thumb_y) < 100:
#                         pyautogui.moveTo(index_x, index_y)
#     cv2.imshow('Virtual Mouse', frame)
#     cv2.waitKey(1)


import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_x, index_y = 0, 0
prev_index_x, prev_index_y = 0, 0
cursor_speed = 10

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    distance = abs(index_y - thumb_y)
                    if distance < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif distance < 100:
                        # Calculate cursor movement based on speed
                        cursor_dx = (index_x - prev_index_x) / cursor_speed
                        cursor_dy = (index_y - prev_index_y) / cursor_speed

                        # Update the cursor position
                        cursor_x, cursor_y = pyautogui.position()
                        cursor_x += cursor_dx
                        cursor_y += cursor_dy

                        # Move the cursor within the screen bounds
                        cursor_x = max(0, min(cursor_x, screen_width))
                        cursor_y = max(0, min(cursor_y, screen_height))

                        # Move the cursor
                        pyautogui.moveTo(cursor_x, cursor_y)

                        # Update the previous cursor position
                        prev_index_x, prev_index_y = index_x, index_y

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

