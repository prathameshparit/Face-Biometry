import webbrowser
from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import pandas as pd
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
import csv


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


def gen_frames():
    global name
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
                name = 'Unauthorized'
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = str(known_face_names[best_match_index])

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                if name == 'Unauthorized':

                    now = str(datetime.now()).split(".")[0].replace(":", "-").replace(" ", "-")
                    now = now[:-3]
                    if not os.path.isfile(f"Restrict/{now}.jpeg"):
                        cv2.imwrite(f"Restrict/{now}.jpeg", frame)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX

                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                markAttendance(name)



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

    # cv2.imwrite(f"log/{name}.jpeg", img)
    # cv2.imshow("Cam", img)


def change_type(sub):
    """
	Makes each element of list or array change to string
	:param sub: list or any array
	:return: string type of all elements
	"""

    if isinstance(sub, list):
        return [change_type(ele) for ele in sub]
    elif isinstance(sub, tuple):
        return tuple(change_type(ele) for ele in sub)
    else:
        return str(sub)


def markAttendance(name):
    df = pd.read_csv('attendance.csv')

    # List1 is the list of all values of librec.csv in a list
    list1 = df.values.tolist()
    list1 = change_type(list1)

    issue_date = datetime.now()
    issue_date = issue_date.strftime("%d-%m-%Y")

    new_date = datetime.now()
    issue_time = new_date.strftime("%H:%M")

    rt_df = pd.DataFrame({'Name': [name],
                          'Date': [issue_date],
                          'Time': [issue_time]
                          })

    list2 = rt_df.values.tolist()
    list2 = change_type(list2)

    flag2 = 0
    for i in range(len(list1)):
        flag2 = 0
        if list1[i][0] == list2[0][0] and list1[i][1] == list2[0][1] and list1[i][2] == list2[0][2]:
            flag2 = 1
            break

    if flag2 == 0:
        rt_df.to_csv('attendance.csv', mode='a', header=False, index=False)


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
    return render_template('enrollnow.html', form=form)


@app.route('/enroll_feed')
def enroll_feed():
    return Response(enroll(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data_attendance', methods=['GET', 'POST'])
def data_attendance():
	f = "attendance.csv"
	data = []
	with open(f) as file:
		csvfile = csv.reader(file)
		for row in csvfile:
			data.append(row)

	data = pd.DataFrame(data)
	return render_template('csvrec.html', data=data.to_html(classes='mystyle', header=False, index=False))


if __name__ == "__main__":
    # app.run(debug=True)
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True, port=5000)
