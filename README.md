# 🚗 License Plate Detection using OpenCV and Tesseract

This Python script uses **OpenCV** for image processing and **Tesseract OCR** for text recognition to detect and read vehicle license plates from a live webcam feed.

## 🔧 Requirements

* Python 3.x
* OpenCV (`cv2`)
* pytesseract
* Tesseract-OCR installed and added to your system PATH

## 📜 Code Breakdown

### 1. **Camera Initialization**

```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

* Initializes the webcam (device 0).
* Sets the resolution to 320x240 for faster processing.

---

### 2. **Live Frame Capture and Preprocessing Loop**

```python
ret, frame = cap.read()
```

* Captures a frame from the webcam.
* If capturing fails, the loop breaks.

#### Convert to Grayscale

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

* Converts the image to grayscale, reducing complexity.

#### Noise Reduction

```python
blur = cv2.bilateralFilter(gray, 11, 17, 17)
```

* Applies a bilateral filter to preserve edges while removing noise.

#### Edge Detection

```python
edged = cv2.Canny(blur, 30, 200)
```

* Detects edges using the Canny algorithm.

---

### 3. **Contour Detection and Filtering**

```python
contours, _ = cv2.findContours(...)
```

* Extracts contours from the edge-detected image.

```python
approx = cv2.approxPolyDP(...)
```

* Approximates each contour to a polygon.

```python
if len(approx) == 4:
```

* Checks for **quadrilateral shapes** (common shape for license plates).

```python
if w > 60 and h > 40:
```

* Filters out small shapes that are unlikely to be license plates.

---

### 4. **Text Extraction with Tesseract**

```python
text = pytesseract.image_to_string(roi, config='--psm 7')
```

* Extracts text from the Region of Interest (ROI) using Tesseract.
* `--psm 7` treats the image as a single line of text.

```python
cv2.rectangle(...) / cv2.putText(...)
```

* If text is found, draws a rectangle and labels it on the original frame.

---

### 5. **Display and Exit**

```python
cv2.imshow("License Plate Detection", frame)
cv2.waitKey(3000)
```

* Displays the processed video frame.
* Waits for 3 seconds or exits early if `'q'` is pressed.

---

### 6. **Cleanup**

```python
cap.release()
cv2.destroyAllWindows()
```

* Releases the camera and closes all OpenCV windows.

---

## 📝 Notes

* You may need to configure the Tesseract executable path if it's not in your system's PATH:

  ```python
  pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_tesseract>'
  ```
* OCR accuracy may vary based on lighting, angle, and plate clarity.
* Consider integrating additional image processing or plate localization methods for better accuracy.

---

## 📷 Example Output

When a license plate is detected:

* A green rectangle appears around the plate.
* The recognized text is printed to the console and displayed above the rectangle.

---


