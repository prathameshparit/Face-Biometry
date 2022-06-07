# import time
# from datetime import date
# import webbrowser
# from flask import Flask, render_template, Response
# import cv2
# import face_recognition
# import numpy as np
# import os
#
# app = Flask(__name__)
# camera = cv2.VideoCapture(0)
#
#
# path = 'log'
#
# def FPS(img, fps, latency):
# 	cv2.putText(img, f"FPS: {str(int(fps))}", org=(7, 25), fontFace=cv2.FONT_HERSHEY_PLAIN,
# 				fontScale=1, color=(0, 0, 0), thickness=1)
#
# 	cv2.putText(img, f"Latency: {str(latency)}s", org=(97, 25), fontFace=cv2.FONT_HERSHEY_PLAIN,
# 				fontScale=1, color=(0, 0, 0), thickness=1)
#
# 	return img
#
#
#
# images = []
# known_face_names = []
# myList = os.listdir(path)
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     known_face_names.append(os.path.splitext(cl)[0])
# print(known_face_names)
#
#
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList
#
#
# known_face_encodings = findEncodings(images)
# print('Encoding Complete')
#
#
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
#
#
# def gen_frames():
#
# 	# pTime, pTimeL = 0, 0
# 	# previous = time.time()
# 	# a, b = 0, 0
# 	# expTime = 0
#
#     while True:
#
#         success, frame_ = camera.read()  # read the camera frame
# 		# frame = cv2.flip(frame_, 1)
# 		#
# 		#
# 		#
# 		# curTime = time.time()
# 		# expTime = curTime - expTime
# 		# expTime = curTime
# 		# # if expTime > 3 and expTime < 4:
# 		# filename = str(int(expTime))
# 		#
# 		#
# 		#
# 		# # FPS
# 		# cTimeL = time.time()
# 		#
# 		# cTime = time.time()
# 		# if (cTime - pTime) != 0:
# 		# 	fps = 1 / (cTime - pTime)
# 		# 	latency = np.round((cTimeL - pTimeL), 4)
# 		# 	pTime, pTimeL = cTime, cTimeL
# 		# 	a += 1
# 		#
# 		# 	frame = FPS(frame, fps, latency)
# 		#
# 		#
# 		#
# 		#
#
#         if not success:
#             break
#         else:
#             # Resize frame of video to 1/4 size for faster face recognition processing
#             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#             # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#             rgb_small_frame = small_frame[:, :, ::-1]
#
#             # Only process every other frame of video to save time
#
#             # Find all the faces and face encodings in the current frame of video
#             face_locations = face_recognition.face_locations(rgb_small_frame)
#             face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#             face_names = []
#             for face_encoding in face_encodings:
#                 # See if the face is a match for the known face(s)
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#                 name = "Restrict"
#                 # Or instead, use the known face with the smallest distance to the new face
#                 face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)
#                 if matches[best_match_index]:
#                     name = known_face_names[best_match_index]
#
#                 face_names.append(name)
#
#             # Display the results
#             for (top, right, bottom, left), name in zip(face_locations, face_names):
#                 # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#                 top *= 4
#                 right *= 4
#                 bottom *= 4
#                 left *= 4
#
#                 # Draw a box around the face
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#
#                 # Draw a label with a name below the face
#                 # if(name=="Restrict"):
#                 #     filename=date.today().strftime("%d/%m/%Y")
#                 #     cv2.imwrite(f"./Restrict/{filename}.jpg")
#
#
#                 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# if __name__ == "__main__":
# 	# app.run(debug=True)
#     webbrowser.open_new('http://127.0.0.1:5000/')
#     app.run(debug=True, port=5000)






import webbrowser
from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
from datetime import date


app = Flask(__name__)
camera = cv2.VideoCapture(0)


path = 'log'



images = []
known_face_names = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    known_face_names.append(os.path.splitext(cl)[0])
print(known_face_names)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


known_face_encodings = findEncodings(images)
print('Encoding Complete')


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def save(name1):

    if name1=="Unauthorized":
        _, img_orig = camera.read()
        img = cv2.flip(img_orig, 1)

        path = 'Restrict'

        cv2.imwrite(os.path.join(path, "Unknown" + '.jpg'), img)

        # Video stream
        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')



def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        frame = cv2.flip(frame, 1)
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unauthorized"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)


            # if (name == "Unauthorized"):
            #
            # filename = date.today().strftime("%d/%m/%Y")
            # path = 'Restrict'
            #
            # # Using cv2.imread() method
            # img = cv2.imread('log/obama2.jpg')
            # cv2.imwrite("/facebiometry/Restrict/new.jpg", img)
            #
            # cv2.imwrite(f"./Restrict/{filename}.jpg", frame)

            from datetime import datetime

            if name == "Unauthorized":

                now = str(datetime.now()).split(".")[0].replace(":", "-").replace(" ", "-")
                cv2.imwrite(f"Restrict/{now}.jpeg", frame)
                cv2.imshow("Cam", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                save(name)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                fontScale = 1
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



def enroll(name):


    _, img_orig = camera.read()
    img = cv2.flip(img_orig, 1)

    path = 'log'
    cv2.imwrite(os.path.join(path, name + '.jpg'), img)
    # Video stream
    ret, buffer = cv2.imencode('.jpg', img)
    img = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')



from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'

class LoginForm(FlaskForm):
    username = StringField('Name')
    password = PasswordField('password')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()


    if form.validate_on_submit():
        # return '<h1>The username is {}. The password is {}.'.format(form.username.data, form.password.data)
        name = form.username.data
        print(name)
        enroll(name)
        return Response(enroll(name), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('form.html', form=form)










@app.route('/enroll_feed')
def enroll_feed():
    return Response(enroll(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	# app.run(debug=True)
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True, port=5000)