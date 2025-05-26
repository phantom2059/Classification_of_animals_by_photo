"""
Скрипт для загрузки тестовых изображений животных
"""

import os
import requests
from pathlib import Path
import shutil


def download_file(url, filename):
    """
    Загрузка файла по URL
    
    Args:
        url (str): URL файла
        filename (str): Имя файла для сохранения
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def setup_test_data():
    """
    Настройка тестовых данных
    """
    # Создаем директории
    test_dir = Path("data/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Список тестовых изображений (URL и имена файлов)
    test_images = [
        {
            "url": "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg",
            "filename": "cat1.jpg"
        },
        {
            "url": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg",
            "filename": "dog1.jpg"
        },
        {
            "url": "https://images.pexels.com/photos/52500/horse-herd-fog-nature-52500.jpeg",
            "filename": "horse1.jpg"
        },
        {
            "url": "https://images.pexels.com/photos/45911/peacock-bird-plumage-color-45911.jpeg",
            "filename": "bird1.jpg"
        }
    ]
    
    print("Загрузка тестовых изображений...")
    
    # Загружаем каждое изображение
    for img in test_images:
        filepath = test_dir / img["filename"]
        if not filepath.exists():
            print(f"Загрузка {img['filename']}...")
            try:
                download_file(img["url"], filepath)
                print(f"✓ {img['filename']} загружен")
            except Exception as e:
                print(f"✗ Ошибка при загрузке {img['filename']}: {e}")
        else:
            print(f"✓ {img['filename']} уже существует")
    
    print("\nТестовые данные готовы!")
    print(f"Изображения находятся в директории: {test_dir.absolute()}")


if __name__ == "__main__":
    setup_test_data() 