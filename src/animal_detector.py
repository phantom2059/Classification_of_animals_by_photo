"""
Модуль для обнаружения и классификации животных на изображениях с использованием MegaDetector
"""

import cv2
import numpy as np
import torch
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Добавляем путь к YOLOv5
yolo_path = Path(__file__).parent.parent / 'yolov5'
if yolo_path.exists():
    sys.path.insert(0, str(yolo_path))


class AnimalDetector:
    """
    Класс для обнаружения и классификации животных на изображениях с использованием MegaDetector
    """
    
    def __init__(self, model_path=None):
        """
        Инициализация детектора животных
        
        Args:
            model_path (str): Путь к модели MegaDetector. Если None, используется предобученная модель
        """
        try:
            # Загружаем MegaDetector через локальный YOLOv5
            if model_path and os.path.exists(model_path):
                self.model = torch.hub.load(str(yolo_path), 'custom', path=model_path, source='local', force_reload=True)
            else:
                # Используем локальную модель MegaDetector v5a
                model_path = 'models/md_v5a.0.0.pt'
                if os.path.exists(model_path):
                    self.model = torch.hub.load(str(yolo_path), 'custom', path=model_path, source='local', force_reload=True)
                else:
                    raise FileNotFoundError(f"Модель MegaDetector не найдена: {model_path}")
            
            print("MegaDetector успешно загружен!")
            
        except Exception as e:
            print(f"Ошибка при загрузке MegaDetector: {e}")
            raise
        
        # Словарь с русскими названиями классов MegaDetector
        # MegaDetector имеет 3 класса: 0=animal, 1=person, 2=vehicle
        self.class_names_ru = {
            0: 'животное',
            1: 'человек', 
            2: 'транспорт'
        }
        
        # Словарь с английскими названиями
        self.class_names_en = {
            0: 'animal',
            1: 'person',
            2: 'vehicle'
        }
    
    def detect(self, image_path, conf_threshold=0.1):
        """
        Обнаружение животных на изображении
        
        Args:
            image_path (str): Путь к изображению
            conf_threshold (float): Порог уверенности для детекции
            
        Returns:
            tuple: (изображение с разметкой, список обнаруженных объектов)
        """
        # Загружаем изображение
        image = Image.open(image_path)
        
        # Выполняем предсказание с помощью MegaDetector
        self.model.conf = conf_threshold
        results = self.model(image)
        
        # Список для хранения обнаруженных объектов
        detected_objects = []
        
        # Создаем копию изображения для рисования
        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)
        
        # Пытаемся загрузить шрифт, если не получается - используем стандартный
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Обрабатываем результаты
        detections = results.pandas().xyxy[0]
        
        for _, detection in detections.iterrows():
            confidence = detection['confidence']
            class_id = int(detection['class'])
            
            # Проверяем порог уверенности
            if confidence >= conf_threshold:
                # Получаем координаты рамки
                x1, y1, x2, y2 = int(detection['xmin']), int(detection['ymin']), int(detection['xmax']), int(detection['ymax'])
                
                # Выбираем цвет в зависимости от категории
                if class_id == 0:  # животное
                    color = "red"
                elif class_id == 1:  # человек
                    color = "blue"
                elif class_id == 2:  # транспорт
                    color = "green"
                else:
                    color = "yellow"
                
                # Рисуем рамку с увеличенной толщиной (5 пикселей)
                draw.rectangle([x1, y1, x2, y2], outline=color, width=5)
                
                # Формируем текст с названием и уверенностью
                class_name = self.class_names_ru.get(class_id, f'класс_{class_id}')
                label = f"{class_name} {confidence:.2f}"
                
                # Рисуем фон для текста
                text_bbox = draw.textbbox((x1, y1-35), label, font=font)
                draw.rectangle(text_bbox, fill=color)
                
                # Рисуем текст
                draw.text((x1, y1-35), label, fill="white", font=font)
                
                # Добавляем информацию в список
                detected_objects.append({
                    'class_ru': class_name,
                    'class_en': self.class_names_en.get(class_id, f'class_{class_id}'),
                    'confidence': confidence,
                    'bbox': (x1, y1, x2, y2),
                    'category': class_id
                })
        
        return draw_image, detected_objects
    
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
    # Создаем детектор
    detector = AnimalDetector()
    
    # Путь к тестовому изображению
    image_path = "data/test/cat1.jpg"
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден!")
        return
    
    # Выполняем обнаружение
    result_image, objects = detector.detect(image_path)
    
    # Выводим результаты
    print("\nОбнаруженные объекты:")
    for obj in objects:
        print(f"- {obj['class_ru']} (уверенность: {obj['confidence']:.2f})")
    
    # Сохраняем результат
    output_path = "data/test/result_megadetector.jpg"
    detector.save_result(result_image, output_path)


if __name__ == "__main__":
    main() 