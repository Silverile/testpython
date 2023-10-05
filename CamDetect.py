import cv2
from tkinter import *
from PIL import Image, ImageTk

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a Tkinter window
root = Tk()
root.title("Webcam Feed")

# Create a label to display the video feed
video_label = Label(root)
video_label.pack(side=LEFT)


def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to a PIL Image
        img = Image.fromarray(frame)

        # Convert the PIL Image to a Tkinter PhotoImage
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Call this function again after 10 milliseconds
    root.after(10, update_frame)


# Call the update_frame function to start the video feed
update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the webcam when the window is closed
cap.release()
