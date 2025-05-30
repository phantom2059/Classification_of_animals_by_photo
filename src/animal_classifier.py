import torch
from ultralytics import YOLO
from PIL import Image
import numpy as np
from .animal_classes import ANIMAL_KEYWORDS

class AnimalClassifier:
    """
    Класс для классификации животных на изображениях с помощью YOLOv8x-классификатора
    """
    def __init__(self, model_path='yolov8x-cls.pt'):
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        print(f"YOLOv8x-классификатор успешно загружен! Классов: {len(self.class_names)}")

    def classify(self, image_path, topk=3):
        """
        Классифицирует изображение, возвращает top-k наиболее вероятных классов
        Args:
            image_path (str): путь к изображению
            topk (int): сколько топовых классов возвращать
        Returns:
            list: список словарей с классами и вероятностями
        """
        image = Image.open(image_path).convert('RGB')
        results = self.model(image)
        probs = results[0].probs
        if not isinstance(probs, torch.Tensor):
            probs = torch.tensor(probs.data)
        topk_indices = torch.topk(probs, topk).indices.cpu().numpy()
        topk_scores = torch.topk(probs, topk).values.cpu().numpy()
        predictions = []
        for idx, score in zip(topk_indices, topk_scores):
            class_name = self.class_names[idx]
            predictions.append({
                'class_en': class_name,
                'confidence': float(score),
                'class_id': int(idx)
            })
        return predictions

if __name__ == "__main__":
    clf = AnimalClassifier()
    preds = clf.classify('data/images/cat1.jpg')
    print(preds) 