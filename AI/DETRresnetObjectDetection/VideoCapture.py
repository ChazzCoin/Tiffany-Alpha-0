import opencv_camera
from transformers import pipeline
import cv2
import tempfile
# Instantiate the model
model = pipeline("object-detection")

# Start the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture the camera frame
    ret, frame = cap.read()

    # Run the model on the frame
    # Save the frame as an image file
    with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
        cv2.imwrite(image_file.name, frame)
        # Run the model on the image file
        outputs = model(image_file.name)

    # Display the frame with the model's output
    for output in outputs:
        xmin, ymin, xmax, ymax = map(int, [output['box']['xmin'],output['box']['ymin'],output['box']['xmax'],output['box']['ymax']])
        label = output['label']
        confidence = output['score']
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        cv2.putText(frame, f"{label}: {confidence:.2f}", (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()