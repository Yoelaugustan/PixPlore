import cv2
import mediapipe as mp
import numpy as np
import time

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 1, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
drawingSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)

while cap.isOpened():
    success, image = cap.read()
    start = time.time()

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) #Flip cam so it is mirrored. Convert color space from BGR to RGB
    image.flags.writeable = False # To Improve Performance

    results = faceMesh.process(image)
    image.flags.writeable = True # To Improve Performance
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) # Convert color space from RGB to BGR

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 26 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    face_2d.append([x, y]) # Get the 2D Coordinates
                    face_3d.append([x, y, lm.z]) # Get the 3D Coordinates
            
            face_2d = np.array(face_2d, dtype=np.float64) # Convert it to NumPy array
            face_3d = np.array(face_3d, dtype=np.float64) # Convert it to NumPy array

            focal_length = 1 * img_w
            cam_matrix = np.array([ [focal_length, 0, img_h/2],
                                    [0, focal_length, img_h/2],
                                    [0, 0, 1] ])
            dist_matrix = np.zeros((4, 1), dtype=np.float64) 
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix) # solve pnp

            rmat, jac = cv2.Rodrigues(rot_vec) # get rotational matrix
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat) # get angles

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            # see where the user's head is tilting
            if y < -10:
                text = "HEAD_LEFT"
            elif y > 10:
                text = "HEAD_RIGHT"
            elif x < -10:
                text = "HEAD_DOWN"
            elif x > 10:
                text = "HEAD_UP"
            else:
                text = "HEAD_FORWARD"

            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        
    end = time.time()
    totalTime = end - start
    
    if totalTime > 0:
        fps = 1 / totalTime
    else:
        fps = 0

    cv2.putText(image, f"FPS: {int(fps)}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    cv2.imshow('Press "ESC" to close the camera', image)
    if cv2.waitKey(1) == 27: 
        break

cap.release()
