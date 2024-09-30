import cv2
import btn
def turn_cam(off):
    vid = cv2.VideoCapture(0)

    while True:
        ret, frame = vid.read()
        cv2.imshow('camera', frame)

        if cv2.waitKey(1)==ord('q') or off():
            break
    vid.release()
    cv2.destroyAllWindows()

def main():
    while True:
        if btn.btn_pressed():
            turn_cam(btn.btn_pressed)
            break
        else:
            pass

main()