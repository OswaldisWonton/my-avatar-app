import os
import cv2
import numpy as np
from tqdm import tqdm

import torch
import torch.nn.functional as F

import face_recognition

from third_party.face_similarity_pytorch.predict import get_model
from third_party.face_similarity_pytorch.src import models, preprocess

def face_detection(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    return bool(len(face_landmarks_list))

class FaceComparison:
    def __init__(self, device="cpu"):
        self.device = device
        self.model = get_model(device, "third_party/face_similarity_pytorch/weights/face-siamese-crop.pt")
        self.transforms = preprocess.get_transforms_inference()
        self.ref_image_path = "ref_data/"
        self.ref_features_path = "ref_data/ref_features.pt"
        self._get_ref_features()
    
    def _get_ref_features(self):
        if os.path.exists(self.ref_features_path):
            tmp = torch.load(self.ref_features_path)
            self.ref_features = tmp["features"]
            self.ref_labels = tmp["labels"]
            return
        print("[INFO] Run code for the first time. Generating features for reference images.")
        self.ref_features = []
        self.ref_labels = []
        for root, dirs, files in os.walk(self.ref_image_path):
            for file in tqdm(files):
                label = file.split("_")[0]
                image = cv2.imread(os.path.join(root, file))
                feature = self.image_feature(image)
                self.ref_features.append(feature)
                self.ref_labels.append(label)
            break
        self.ref_features = torch.stack(self.ref_features)
        torch.save({"features": self.ref_features, "labels": self.ref_labels}, self.ref_features_path)

    def _transform(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.array(self.transforms(image))
        image = image.transpose(2, 0, 1).astype(np.float32)[np.newaxis, ...]
        return torch.from_numpy(image).to(self.device)
    
    def image_feature(self, image):
        image = self._transform(image)
        feature = self.model.forward_once(image)
        return feature.squeeze().detach()

    def comparison(self, image):
        feature = self.image_feature(image)
        distance = F.pairwise_distance(feature, self.ref_features, p=2)
        print(distance)
        exit()

if __name__ == "__main__":

    image = face_recognition.load_image_file("input/5485.jpg_wh300.jpg")

    print(face_detection(image))
