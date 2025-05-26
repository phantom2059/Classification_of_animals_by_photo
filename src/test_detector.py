"""
Тестовый скрипт для проверки работы детектора животных на основе YOLOv11x
"""

import os
import sys
from pathlib import Path
from animal_detector import AnimalDetector

def test_all_animals():
    """
    Тестирование детектора на всех изображениях животных
    """
    # Создаем детектор
    print("Инициализация детектора животных YOLOv11x...")
    detector = AnimalDetector()
    
    # Создаем директории для результатов
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    print(f"Результаты будут сохранены в: {results_dir.absolute()}")
    
    # Путь к тестовым изображениям
    test_dir = Path("data/test")
    
    if not test_dir.exists():
        print(f"Директория {test_dir} не найдена!")
        print("Запустите сначала: python src/download_animal_test_data.py")
        return
    
    # Получаем список всех изображений
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(test_dir.glob(f"*{ext}"))
        image_files.extend(test_dir.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"Изображения не найдены в {test_dir}")
        return
    
    print(f"\nНайдено {len(image_files)} изображений для тестирования")
    print("=" * 60)
    
    total_animals_found = 0
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Обработка: {image_path.name}")
        print("-" * 40)
        
        try:
            # Выполняем детекцию
            result_image, detected_animals = detector.detect(str(image_path), conf_threshold=0.25)
            
            # Выводим результаты
            if detected_animals:
                print(f"🐾 Найдено животных: {len(detected_animals)}")
                for animal in detected_animals:
                    print(f"  - {animal['class_ru']} (уверенность: {animal['confidence']:.2f}) [YOLOv11x]")
                total_animals_found += len(detected_animals)
            else:
                print("❌ Животные не обнаружены")
            
            # Сохраняем результат
            base_name = image_path.stem
            output_path = results_dir / f"{base_name}_yolo11x.jpg"
            detector.save_result(result_image, str(output_path))
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {image_path.name}: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 ИТОГИ ТЕСТИРОВАНИЯ YOLOv11x:")
    print(f"📁 Обработано изображений: {len(image_files)}")
    print(f"🐾 Всего найдено животных: {total_animals_found}")
    print(f"📊 Среднее количество животных на изображение: {total_animals_found/len(image_files):.1f}")
    print(f"📂 Результаты сохранены в папке: {results_dir.absolute()}")

def main():
    """
    Основная функция
    """
    print("🐾 ТЕСТИРОВАНИЕ ДЕТЕКТОРА ЖИВОТНЫХ YOLOv11x 🐾")
    print("=" * 60)
    
    # Запускаем тестирование
    test_all_animals()

if __name__ == "__main__":
    main() 