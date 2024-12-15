import os
import cv2
import numpy as np
from tqdm import tqdm

import torch
import torch.nn.functional as F

import face_recognition
from facenet_pytorch import MTCNN, InceptionResnetV1

def face_detection(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    return bool(len(face_landmarks_list))

class FaceComparison:
    def __init__(self, device="cpu"):
        self.device = device
        self.mtcnn = MTCNN(device=device)
        self.resnet = InceptionResnetV1(pretrained='vggface2', device=device).eval()
        self.ref_image_path = "ref_data/"
        self.ref_features_path = "ref_data/ref_features.pt"
        self._get_ref_features()
        self.label_name = {
            "catfish": "鲶鱼",
            "dog": "犬",
            "frog": "蛙",
            "rat": "鼠",
            "sheep": "羊"
        }
    
    def _get_ref_features(self):
        if os.path.exists(self.ref_features_path):
            print("[INFO] 加载已有的参考特征文件")
            tmp = torch.load(self.ref_features_path)
            self.ref_features = tmp["features"].to(self.device)
            self.ref_labels = tmp["labels"]
            return
        print("[INFO] 首次运行，正在生成参考图像特征。")
        self.ref_features = []
        self.ref_labels = []
        for root, dirs, files in os.walk(self.ref_image_path):
            for file in tqdm(files):
                label = file.split("_")[0]
                image_path = os.path.join(root, file)
                print("正在加载参考图像:", image_path)  # 新增调试信息
                image = cv2.imread(image_path)
                if image is None:
                    print("[WARNING] 图像加载失败:", image_path)
                    continue
                feature = self.image_feature(image)
                self.ref_features.append(feature)
                self.ref_labels.append(label)
            break
        if not self.ref_features:
            raise ValueError("[ERROR] 无法生成参考特征，请检查 ref_data 文件夹中的图像。")
        self.ref_features = torch.stack(self.ref_features)
        torch.save({"features": self.ref_features.detach().cpu(), "labels": self.ref_labels}, self.ref_features_path)
        

    def image_feature(self, image):
        image_cropped = self.mtcnn(image)
        if image_cropped is None:
            raise ValueError("[ERROR] MTCNN 未能检测到人脸，请确保上传的图像包含清晰的人脸")
        image_cropped = image_cropped.to(self.device)
        img_embedding = self.resnet(image_cropped.unsqueeze(0))
        return img_embedding.squeeze().detach()       

     # 新增方法：检查是否包含人脸
    def has_face(self, image):
        """
        检测输入图像中是否包含人脸。
        :param image: 输入的图像
        :return: 如果检测到人脸返回 True，否则返回 False
        """
        try:
            image_cropped = self.mtcnn(image)  # 尝试检测人脸
            return image_cropped is not None  # 如果检测到，返回 True
        except Exception as e:
            print(f"[WARNING] 检测人脸失败: {e}")
            return False
    
    def comparison(self, image, output=None, similarity_threshold=0.5):
        try:
            feature = self.image_feature(image)
        except ValueError as e:
            print("[WARNING] 人脸检测失败:", e)
            return "未识别到有效分类"

        similarity = self.ref_features @ feature
        max_idx = torch.argmax(similarity).item()
        max_similarity = similarity[max_idx].item()

        if max_similarity < similarity_threshold:
            return "未识别到有效分类"

        label = self.ref_labels[max_idx]
        if output is None:
            return label
        else:
            output.append(label)




if __name__ == "__main__":

    image = face_recognition.load_image_file("input/5485.jpg_wh300.jpg")

    print(face_detection(image))
