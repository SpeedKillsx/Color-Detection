from flask import Flask,render_template,Response, request, redirect
import cv2 as cv
from PIL import  Image
from hsv_convertor import get_range_hsv
app=Flask(__name__)
camera=cv.VideoCapture(0)
selected_color="red"
def generate_frames():
    global selected_color
    color = []
    if selected_color =="yellow":
        color = [0,255,255]
    elif selected_color =="red":
        color = [0,0,255]
    elif selected_color =="green":
        color = [0,255,0]
    else:
        color = [255,0,0]
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            low, high = get_range_hsv(color)
            mask = cv.inRange(frame_hsv, low, high)
            bitwise_and = cv.bitwise_and(src1=frame,src2=frame, mask=mask)
            # Get the bouding box of the image
            mask_ = Image.fromarray(mask)
            box = mask_.getbbox()
            if box is not None:
                x1, y1,x2,y2 = box
                
                frame = cv.rectangle(frame,(x1,y1), (x2,y2), color, thickness=5)
            ret,buffer=cv.imencode('.jpg',frame)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/select', methods=["post"])
def select():
    global selected_color
    selected_color = request.form.get('color')
    print(str(selected_color))
    
    return redirect('/')
@app.route('/video')
def video():
    """color = request.form.get['color']
    print(color)"""
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
