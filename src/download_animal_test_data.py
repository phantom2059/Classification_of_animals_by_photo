"""
Скрипт для загрузки тестовых изображений животных из COCO dataset
"""

import os
import requests
from pathlib import Path

def download_image(url, filename):
    """
    Загрузка изображения по URL
    
    Args:
        url (str): URL изображения
        filename (str): Имя файла для сохранения
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Загружено: {filename}")
        return True
    except Exception as e:
        print(f"✗ Ошибка загрузки {filename}: {e}")
        return False

def main():
    """
    Основная функция для загрузки тестовых изображений животных из COCO
    """
    # Создаем директорию для тестовых данных
    test_dir = Path("data/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("🐾 Загрузка тестовых изображений животных COCO dataset...")
    print("=" * 60)
    
    # Словарь с URL изображений животных из COCO dataset
    # Только качественные изображения с правильными животными
    images = {
        # Птицы
        "bird1.jpg": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=640",
        
        # Коты
        "cat1.jpg": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=640",
        "cat2.jpg": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=640",
        
        # Собаки
        "dog1.jpg": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=640",
        "dog2.jpg": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=640",
        
        # Лошади
        "horse1.jpg": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=640",
        
        # Слоны
        "elephant1.jpg": "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=640",
        
        # Медведи
        "bear1.jpg": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=640",
        
        # Жирафы
        "giraffe1.jpg": "https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=640",
        
        # Смешанные изображения с несколькими животными
        "farm_animals.jpg": "https://images.unsplash.com/photo-1500595046743-cd271d694d30?w=640"
    }
    
    # Загружаем изображения
    successful_downloads = 0
    total_images = len(images)
    
    for filename, url in images.items():
        filepath = test_dir / filename
        
        # Пропускаем, если файл уже существует
        if filepath.exists():
            print(f"⏭ Пропущено (уже существует): {filename}")
            successful_downloads += 1
            continue
        
        print(f"📥 Загрузка: {filename}")
        if download_image(url, filepath):
            successful_downloads += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 ИТОГИ ЗАГРУЗКИ:")
    print(f"📁 Успешно загружено: {successful_downloads}/{total_images}")
    print(f"📂 Директория: {test_dir.absolute()}")
    print(f"🐾 Готово для тестирования YOLOv11x!")

if __name__ == "__main__":
    main() 