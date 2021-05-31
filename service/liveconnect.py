import cv2
import time
from flask import Flask, render_template, Response
from pyzbar.pyzbar import decode, ZBarSymbol
from service import download_service

app = Flask(__name__)

def read_barcodes(frame1):
    barcodes = decode(frame1,symbols=[ZBarSymbol.QRCODE])
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        print("successful")
        print(barcode_info)
        file = download_service.initiate_download(barcode_info)
        print(file)
        cv2.rectangle(frame1, (x, y),(x+w, y+h), (0, 255, 0), 2)
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame1, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        time.sleep(1)
    return frame1

def gen_frames():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__=='__main__':
    app.run()
