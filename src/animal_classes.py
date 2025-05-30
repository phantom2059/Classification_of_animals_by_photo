# animal_classes.py

# Словарь переводов классов животных (можно дополнять)
animal_classes_ru = {
    'Animal': 'животное',
    'Mammal': 'млекопитающее',
    'Dog': 'собака',
    'Cat': 'кот',
    'Horse': 'лошадь',
    'Cow': 'корова',
    'Pig': 'свинья',
    'Sheep': 'овца',
    'Goat': 'коза',
    'Deer': 'олень',
    'Elephant': 'слон',
    'Giraffe': 'жираф',
    'Zebra': 'зебра',
    'Lion': 'лев',
    'Tiger': 'тигр',
    'Leopard': 'леопард',
    'Jaguar': 'ягуар',
    'Cheetah': 'гепард',
    'Bear': 'медведь',
    'Polar bear': 'белый медведь',
    'Panda': 'панда',
    'Koala': 'коала',
    'Kangaroo': 'кенгуру',
    'Monkey': 'обезьяна',
    'Gorilla': 'горилла',
    'Chimpanzee': 'шимпанзе',
    'Orangutan': 'орангутан',
    'Rabbit': 'кролик',
    'Hamster': 'хомяк',
    'Guinea pig': 'морская свинка',
    'Mouse': 'мышь',
    'Rat': 'крыса',
    'Squirrel': 'белка',
    'Chipmunk': 'бурундук',
    'Beaver': 'бобр',
    'Otter': 'выдра',
    'Seal': 'тюлень',
    'Sea lion': 'морской лев',
    'Walrus': 'морж',
    'Dolphin': 'дельфин',
    'Whale': 'кит',
    'Shark': 'акула',
    'Bat': 'летучая мышь',
    'Fox': 'лиса',
    'Wolf': 'волк',
    'Coyote': 'койот',
    'Hyena': 'гиена',
    'Raccoon': 'енот',
    'Skunk': 'скунс',
    'Hedgehog': 'еж',
    'Sloth': 'ленивец',
    'Anteater': 'муравьед',
    'Armadillo': 'броненосец',
    'Platypus': 'утконос',
    'Echidna': 'ехидна',
    'Bird': 'птица',
    'Cattle': 'крупный рогатый скот',
    'Ox': 'вол',
    'Ram': 'баран',
    'Hare': 'заяц',
    'Bull': 'бык',
    # ... (дополнить по необходимости)
}

# Ключевые слова для автоматического выбора животных классов
ANIMAL_KEYWORDS = [
    "cat", "dog", "elephant", "horse", "giraffe", "bear", "bird", "cattle", "ox", "ram", "goat", "sheep", "pig", "cow", "bull", "lion", "tiger", "wolf", "fox", "deer", "rabbit", "hare", "mouse", "rat", "squirrel", "hedgehog", "bat",
    "zebra", "leopard", "jaguar", "cheetah", "panda", "koala", "kangaroo", "monkey", "gorilla", "chimpanzee", "orangutan", "hamster", "guinea", "chipmunk", "beaver", "otter", "seal", "walrus", "dolphin", "whale", "shark", "coyote", "hyena", "raccoon", "skunk", "sloth", "anteater", "armadillo", "platypus", "echidna",
    "mammal", "reptile", "amphibian", "fish", "insect", "animal"
]

import csv
import os

def get_animal_class_ids(model_classes):
    animal_ids = []
    for idx in model_classes:
        class_name = model_classes[idx]
        if isinstance(class_name, str):
            name = class_name.lower()
            if any(keyword in name for keyword in ANIMAL_KEYWORDS):
                animal_ids.append(idx)
    return animal_ids 