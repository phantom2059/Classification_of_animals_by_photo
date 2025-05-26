"""
Простой скрипт для тестирования детектора на одном изображении
"""

import sys
from pathlib import Path
from animal_detector import AnimalDetector

def test_single_image(image_path):
    """
    Тестирование детектора на одном изображении
    
    Args:
        image_path (str): Путь к изображению
    """
    if not Path(image_path).exists():
        print(f"❌ Файл {image_path} не найден!")
        return
    
    print(f"🐾 Тестирование изображения: {image_path}")
    print("Инициализация YOLOv11x...")
    
    detector = AnimalDetector()
    
    result_image, detected_objects = detector.detect(image_path)
    
    if detected_objects:
        print(f"🎯 Найдено животных: {len(detected_objects)}")
        for i, obj in enumerate(detected_objects, 1):
            print(f"  {i}. {obj['class_ru']} (уверенность: {obj['confidence']:.2f})")
    else:
        print("😔 Животные не обнаружены")
    
    output_path = f"results/{Path(image_path).stem}_result.jpg"
    Path("results").mkdir(exist_ok=True)
    result_image.save(output_path)
    print(f"💾 Результат сохранен: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python src/test_single.py <путь_к_изображению>")
        print("Пример: python src/test_single.py data/test/cat1.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_single_image(image_path) 