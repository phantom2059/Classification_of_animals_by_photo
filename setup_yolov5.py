#!/usr/bin/env python3
"""
Скрипт автоматической установки YOLOv5 для работы с MegaDetector
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Выполнение команды с описанием"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ошибка:")
        print(f"Команда: {command}")
        print(f"Код ошибки: {e.returncode}")
        print(f"Вывод: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False

def main():
    """Основная функция установки"""
    print("🚀 Установка YOLOv5 для MegaDetector")
    print("=" * 50)
    
    # Проверяем, существует ли уже папка yolov5
    yolo_path = Path("yolov5")
    if yolo_path.exists():
        print("📁 Папка yolov5 уже существует")
        response = input("Удалить и переустановить? (y/N): ")
        if response.lower() == 'y':
            import shutil
            shutil.rmtree(yolo_path)
            print("🗑️ Старая папка yolov5 удалена")
        else:
            print("⏭️ Пропускаем клонирование")
            return
    
    # Клонируем YOLOv5
    if not run_command(
        "git clone https://github.com/ultralytics/yolov5.git",
        "Клонирование репозитория YOLOv5"
    ):
        return
    
    # Исправляем импорт scipy в plots.py
    plots_file = yolo_path / "utils" / "plots.py"
    if plots_file.exists():
        print("\n🔧 Исправление импорта scipy...")
        try:
            with open(plots_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Заменяем импорт
            content = content.replace(
                "from scipy.ndimage import gaussian_filter1d",
                "from scipy.ndimage import gaussian_filter1d"
            )
            
            with open(plots_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Импорт scipy исправлен")
        except Exception as e:
            print(f"❌ Ошибка при исправлении импорта: {e}")
    
    # Устанавливаем совместимые версии пакетов
    if not run_command(
        'pip install "numpy<2.0" "scipy>=1.7.0"',
        "Установка совместимых версий numpy и scipy"
    ):
        print("⚠️ Возможны проблемы с совместимостью пакетов")
    
    # Проверяем установку
    print("\n🧪 Проверка установки...")
    if Path("src/test_detector.py").exists():
        if run_command(
            "python src/test_detector.py",
            "Тестирование детектора"
        ):
            print("\n🎉 Установка завершена успешно!")
            print("Теперь вы можете использовать MegaDetector для детекции животных.")
        else:
            print("\n⚠️ Установка завершена, но тест не прошел")
            print("Проверьте логи выше для диагностики проблем")
    else:
        print("\n✅ YOLOv5 установлен")
        print("Файл test_detector.py не найден для проверки")

if __name__ == "__main__":
    main() 