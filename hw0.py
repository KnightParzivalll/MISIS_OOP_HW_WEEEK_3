"""
Создайте следующую иерархию классов:

Animal (базовый класс)
    Mammal
        Dog
        Cat
        Horse
    Bird
        Eagle
        Penguin
    Reptile
        Snake
        Turtle
"""

from abc import ABC

class Animal(ABC):
    """Abstract base class representing an animal."""
    def __init__(self, name):
        self.name = name

class Mammal(Animal):
    """Class representing mammals."""
    def __init__(self, name):
        super().__init__(name)

class Dog(Mammal):
    """Class representing a dog."""
    def __init__(self, name):
        super().__init__(name)

class Cat(Mammal):
    """Class representing a cat."""
    def __init__(self, name):
        super().__init__(name)

class Horse(Mammal):
    """Class representing a horse."""
    def __init__(self, name):
        super().__init__(name)

class Bird(Animal):
    """Class representing birds."""
    def __init__(self, name):
        super().__init__(name)

class Eagle(Bird):
    """Class representing an eagle."""
    def __init__(self, name):
        super().__init__(name)

class Penguin(Bird):
    """Class representing a penguin."""
    def __init__(self, name):
        super().__init__(name)

class Reptile(Animal):
    """Class representing reptiles."""
    def __init__(self, name):
        super().__init__(name)

class Snake(Reptile):
    """Class representing a snake."""
    def __init__(self, name):
        super().__init__(name)

class Turtle(Reptile):
    """Class representing a turtle."""
    def __init__(self, name):
        super().__init__(name)

# DEMO
animals = [
    Dog("Lenny"),
    Cat("Lemmy"),
    Horse("Manny"),
    Eagle("Sunny"),
    Penguin("Snowy"),
    Snake("Shish"),
    Turtle("Shelly")
]

print("Animals:")
for animal in animals:
    print(f"{animal.__class__.__name__}: {animal.name}")
