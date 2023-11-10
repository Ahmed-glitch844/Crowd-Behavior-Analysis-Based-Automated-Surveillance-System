import cv2

# Open the webcam for capturing video
video_capture = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this number if you have multiple cameras)

# Check if the webcam was opened successfully
if not video_capture.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Define the codec for the output clip and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Change the codec as needed
output_path = 'output_clip.avi'  # Specify the path and filename for the output clip
output_clip = cv2.VideoWriter(output_path, fourcc, 16.0, (640, 480))  # Adjust the resolution as needed

# Set the number of frames to capture for the clip
frame_count = 32  # Adjust this as needed

frame_number = 0

while frame_number < frame_count:
    ret, frame = video_capture.read()

    if not ret:
        print("Error: Could not read a frame from the webcam.")
        break

    output_clip.write(frame)
    frame_number += 1

# Release the webcam and video writer
video_capture.release()
output_clip.release()
