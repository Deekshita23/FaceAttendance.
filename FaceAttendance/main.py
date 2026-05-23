import cv2
import csv
from datetime import datetime

# Open Webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Load Face Detector
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Enter Name
name = input("Enter Your Name: ")

while True:

    # Read Camera Frame
    success, img = cap.read()

    # Check Camera
    if not success:
        print("Camera not working")
        break

    # Convert to Gray Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect Faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # Draw Rectangle Around Face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Date and Time
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        # Store Attendance Only Once
        with open("attendance.csv", "a+", newline="") as f:

            f.seek(0)
            data = f.read()

            if name not in data:

                writer = csv.writer(f)
                writer.writerow([name, date, time])

                print("Attendance Marked")

        # Show Name on Screen
        cv2.putText(
            img,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # Show Webcam
    cv2.imshow("Face Attendance System", img)

    # Press q to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release Camera
cap.release()
cv2.destroyAllWindows()