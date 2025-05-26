# Установка YOLOv5 для MegaDetector

Для работы с MegaDetector необходимо клонировать репозиторий YOLOv5 локально.

## Автоматическая установка

Запустите скрипт установки:

```bash
python setup_yolov5.py
```

## Ручная установка

1. Клонируйте репозиторий YOLOv5:
```bash
git clone https://github.com/ultralytics/yolov5.git
```

2. Исправьте импорт scipy в файле `yolov5/utils/plots.py`:
```python
# Замените строку:
from scipy.ndimage import gaussian_filter1d

# На:
from scipy.ndimage import gaussian_filter1d
```

3. Установите совместимые версии пакетов:
```bash
pip install "numpy<2.0" "scipy>=1.7.0"
```

## Проверка установки

Запустите тест:
```bash
python src/test_detector.py
```

Если все работает корректно, вы увидите результаты детекции животных.

## Примечания

- YOLOv5 исключен из Git репозитория из-за большого размера
- Модель MegaDetector (268MB) также исключена и скачивается автоматически
- При первом запуске может потребоваться время на загрузку модели 