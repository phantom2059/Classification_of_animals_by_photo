# Animal Classification by Photo

**Двухэтапная детекция и классификация животных на изображениях с YOLOv8**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00BFFF?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-1.8+-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## Overview

Автоматическое обнаружение и классификация животных на изображениях с помощью двухэтапного пайплайна YOLOv8. Детектор (YOLOv8x, обученный на Open Images Dataset) находит животных и определяет вид среди 72 классов, а дополнительный классификатор (YOLOv8x-cls, обученный на ImageNet) подтверждает результат. Все названия классов переведены на русский язык.

---

## Pipeline

1. **Detection** — YOLOv8x-oiv7 находит bounding boxes и определяет вид животного среди 72 классов.
2. **Classification** — YOLOv8x-cls запускается на полном изображении для перекрёстной проверки.
3. **Filtering** — умная пороговая фильтрация: при наличии высоко-уверенных детекций (≥50%) менее уверенные результаты подавляются.
4. **Visualization** — цветовые рамки с русскоязычными подписями.

Цветовое кодирование уверенности:
- Красный — высокая уверенность (≥80%)
- Оранжевый — хорошая уверенность (≥50%)
- Жёлтый — удовлетворительная уверенность (≥30%)

---

## Quick start

```bash
git clone https://github.com/phantom2059/Classification_of_animals_by_photo.git
cd Classification_of_animals_by_photo
pip install -r requirements.txt
```

Модели (`yolov8x-oiv7.pt`, `yolov8x-cls.pt`) скачиваются автоматически при первом запуске.

### Обработка тестовых изображений

```bash
python -m src.animal_detector
```

### Программное использование

```python
from src.animal_detector import AnimalDetector
from src.animal_classifier import AnimalClassifier

detector = AnimalDetector()
classifier = AnimalClassifier()

result_image, animals = detector.detect("path/to/image.jpg")
for a in animals:
    print(f"{a['class_ru']}: {a['confidence']:.2f}")

predictions = classifier.classify("path/to/image.jpg")
for pred in predictions:
    print(f"{pred['class_en']}: {pred['confidence']:.2f}")

detector.save_result(result_image, "result.jpg")
```

Результаты сохраняются в `data/result/`.

---

## Examples

<p align="center">
  <img src="images_readme/bird1_yolo11x.jpg" width="420"/>
  &nbsp;&nbsp;
  <img src="images_readme/elephant1_yolo11x.jpg" width="420"/>
</p>

<p align="center">
  <img src="images_readme/farm_animals_yolo11x.jpg" width="420"/>
</p>

Примеры результатов: белый медведь (0.99), фермерские животные — 4 коровы (0.94, 0.88, 0.86, 0.86), слоны (0.95, 0.93), лошадь (0.97).

---

## Supported classes

72 класса животных из Open Images Dataset, сгруппированных по категориям:

- **Птицы** (15) — орёл, утка, лебедь, гусь, попугай, сова, дятел, сорока, голубь, воробей, канарейка, сокол, ворон и др.
- **Домашние** (10) — кот, собака, КРС, лошадь, овца, коза, свинья, курица, кролик, хомяк
- **Морские** (12) — кит, дельфин, акула, тюлень, краб, омар, креветка, морская звезда, медуза, осьминог, кальмар, золотая рыбка
- **Дикие** (28) — слон, жираф, носорог, бегемот, зебра, лев, тигр, ягуар, рысь, медведь, белый медведь, панда, волк, лиса, енот, олень, кенгуру, коала, обезьяна и др.
- **Прочие** (7) — лягушка, черепаха, крокодил, ящерица, змея, улитка, паук

Полный список с русскими переводами — в `src/animal_classes.py`.

---

## Project structure

```
├── src/
│   ├── animal_detector.py     # Модуль детекции (YOLOv8x-oiv7)
│   ├── animal_classifier.py   # Модуль классификации (YOLOv8x-cls)
│   ├── animal_classes.py      # Определения классов + русские переводы
│   └── __init__.py
├── data/
│   ├── images/                # Тестовые изображения
│   └── result/                # Результаты с bounding boxes
├── images_readme/             # Примеры для README
├── requirements.txt
└── LICENSE
```

---

## License

MIT
