import cv2 
import numpy as np


class MiniPainter:

  def __init__(self, width=800, height=600):
    self.width = width
    self.height = height
    self.canvas = np.ones((height, width, 3), dtype=np.uint8) * 255
    self.current_shape = "circle"
    self.current_color_idx = 0
    self.colors = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
        (255, 0, 255),
    ]
    self.window_name = "Mini Painter Task"

  def mouse_callback(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      color = self.colors[self.current_color_idx]
      if self.current_shape == "circle":
        cv2.circle(self.canvas, (x, y), 30, color, -1)
      elif self.current_shape == "rectangle":
        cv2.rectangle(self.canvas, (x - 30, y - 20), (x + 30, y + 20), color, -1)
      elif self.current_shape == "polygon":
        pts = np.array(
            [[x, y - 30], [x - 25, y + 20], [x + 25, y + 20]], np.int32
        )
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(self.canvas, [pts], color)

  def run(self):
    cv2.namedWindow(self.window_name)
    cv2.setMouseCallback(self.window_name, self.mouse_callback)

    while True:
      display_img = self.canvas.copy()
      info_text = f"Shape: {self.current_shape} | Color: {self.current_color_idx + 1}"
      cv2.putText(
          display_img,
          info_text,
          (10, 30),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.7,
          (0, 0, 0),
          2,
      )

      cv2.imshow(self.window_name, display_img)
      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
        break
      elif key == ord("c"):
        self.current_shape = "circle"
      elif key == ord("r"):
        self.current_shape = "rectangle"
      elif key == ord("p"):
        self.current_shape = "polygon"
      elif key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5")]:
        self.current_color_idx = int(chr(key)) - 1
      elif key == ord("w"):
        cv2.imwrite("saved_canvas.png", self.canvas)
        print("Saved successfully as saved_canvas.png")

    cv2.destroyAllWindows()


if __name__ == "__main__":
  painter = MiniPainter()
  painter.run()