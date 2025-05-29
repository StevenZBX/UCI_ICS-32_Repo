# NAME
# EMAIL
# STUDENT ID


from abc import ABC, abstractmethod
import random,enum

class Appetite:
    LOW = 3
    MEDIUM = 4
    HIGH = 5

class Dog(ABC):
    def __init__(self, name, age, appetite) -> None:
        self.hunger_clock = 0
        self._name = name
        self._age = age 
        self.appetite = appetite

    @abstractmethod
    def breed(self):
        pass
    
    def name(self):
        return self._name
    
    def age(self):
        return self._age

    def hungry(self):
        """
        The hungry method will check the hungry clock to see if some time has
        passed since the last feeding. If clock is greater than breed typical
        appetite, hunger assessment is randomly selected, otherwise hunger clock increases
        """
        if self.hunger_clock > self.appetite:
            return bool(random.getrandbits(1))
        else:
            self.hunger_clock += 1
            return False

    def feed(self):
        """
        Feeds the dog. Hunger clock is reset
        """
        self.hunger_clock = 0

class GermanShepherd(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "German Shepherd"

class GoldenRetriever(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "Golden Retriever"

class AnatolianShepherd(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "Anatolian Shepherd"
    

if __name__ == '__main__':
    dog = None
    breed = input("What breed of dog would you like to care for? \n\n 1. German Shepherd \n 2. Golden Retriever \n 3. Anatolian Shepherd \n: ")
    name = input("What would you like to name your dog? ")
    age = input("How old would you like your dog to be? ")
    age = int(age)
    if breed == "1":
        dog = GermanShepherd(name, age)
    elif breed == "2":
        dog = GoldenRetriever(name, age)
    elif breed == "3":
        dog = AnatolianShepherd(name, age)
    else:
        print("I didn't understand your entry, please run again.")

    q = False
    while q == False:
        h = ""
        if dog.hungry() == False:
            h = "not "
        print(f"Your {dog.breed()}, {dog.name()} is {h}hungry.")
        feed = input(f"Would you like to feed {dog.name()}? (y/n/q): ")

        if feed == "y":
            dog.feed()
        elif feed == "q":
            break
