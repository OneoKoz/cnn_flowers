import json
import numpy as np
import torch
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from fastapi import File


class Model:
    PATH_MODEL = 'src/efficientnet_b5.pt'
    CONFIG_PATH = 'src/config.json'

    def __init__(self):
        with open(self.CONFIG_PATH) as f:
            self.config = json.load(f)
        self.model = torch.load(self.PATH_MODEL, map_location=torch.device('cpu'))
        self.model.eval()

    def make_predict(self, file: File):
        img = self.get_correct_format_img(file)
        answer_dict = torch.topk(self.model(img), k=5)
        answer_prob = answer_dict.values[0].tolist()
        answer_group = list(np.array(answer_dict.indices)[0] + 1)
        return answer_group, answer_prob

    def get_correct_format_img(self, file):
        file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        transform = A.Compose([
            A.Resize(height=self.config['input_shape_image']['height'],
                     width=self.config['input_shape_image']['width']),
            A.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]),
            ToTensorV2()
        ])
        img = transform(image=img)['image'].unsqueeze(0)
        return img
