"""
1. Создать несколько объектов классов Player, Enemy и Item с разными параметрами
2. Реализовать и запустить игровой цикл, используя предоставленный шаблон
3. Добавить новый класс Boss, который наследуется от Enemy, но имеет специальные способности:
    Особая атака, наносящая больше урона
    Больше здоровья и возможность восстанавливать здоровье
    Способность вызывать союзников (генерировать новых врагов)

4. Проанализировать и объяснить, что произойдет, если изменить порядок наследования в классе Character с (GameObject, Movable) на (Movable, GameObject) и почему
"""

from abc import ABC, abstractmethod
import random

# Базовые абстрактные классы
class GameObject(ABC):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    @abstractmethod
    def update(self):
        pass
    
    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"

class Movable(ABC):
    @abstractmethod
    def move(self, dx, dy):
        pass

# Наследники от базовых классов
class Character(GameObject, Movable):
    def __init__(self, x, y, name, health):
        super().__init__(x, y, name)
        self.health = health
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print(f"{self.name} moved to ({self.x}, {self.y})")
    
    def update(self):
        print(f"{self.name} updated, health: {self.health}")
    
    def is_alive(self):
        return self.health > 0

class Player(Character):
    def __init__(self, x, y, name, health, score=0):
        super().__init__(x, y, name, health)
        self.score = score
    
    def update(self):
        super().update()
        print(f"Player score: {self.score}")
    
    def collect_item(self, item):
        self.score += item.value
        print(f"Collected {item.name}, score: {self.score}")

class Enemy(Character):
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health)
        self.damage = damage
    
    def update(self):
        super().update()
        print(f"Enemy ready to attack with damage: {self.damage}")
    
    def attack(self, target):
        target.health -= self.damage
        print(f"{self.name} attacked {target.name} for {self.damage} damage")

class Item(GameObject):
    def __init__(self, x, y, name, value):
        super().__init__(x, y, name)
        self.value = value
    
    def update(self):
        print(f"Item {self.name} waiting to be collected")

class Boss(Enemy): # ADDED BOSS CLASS
    def __init__(self, x, y, name, health, damage):
        super().__init__(x, y, name, health, damage)
        self._next_attack_special = False
    
    def update(self):
        super().update()
        # 20% chance to heal each turn
        if random.random() < 0.2:
            self._heal()
        # 15% chance to summon minion at end of turn
        if random.random() < 0.15:
            self._summon_minion()
        # 10% chance to prepare special
        if random.random() < 0.1:
            self._next_attack_special = True
            print(f"{self.name} is preparing a special attack!")
    
    def _heal(self):
        heal_amount = random.randint(5, 15)
        self.health += heal_amount
        print(f"{self.name} healed for {heal_amount} HP!")
    
    def attack(self, target):
        if self._next_attack_special:
            print(f"{self.name} uses CRUSHING BLOW!")
            target.health -= self.damage * 2  # Double damage
            self._next_attack_special = False
            print(f"{self.name} attacked {target.name} for {self.damage * 2} damage")
        else:
            super().attack(target)
    
    def _summon_minion(self):
        minion = Enemy(self.x, self.y, f"{self.name}'s Minion", 30, 5)
        globals().get('enemies', []).append(minion)
        print(f"{self.name} summoned a minion!")

# Базовый игровой цикл
def game_loop(player, enemies, items, turns=5):
    print("\n=== GAME START ===\n")
    
    for turn in range(1, turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        # Обновление всех объектов
        player.update()
        for enemy in enemies:
            enemy.update()
        for item in items:
            item.update()
        
        # Враги атакуют игрока
        for enemy in enemies:
            if enemy.is_alive():
                enemy.attack(player)
        
        # Проверка сбора предметов
        for item in items[:]:  # Копия списка для безопасного удаления
            if item.x == player.x and item.y == player.y:
                player.collect_item(item)
                items.remove(item)
        
        # Проверка состояния игрока
        if not player.is_alive():
            print("\nИгрок погиб! Игра окончена.")
            break
        
        # Движение игрока (для примера - случайное)
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        player.move(dx, dy)
    
    print("\n=== GAME END ===")
    print(f"Final score: {player.score}")
    print(f"Player health: {player.health}")

# GAME
player = Player(0, 0, "Hero", 170)
enemies = [
    Enemy(2, 3, "Goblin", 10, 3),
    Enemy(5, 1, "Orc", 25, 7),
    Boss(4, 4, "Death King", 35 * 2, 10 * 2)  # Boss with double health and damage
]
items = [
    Item(1, 1, "Health Potion", 20),
    Item(3, 2, "Saint Sword", 30),
    Item(4, 0, "Magic Ring", 50)
]

print("Starting the adventure...\n")
game_loop(player, enemies, items, turns=8)

print("\n=== Stats ===")
print(f"Enemies remaining: {len([e for e in enemies if e.is_alive()])}")
print(f"Items left: {len(items)}")


"""
4. В данной реализации ничего не изменится при смене порядка наследования, потому что в родительских классах GameObject и Movable нет 
методов с одинаковыми именами, так что они не конфликтуют между собой, и super() корректно находит все нужные методы. Однако логически 
правильнее оставить текущий порядок (GameObject, Movable), так как GameObject является фундаментальным классом, определяющим сущность 
игрового объекта, тогда как Movable добавляет лишь дополнительную функциональность для перемещения. Такой порядок лучше отражает 
архитектурную иерархию "от общего к частному" и соответствует принципам хорошего ООП-дизайна.
"""