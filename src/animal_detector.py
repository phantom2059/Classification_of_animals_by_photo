"""
Модуль для обнаружения и классификации животных на изображениях с использованием YOLOv11x
"""

import cv2
import numpy as np
import torch
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

class AnimalDetector:
    """
    Класс для обнаружения и классификации животных на изображениях с использованием YOLOv11x
    """
    
    def __init__(self, model_path=None):
        """
        Инициализация детектора животных
        
        Args:
            model_path (str): Путь к модели YOLOv11x. Если None, используется предобученная модель
        """
        try:
            if model_path and os.path.exists(model_path):
                self.model = YOLO(model_path)
            else:
                self.model = YOLO('yolo11x.pt')
            
            print("YOLOv11x успешно загружен!")
            
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            raise
        
        # Словарь с русскими названиями животных из COCO dataset
        self.animal_classes_ru = {
            'bird': 'птица',
            'cat': 'кот',
            'dog': 'собака', 
            'horse': 'лошадь',
            'sheep': 'овца',
            'cow': 'корова',
            'elephant': 'слон',
            'bear': 'медведь',
            'zebra': 'зебра',
            'giraffe': 'жираф'
        }
        
        # Получаем все классы COCO
        self.coco_classes = self.model.names
        
        # Определяем какие классы являются животными
        self.animal_class_ids = []
        for class_id, class_name in self.coco_classes.items():
            if class_name in self.animal_classes_ru:
                self.animal_class_ids.append(class_id)
        
        print(f"Обнаружено {len(self.animal_class_ids)} классов животных в COCO")
    
    def detect(self, image_path, conf_threshold=0.25):
        """
        Обнаружение и классификация животных на изображении
        
        Args:
            image_path (str): Путь к изображению
            conf_threshold (float): Порог уверенности для детекции
            
        Returns:
            tuple: (изображение с разметкой, список обнаруженных объектов)
        """
        image = Image.open(image_path)
        
        print("Обнаружение животных с помощью YOLOv11x...")
        
        results = self.model(image, conf=conf_threshold)
            
        detected_animals = []
        
        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        if len(results) > 0:
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        coords = box.xyxy[0].tolist()
                        class_name = self.coco_classes[class_id]
                        
                        if class_id in self.animal_class_ids and confidence >= conf_threshold:
                            x1, y1, x2, y2 = [int(coord) for coord in coords]
                            
                            animal_name_ru = self.animal_classes_ru.get(class_name, class_name)
                            
                            if confidence >= 0.8:
                                color = "red"
                            elif confidence >= 0.5:
                                color = "orange"
                            else:
                                color = "yellow"
                            
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=6)
                            
                            label = f"{animal_name_ru} {confidence:.2f}"
                            
                            text_bbox = draw.textbbox((x1, y1-40), label, font=font)
                            draw.rectangle(text_bbox, fill=color)
                            
                            draw.text((x1, y1-40), label, fill="white", font=font)
                            
                            detected_animals.append({
                                'class_ru': animal_name_ru,
                                'class_en': class_name,
                                'confidence': confidence,
                                'bbox': (x1, y1, x2, y2),
                                'class_id': class_id,
                                'detection_method': 'YOLOv11x'
                            })
            
        return draw_image, detected_animals
    
    def save_result(self, image, output_path):
        """
        Сохранение результата
        
        Args:
            image: Изображение с разметкой
            output_path (str): Путь для сохранения
        """
        image.save(output_path)
        print(f"Результат сохранен в {output_path}")


def main():
    """
    Пример использования детектора
    """
    detector = AnimalDetector()
    
    image_path = "data/test/cat1.jpg"
    
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден!")
        return
    
    result_image, animals = detector.detect(image_path)
    
    print("\nОбнаруженные животные:")
    for animal in animals:
        print(f"- {animal['class_ru']} (уверенность: {animal['confidence']:.2f}) [YOLOv11x]")
    
    output_path = "data/test/result_yolo11x.jpg"
    detector.save_result(result_image, output_path)


if __name__ == "__main__":
    main() 