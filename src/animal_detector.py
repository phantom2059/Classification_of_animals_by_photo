"""
Модуль для обнаружения и классификации животных на изображениях с использованием YOLOv8
"""

import cv2
import numpy as np
import torch
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
from .animal_classes import animal_classes_ru, get_animal_class_ids
from .animal_classifier import AnimalClassifier

class AnimalDetector:
    """
    Класс для обнаружения и классификации животных на изображениях с использованием YOLOv8
    """
    
    def __init__(self, model_path=None):
        """
        Инициализация детектора животных
        
        Args:
            model_path (str): Путь к модели YOLOv8. Если None, используется предобученная модель
        """
        try:
            if model_path and os.path.exists(model_path):
                self.model = YOLO(model_path)
            else:
                # Используем модель, обученную на Open Images Dataset
                self.model = YOLO('yolov8x-oiv7.pt')
            
            print("YOLOv8 успешно загружен!")
            
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}")
            raise
        
        # Получаем все классы из модели
        self.model_classes = self.model.names
        
        # Используем словарь переводов и автоматический выбор классов животных
        self.animal_classes_ru = animal_classes_ru
        self.animal_class_ids = get_animal_class_ids(self.model_classes)
        
        print(f"Обнаружено {len(self.animal_class_ids)} классов животных в Open Images Dataset")
    
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
        
        print("Обнаружение животных с помощью YOLOv8...")
        
        results = self.model(image, conf=conf_threshold)
            
        detected_animals = []
        
        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        if len(results) > 0:
            # Сначала собираем всех потенциальных животных
            potential_animals = []
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        coords = box.xyxy[0].tolist()
                        class_name = self.model_classes[class_id]
                        
                        if class_id in self.animal_class_ids and confidence >= max(conf_threshold, 0.3):
                            x1, y1, x2, y2 = [int(coord) for coord in coords]
                            animal_name_ru = self.animal_classes_ru.get(class_name, f"нет перевода: {class_name}")
                            
                            potential_animals.append({
                                'class_ru': animal_name_ru,
                                'class_en': class_name,
                                'confidence': confidence,
                                'bbox': (x1, y1, x2, y2),
                                'class_id': class_id,
                                'detection_method': 'YOLOv8'
                            })
            
            # Если есть животные с уверенностью ≥50%, показываем только их
            high_confidence_animals = [animal for animal in potential_animals if animal['confidence'] >= 0.5]
            if high_confidence_animals:
                animals_to_show = high_confidence_animals
            else:
                animals_to_show = potential_animals
            
            # Рисуем рамки только для выбранных животных
            for animal in animals_to_show:
                x1, y1, x2, y2 = animal['bbox']
                confidence = animal['confidence']
                animal_name_ru = animal['class_ru']
                
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
                
                detected_animals.append(animal)
            
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
    Пример использования детектора и классификатора для всех изображений из папки images
    """
    detector = AnimalDetector()
    classifier = AnimalClassifier()

    test_dir = "data/images"
    result_dir = "data/result"
    if not os.path.exists(test_dir):
        print(f"Папка {test_dir} не найдена!")
        return
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for filename in os.listdir(test_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(test_dir, filename)
            print(f"\nОбработка {filename}...")

            result_image, animals = detector.detect(image_path)

            print("Обнаруженные животные:")
            for animal in animals:
                print(f"- {animal['class_ru']} (уверенность: {animal['confidence']:.2f}) [YOLOv8]")

            print("Классификация изображения:")
            predictions = classifier.classify(image_path)
            for pred in predictions:
                print(f"- {pred['class_en']} (уверенность: {pred['confidence']:.2f})")

            output_path = os.path.join(result_dir, f"result_{filename}")
            detector.save_result(result_image, output_path)


if __name__ == "__main__":
    main() 