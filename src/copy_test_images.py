"""
Скрипт для копирования тестовых изображений
"""

import os
from pathlib import Path
import shutil


def copy_test_images():
    """
    Копирование изображений из директории images в test
    """
    # Создаем директории
    images_dir = Path("data/images")
    test_dir = Path("data/test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("Копирование тестовых изображений...")
    
    # Копируем все изображения из директории images
    for img_file in images_dir.glob("*.jpg"):
        dest_file = test_dir / img_file.name
        if not dest_file.exists():
            print(f"Копирование {img_file.name}...")
            shutil.copy2(img_file, dest_file)
            print(f"✓ {img_file.name} скопирован")
        else:
            print(f"✓ {img_file.name} уже существует")
    
    print("\nТестовые данные готовы!")
    print(f"Изображения находятся в директории: {test_dir.absolute()}")


if __name__ == "__main__":
    copy_test_images() 