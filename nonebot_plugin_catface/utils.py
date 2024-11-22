
from ultralytics import YOLO

class YOLOModel():
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image):
        # TODO: 返回方框信息
        results = self.model(image)
        return results