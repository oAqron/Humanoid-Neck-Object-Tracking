import cv2

# replace 1 with whichever index showed up
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    raise IOError("Cannot open camera at index 1")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame grab failed; retrying…")
        continue

    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()