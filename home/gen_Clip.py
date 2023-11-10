import cv2

def gen_clip(f):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use the desired codec (e.g., 'XVID')
    output_path = 'output_clip.avi'  # Specify the path and filename for the output clip
    height, width, _ = f[0].shape
    output_clip = cv2.VideoWriter(output_path, fourcc, 16.0, (width, height))
    for frame in f:
        output_clip.write(frame)

# Release the VideoWriter and close the video capture
    output_clip.release()

