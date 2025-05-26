# Классификация животных по фотографиям

Проект для автоматической классификации животных на изображениях с использованием машинного обучения.

## Описание

Этот проект использует нейронные сети для распознавания и классификации различных видов животных на фотографиях.

## Функциональность

- Загрузка и предобработка изображений
- Обучение модели классификации
- Предсказание вида животного по фотографии
- Оценка точности модели

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```python
from animal_classifier import AnimalClassifier

classifier = AnimalClassifier()
classifier.load_model()
prediction = classifier.predict('path/to/image.jpg')
print(f"Обнаружено животное: {prediction}")
```

## Структура проекта

```
Classification_of_animals_by_photo/
│
├── data/                 # Данные для обучения
├── models/              # Сохраненные модели
├── src/                 # Исходный код
├── notebooks/           # Jupyter ноутбуки
├── requirements.txt     # Зависимости
└── README.md           # Этот файл
```

## Лицензия

MIT License 