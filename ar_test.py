import cv2


# Function to detect person using OpenCV's pre-trained Haar cascade
def detect_person(image):
    # Load pre-trained Haar cascade for full body
    full_body_cascade = cv2.CascadeClassifier("./haarcascade_upperbody.xml")

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect full body in the image
    persons = full_body_cascade.detectMultiScale(gray, 1.1, 5)

    return persons


# Main function to capture video from camera and display "Hello World!" on the person
def main():
    # Start capturing video from the default camera
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Detect person in the frame
            persons = detect_person(frame)

            # Draw "Hello World!" on the person if detected
            for x, y, w, h in persons:
                cv2.putText(
                    frame,
                    "Hello World!",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Frame", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            print("Error: Failed to capture frame.")
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
