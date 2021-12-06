import numpy as np
import cv2
import tensorflow as tf

model = tf.keras.models.load_model(r"ASLModel.h5")
background = None
accumulated_weight = 0.5
ROI_top = 100
ROI_bottom = 300
ROI_right = 150
ROI_left = 350
letters = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J', '10': 'K', '11': 'L', '12': 'M',
           '13': 'N', '14': 'O', '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T', '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y', '25': 'Z'}


def cal_accum_avg(frame, accumulated_weight):
    global background
    if background is None:
        background = frame.copy().astype("float")
        return None
    cv2.accumulateWeighted(frame, background, accumulated_weight)

def segment_hand(frame, threshold=25):
    global background
    diff = cv2.absdiff(background.astype("uint8"), frame)
    _, thresholded = cv2.threshold(diff, threshold, 255,
                                   cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(
        thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None
    else:
        hand_segment_max_cont = max(contours, key=cv2.contourArea)
        return (thresholded, hand_segment_max_cont)
cam = cv2.VideoCapture(0)
num_frames = 0
lets = []
word = []
while True:
    ret, frame = cam.read()
    if frame is None:
        break
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()
    # ROI from the frame
    roi = frame[ROI_top:ROI_bottom, ROI_right:ROI_left]
    gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)
    if num_frames < 70:
        cal_accum_avg(gray_frame, accumulated_weight)
        cv2.putText(frame_copy, "FETCHING BACKGROUND...PLEASE WAIT",
                    (80, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    else:
        hand = segment_hand(gray_frame)
        if hand is not None:
            thresholded, hand_segment = hand
            # Drawing contours around hand segment
            cv2.drawContours(frame_copy, [hand_segment + (ROI_right,
                                                          ROI_top)], -1, (255, 0, 0), 1)
            cv2.imshow("Thesholded Hand Image", thresholded)
            thresholded = cv2.resize(thresholded, (64, 64))
            thresholded = cv2.cvtColor(thresholded,
                                       cv2.COLOR_GRAY2RGB)
            thresholded = np.reshape(thresholded,
                                     (1, thresholded.shape[0], thresholded.shape[1], 3))
            # thresholded = np.expand_dims(thresholded, axis=0)
            pred = model.predict(thresholded)
            pred_letter = letters[str(np.argmax(pred[0]))]
            lets.append(pred_letter)

            if pred_letter == 'V':
                d = {}
                for i in range(len(lets)):
                    _, c = d[lets[i]] if lets[i] in d else (lets[i], 0)
                    d[lets[i]] = (i, c + 1)
                op = {k: v for k, v in sorted(
                    d.items(), key=lambda item: item[1][1], reverse=True)}
                op = {k: op[k] for k in list(op)[:4]}
                op = {k: v for k, v in sorted(
                    op.items(), key=lambda item: item[1][0])}
                print(''.join(list(op)))
                break

            cv2.putText(frame_copy, pred_letter,
                        (170, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # Draw ROI on frame_copy
    cv2.rectangle(frame_copy, (ROI_left, ROI_top), (ROI_right,
                                                    ROI_bottom), (255, 128, 0), 3)
    # incrementing the number of frames for tracking
    num_frames += 1
    # Display the frame with segmented hand
    cv2.putText(frame_copy, "DataFlair hand sign recognition_ _ _",
                (10, 20), cv2.FONT_ITALIC, 0.5, (51, 255, 51), 1)
    cv2.imshow("Sign Detection", frame_copy)
    # Close windows with Esc
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


# Release the camera and destroy all the windows


cam.release()
cv2.destroyAllWindows()
