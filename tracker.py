import cv2

# Initialize Tracker
tracker = cv2.legacy.TrackerMOSSE_create()

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3, 3)
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2)

# Open Camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Read a frame and select ROI
success, img = cap.read()
if not success:
    print("Error: Unable to read from the camera.")
    cap.release()
    exit()

# Select ROI
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)

# Main Loop
while True:
    timer = cv2.getTickCount()
    success, img = cap.read()
    if not success:
        print("Error: Unable to read frame.")
        break

    # Update Tracker
    success, bbox = tracker.update(img)
    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Calculate FPS
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps > 60:
        myColor = (20, 230, 20)
    elif fps > 20:
        myColor = (230, 20, 20)
    else:
        myColor = (20, 20, 230)
    
    cv2.putText(img, f"FPS: {int(fps)}", (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)
    cv2.imshow("Tracking", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
