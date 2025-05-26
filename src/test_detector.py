"""
Скрипт для тестирования детектора животных с использованием MegaDetector
"""

import os
from pathlib import Path
from animal_detector import AnimalDetector


def test_detector(image_path=None):
    """
    Тестирование детектора животных
    
    Args:
        image_path (str): Путь к изображению. Если None, используется cat1.jpg
    """
    print(f"\nТестирование MegaDetector на изображении: {image_path}")
    
    # Создаем детектор
    print("Инициализация MegaDetector...")
    detector = AnimalDetector()
    
    # Если путь не указан, используем первое тестовое изображение
    if image_path is None:
        image_path = "data/test/cat1.jpg"
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"Файл {image_path} не найден!")
        print("Пожалуйста, запустите сначала скрипт download_test_data.py")
        return
    
    print(f"Файл {image_path} найден")
    
    # Выполняем обнаружение
    print("Выполняем обнаружение с помощью MegaDetector...")
    result_image, objects = detector.detect(image_path)
    
    # Выводим результаты
    print(f"\nРезультаты для {os.path.basename(image_path)}:")
    if objects:
        print("Обнаруженные объекты:")
        for obj in objects:
            print(f"- {obj['class_ru']} (уверенность: {obj['confidence']:.2f})")
    else:
        print("Объекты не обнаружены")
    
    # Сохраняем результат
    output_path = str(Path(image_path).parent / f"megadetector_result_{Path(image_path).stem}.jpg")
    print(f"Сохраняем результат в {output_path}")
    detector.save_result(result_image, output_path)
    
    print(f"Результат сохранен в {output_path}")


def test_all_images():
    """
    Тестирование на всех изображениях в директории test
    """
    print("Начинаем тестирование MegaDetector на всех изображениях...")
    
    test_dir = Path("data/test")
    if not test_dir.exists():
        print("Директория с тестовыми изображениями не найдена!")
        print("Пожалуйста, запустите сначала скрипт download_test_data.py")
        return
    
    print(f"Директория {test_dir} найдена")
    
    # Получаем список всех jpg файлов
    image_files = list(test_dir.glob("*.jpg"))
    # Исключаем файлы результатов
    image_files = [f for f in image_files if not f.name.startswith('result_') and not f.name.startswith('megadetector_result_')]
    
    if not image_files:
        print("Тестовые изображения не найдены!")
        print("Пожалуйста, запустите сначала скрипт download_test_data.py")
        return
    
    print(f"Найдено {len(image_files)} изображений для тестирования")
    
    # Тестируем каждое изображение
    for image_file in image_files:
        print(f"\n{'='*60}")
        test_detector(str(image_file))


if __name__ == "__main__":
    print("Запуск тестирования MegaDetector...")
    test_all_images()
    print("\nТестирование завершено!") 