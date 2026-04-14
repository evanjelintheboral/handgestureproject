import cv2
import mediapipe as mp
import pyautogui
import time
import math
print("STARTED FILE")
# Mediapipe setup (optimized)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Check camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Screen size
screen_w, screen_h = pyautogui.size()

# Cooldowns
last_click_time = 0
last_scroll_time = 0
last_screenshot_time = 0

click_delay = 0.5
scroll_delay = 0.2
screenshot_delay = 2

print("Hand Gesture Control Started... Press 'q' to exit")

while True:
    success, img = cap.read()

    #  Prevent sudden close
    if not success:
        print("Frame dropped, retrying...")
        continue

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark
            thumb_tip = lm[4]
            index_tip = lm[8]

            # =========================
            #  FINGER DETECTION
            # =========================
            fingers = []

            # Thumb
            fingers.append(1 if thumb_tip.x < lm[3].x else 0)

            # Other fingers
            for tip in [8, 12, 16, 20]:
                fingers.append(1 if lm[tip].y < lm[tip - 2].y else 0)

            current_time = time.time()

            # =========================
            #  CURSOR MOVE
            # =========================
            if fingers == [0,1,0,0,0]:
                x = int(index_tip.x * screen_w)
                y = int(index_tip.y * screen_h)
                pyautogui.moveTo(x, y, duration=0.02)
                cv2.putText(img, "Move", (10,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # =========================
            #  CLICK
            # =========================
            dist = math.hypot(thumb_tip.x - index_tip.x,
                              thumb_tip.y - index_tip.y)

            if dist < 0.05 and current_time - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = current_time
                cv2.putText(img, "Click", (10,90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            # =========================
            #  SCROLL UP (2 fingers)
            # =========================
            if fingers == [0,1,1,0,0] and current_time - last_scroll_time > scroll_delay:
                pyautogui.scroll(60)
                last_scroll_time = current_time
                cv2.putText(img, "Scroll Up", (10,130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # =========================
            #  SCROLL DOWN (3 fingers)
            # =========================
            elif fingers == [0,1,1,1,0] and current_time - last_scroll_time > scroll_delay:
                pyautogui.scroll(-60)
                last_scroll_time = current_time
                cv2.putText(img, "Scroll Down", (10,130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # =========================
            #  SCREENSHOT
            # =========================
            if fingers == [0,0,0,0,0] and current_time - last_screenshot_time > screenshot_delay:
                pyautogui.screenshot(f"screenshot_{int(current_time)}.png")
                last_screenshot_time = current_time
                cv2.putText(img, "Screenshot", (10,170),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)

    cv2.imshow("Hand Gesture Mouse", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 🔒 Prevent CPU overload
    time.sleep(0.01)

cap.release()
cv2.destroyAllWindows()
