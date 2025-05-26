"""
Классификатор животных на основе нейронной сети
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2
from PIL import Image
import os


class AnimalClassifier:
    """
    Класс для классификации животных на изображениях
    """
    
    def __init__(self, model_path=None, img_size=(224, 224)):
        """
        Инициализация классификатора
        
        Args:
            model_path (str): Путь к сохраненной модели
            img_size (tuple): Размер изображения для обработки
        """
        self.model = None
        self.img_size = img_size
        self.classes = []
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def create_model(self, num_classes):
        """
        Создание модели CNN для классификации
        
        Args:
            num_classes (int): Количество классов животных
        """
        model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D(2, 2),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(512, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def preprocess_image(self, image_path):
        """
        Предобработка изображения для модели
        
        Args:
            image_path (str): Путь к изображению
            
        Returns:
            np.array: Предобработанное изображение
        """
        image = Image.open(image_path)
        image = image.convert('RGB')
        image = image.resize(self.img_size)
        image_array = np.array(image) / 255.0
        return np.expand_dims(image_array, axis=0)
    
    def predict(self, image_path):
        """
        Предсказание класса животного
        
        Args:
            image_path (str): Путь к изображению
            
        Returns:
            str: Предсказанный класс животного
        """
        if self.model is None:
            raise ValueError("Модель не загружена. Используйте load_model() или create_model()")
        
        processed_image = self.preprocess_image(image_path)
        predictions = self.model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        if self.classes:
            predicted_class = self.classes[predicted_class_idx]
        else:
            predicted_class = f"Класс {predicted_class_idx}"
        
        return predicted_class, confidence
    
    def train(self, train_data, validation_data, epochs=20):
        """
        Обучение модели
        
        Args:
            train_data: Данные для обучения
            validation_data: Данные для валидации
            epochs (int): Количество эпох
        """
        if self.model is None:
            raise ValueError("Модель не создана. Используйте create_model()")
        
        history = self.model.fit(
            train_data,
            epochs=epochs,
            validation_data=validation_data,
            callbacks=[
                keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                keras.callbacks.ReduceLROnPlateau(factor=0.2, patience=3)
            ]
        )
        
        return history
    
    def save_model(self, path):
        """
        Сохранение модели
        
        Args:
            path (str): Путь для сохранения
        """
        if self.model is None:
            raise ValueError("Модель не создана")
        
        self.model.save(path)
        print(f"Модель сохранена в {path}")
    
    def load_model(self, path):
        """
        Загрузка модели
        
        Args:
            path (str): Путь к модели
        """
        self.model = keras.models.load_model(path)
        print(f"Модель загружена из {path}")
    
    def set_classes(self, classes):
        """
        Установка списка классов
        
        Args:
            classes (list): Список названий классов
        """
        self.classes = classes 