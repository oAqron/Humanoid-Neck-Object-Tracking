import cv2

for idx in range(5):
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"[+] Camera found at index {idx}")
        cap.release()
    else:
        print(f"[-] No camera at index {idx}")