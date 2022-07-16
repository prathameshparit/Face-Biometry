
# Face Biometry

Face Detection, Verification and Recognition using Python and Face Recognition Libraries. This is a Computer Vision project for 
RAIT Internship. This project is a collaboratory project of Group 6.

## Face-Biometrics System

Identifying facial features from photo, video or live camera and comparing them with reference photo or set of photos to identify or authorize humans into premises or systems.

**Face Detection - Identify human faces in given set of images**

**Face Identification - Comparing the face in the image with all the registered faces in the database (One to Many face mapping)**

**Face Verification/Recognition - Verifying the detected face by finding a match from the registered faces in database (One to One face mapping)**

## Use Cases
1.  Attendance System
2.  Login authentication application
3.  Office security clearance
4.  Criminal Investigation
5.  Pension and Visa Verification (Especially to make sure the person is alive)
## Screenshots and Steps

**1. Landing Page:**

This is the landing page for the web application 

![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/landing.png?raw=true)

**2. Face Recognition(Authorized User):**

The face of person is being captured frame by frame and the model tries to analyze weather the image is known or unknown.
If the image was already in the Database known then model tries to find patterns in the image and recognizes the image 
with the name of the person overlayed on the screen.

![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/check.png?raw=true)

**3. Records:**

Once the Face is recognized the data is been updated in the database with features that contain the name of person, date and time 
when accessed the app. The page also contains a download button to download the csv record.


![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/csv.png?raw=true)

**4. Face Recognition(Unauthorized User):**

The Unauthorized user is marked with an overlay of 'Unauthorized' label. And the image of unauthorised is saved in the database.

![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/unauthorised.png?raw=true)

**5. Database:**

The Database consists of images of users who were marked as unauthorised and those unauthorised users are labeled with the date
and time when they tried to gain access.

![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/saved.png?raw=true)

**6. Enroll:**

At last we have the Enroll page that enables new users to enroll themselves on the application so that next time when they try to 
gain access they aren't restricted.The enroll page consists of a Name input button that gives user an option to enroll their name.  

![App Screenshot](https://github.com/prathameshparit/Dummy-Storage/blob/main/readme%20images/Enroll.png?raw=true)
## Contributers:

This project is a collaboratory project with:

- Collaborators:

        1. Prathamesh Parit
        2. Dhumravarna Ambre
        3. Gaurav Ojha
        4. Riyanshu Singh
- Mentors:

        1. Sumedha Bhagwat
        2. Dr. Reshma Gulwani
