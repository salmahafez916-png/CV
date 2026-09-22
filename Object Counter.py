import cv2
import numpy as np


class ObjectCounter:

  def __init__(self, image_path):
    self.image_path = image_path
    self.original_image = cv2.imread(image_path)
    if self.original_image is None:
      raise ValueError(f"Could not load image from: {image_path}")

    self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
    self.selected_hsv = None

  def mouse_callback(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.selected_hsv = self.hsv_image[y, x]
      print(f"Selected HSV at ({x}, {y}): {self.selected_hsv}")

  def process(self):
    print("--- Object Counter Started ---")
    print("Click on any color in the image to detect matching objects.")
    print("Press 'r' to reset color, or 'q' to quit.")

    window_name = "Object Counter"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, self.mouse_callback)

    while True:
      temp_img = self.original_image.copy()

      if self.selected_hsv is not None:
        hue = self.selected_hsv[0]
        lower_bound = np.array([max(0, hue - 10), 100, 100])
        upper_bound = np.array([min(179, hue + 10), 255, 255])

        mask = cv2.inRange(self.hsv_image, lower_bound, upper_bound)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        count = 0
        for cnt in contours:
          if cv2.contourArea(cnt) > 30:
            count += 1
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(temp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print(f"Detected objects with this color: {count}")
        cv2.putText(
            temp_img,
            f"Count: {count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

      cv2.imshow(window_name, temp_img)
      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break
      elif key == ord("r"):
        self.selected_hsv = None
        print("Reset. Please select a new color.")

    cv2.destroyAllWindows()


if __name__ == "__main__":
  counter = ObjectCounter("task_two.png")
  counter.process()
