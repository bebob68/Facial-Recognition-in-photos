import face_recognition
import os
import cv2

KNOWN_FACES_DIR = "Known_faces"
UNKNOWN_FACES_DIR = "Unknown_faces"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "cnn"

print("loading known faces")

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[1]
        known_faces.append(encoding)
        known_names.append(name)

print("processing unknown faces")
for filename in os.listdir(UNKNOWN_FACES_DIR):
    print(filename)
    image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
    locations = face_recognition.face_locations(image, model= MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    for face_encodings, face_locations in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encodings, TOLERANCE)
        match = known_names
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match found: {match}")

            top_left = (face_loaction[3], face_loaction[0])
            bottom_right = (face_loaction[1], face_loaction[2])

            color = [0, 255, 0]

            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_loaction[3], face_loaction[2])
            bottom_right = (face_loaction[1], face_loaction[2]+22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_loaction[3]+10, face_loaction[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)
    cv2.imshow(filename, image)
    cv2.waitKey(1000)
    #cv2.destroyWindow(filename)
