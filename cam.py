import cv2
import btn
import pickle
import struct
import imutils

def turn_cam(off, conn):
    vid = cv2.VideoCapture(0)

    while (vid.isOpened()):
        ret, frame = vid.read()
        frame = imutils.resize(frame,width = 320)
        a = pickle.dumps(frame)
        message = struct.pack('Q', len(a))+a

        conn.sendall(message)
        cv2.imshow('camera', frame)

        if cv2.waitKey(1)==ord('q') or off():
            conn.close()
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
