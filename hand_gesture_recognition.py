"""
Hand Gesture Recognition using MediaPipe + OpenCV
--------------------------------------------------
Detects hand landmarks from your webcam and classifies
common gestures in real time.

Install dependencies:
    pip install opencv-python mediapipe

Run:
    python hand_gesture_recognition.py
"""

import cv2
import mediapipe as mp

# ── MediaPipe setup ──────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles

# ── Finger tip / pip landmark indices ────────────────────────────────────────
TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
PIPS = [3, 6, 10, 14, 18]   # proximal interphalangeal joints (one below tip)

# ── Gesture classifier ────────────────────────────────────────────────────────
def fingers_up(landmarks):
    """
    Returns a list of 5 booleans [thumb, index, middle, ring, pinky]
    indicating whether each finger is extended.
    """
    lm = landmarks.landmark
    up = []

    # Thumb: compare x-axis (works for right hand facing camera)
    # If tip is to the right of the IP joint → extended
    thumb_up = lm[TIPS[0]].x < lm[PIPS[0]].x  # flipped for mirror view
    up.append(thumb_up)

    # Other four fingers: tip higher (smaller y) than PIP joint → extended
    for i in range(1, 5):
        up.append(lm[TIPS[i]].y < lm[PIPS[i]].y)

    return up


def classify_gesture(up):
    """
    Maps a [thumb, index, middle, ring, pinky] boolean list to a gesture name.
    """
    t, i, m, r, p = up
    count = sum(up)

    if count == 0:
        return "Fist ✊"
    if count == 5:
        return "Open Hand ✋"
    if not t and i and not m and not r and not p:
        return "Pointing ☝️"
    if not t and i and m and not r and not p:
        return "Peace / Victory ✌️"
    if t and i and not m and not r and not p:
        return "Gun / L-shape 🤞"
    if not t and i and m and r and p:
        return "Four Fingers"
    if t and not i and not m and not r and p:
        return "Shaka / Hang Loose 🤙"
    if not t and not i and not m and not r and p:
        return "Pinky Up 🤙"
    if t and i and m and not r and not p:
        return "Three Fingers"
    if not t and i and not m and not r and p:
        return "Horns 🤘"
    if t and not i and not m and not r and not p:
        return "Thumbs Up 👍"
    if count == 1 and not t:
        # only non-thumb finger extended
        for idx, val in enumerate(up[1:], 1):
            if val:
                names = ["Index", "Middle", "Ring", "Pinky"]
                return f"{names[idx-1]} Finger"
    return f"{count} Fingers"


# ── Drawing helpers ───────────────────────────────────────────────────────────
FONT       = cv2.FONT_HERSHEY_SIMPLEX
TEXT_COLOR = (255, 255, 255)
BOX_COLOR  = (30, 30, 30)
DOT_COLOR  = (0, 220, 120)


def draw_label(frame, text, pos):
    """Draw a dark background label at pos (x, y)."""
    x, y = pos
    (w, h), baseline = cv2.getTextSize(text, FONT, 0.9, 2)
    cv2.rectangle(frame, (x - 6, y - h - 10), (x + w + 6, y + baseline), BOX_COLOR, -1)
    cv2.putText(frame, text, (x, y), FONT, 0.9, TEXT_COLOR, 2, cv2.LINE_AA)


def draw_finger_dots(frame, landmarks, h, w, up):
    """Overlay a coloured dot on each fingertip — green if up, red if down."""
    for idx, tip_id in enumerate(TIPS):
        lm = landmarks.landmark[tip_id]
        cx, cy = int(lm.x * w), int(lm.y * h)
        color = (0, 220, 80) if up[idx] else (60, 60, 200)
        cv2.circle(frame, (cx, cy), 10, color, -1)
        cv2.circle(frame, (cx, cy), 10, (255, 255, 255), 2)


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam. Check your camera index.")
        return

    print("Hand Gesture Recognition running — press Q to quit.")

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip for mirror view and convert BGR→RGB for MediaPipe
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_idx, hand_lms in enumerate(results.multi_hand_landmarks):

                    # Draw skeleton
                    mp_draw.draw_landmarks(
                        frame,
                        hand_lms,
                        mp_hands.HAND_CONNECTIONS,
                        mp_style.get_default_hand_landmarks_style(),
                        mp_style.get_default_hand_connections_style(),
                    )

                    # Classify
                    up      = fingers_up(hand_lms)
                    gesture = classify_gesture(up)

                    # Finger count overlay
                    draw_finger_dots(frame, hand_lms, h, w, up)

                    # Bounding box from landmarks
                    xs = [lm.x for lm in hand_lms.landmark]
                    ys = [lm.y for lm in hand_lms.landmark]
                    x1 = max(0, int(min(xs) * w) - 20)
                    y1 = max(0, int(min(ys) * h) - 20)

                    # Label above the hand
                    draw_label(frame, gesture, (x1, max(30, y1 - 10)))

                    # Finger states in bottom-left corner
                    state_str = "  ".join(
                        ["T", "I", "M", "R", "P"][i] if up[i] else "_"
                        for i in range(5)
                    )
                    y_offset = h - 50 + hand_idx * 30
                    draw_label(frame, f"Hand {hand_idx+1}: {state_str}", (10, y_offset))

            else:
                draw_label(frame, "No hand detected", (10, 40))

            # Header bar
            cv2.rectangle(frame, (0, 0), (w, 36), (20, 20, 20), -1)
            cv2.putText(frame, "Hand Gesture Recognition  |  Q to quit",
                        (10, 24), FONT, 0.6, (180, 180, 180), 1, cv2.LINE_AA)

            cv2.imshow("Hand Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()