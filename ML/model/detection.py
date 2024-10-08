from typing import Any
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import joblib
import pandas as pd
from PIL import Image


class Detection:
    def __init__(self, model_path="./model/pose_landmarker_lite.task"):
        self.model_path = model_path
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options, output_segmentation_masks=True
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)
        self.best_model = joblib.load("./model/best_xgboost_model.pkl")

    def __data_prep(self, pose_landmarker_result):
        try:
            pose_landmarker_result.pose_landmarks[0]
        except IndexError:
            return []
        landmarks = pose_landmarker_result.pose_landmarks[0]
        landmarks = landmarks[7:9] + landmarks[11:]
        data = []
        for landmark in landmarks:
            data.append({"x": landmark.x, "y": landmark.y, "z": landmark.z})
        return data

    def __mark_image(self, image_path):
        image = mp.Image.create_from_file(image_path)

        detection_result = self.detector.detect(image)

        return detection_result

    def __format_data(self, data):
        formatted_data = []
        for e in data:
            formatted_data.append((e["x"] + e["y"] + e["z"]) / 3)
        return formatted_data

    def get_detection(self, image_path):
        detection_result = self.__mark_image(image_path)
        return self.__data_prep(detection_result)

    def predict(self, img_path):
        formatted_data = self.__format_data(self.get_detection(img_path))
        X = pd.DataFrame([formatted_data])
        return self.best_model.predict(X)[0]

    def predict_proba(self, img_path):
        formatted_data = self.__format_data(self.get_detection(img_path))
        X = pd.DataFrame([formatted_data])
        classes = self.best_model.classes_
        proba = self.best_model.predict_proba(X)[0]
        l = [(classes[i], proba[i]) for i in range(len(classes))]
        print(sorted(l, key=lambda x: x[1], reverse=True))
