import cv2
import pytesseract
import time

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Set lower resolution for performance
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise and keep edges
    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    # Perform Canny edge detection
    edged = cv2.Canny(blur, 30, 200)

    # Find contours from the edged image
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    found = False  # Flag to indicate plate detection

    for c in contours:
        # Approximate the contour
        approx = cv2.approxPolyDP(c, 0.018 * cv2.arcLength(c, True), True)

        # Check for quadrilateral shapes (potential license plates)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)

            # Filter out small rectangles (likely noise)
            if w > 60 and h > 40:
                roi = frame[y:y+h, x:x+w]

                # Use Tesseract to extract text
                text = pytesseract.image_to_string(roi, config='--psm 7')
                text = text.strip()

                if text:
                    print("Detected:", text)

                    # Draw bounding box and text on the original frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 1)

                    found = True
                    break  # Exit after detecting one plate to save processing

    # Show the processed frame
    cv2.imshow("License Plate Detection", frame)

    # Wait for 3 seconds or break early with 'q'
    if cv2.waitKey(3000) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
