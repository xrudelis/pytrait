# Re-implementation of https://doc.rust-lang.org/rust-by-example/trait.html
from pytrait import Trait, Impl, Struct, abstractmethod


class Animal(metaclass=Trait):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def noise(self) -> str:
        pass

    def talk(self):
        print(f"{self.name()} says {self.noise()}")


class ImplAnimalForSheep(Animal, metaclass=Impl):
    def name(self) -> str:
        return self._name

    def noise(self) -> str:
        if self.is_naked():
            return "baaaaah?"
        else:
            return "baaaaah!"

    # Default trait methods can be overridden.
    def talk(self):
        print(f"{self.name()} pauses briefly... {self.noise()}")


class Sheep(metaclass=Struct):
    _name: str
    naked: bool = False

    def is_naked(self) -> bool:
        return self.naked

    def shear(self):
        if self.is_naked():
            print(f"{self._name} is already naked...")
        else:
            print(f"{self._name} gets a haircut!")
            self.naked = True


if __name__ == "__main__":
    dolly = Sheep(_name="Dolly")
    dolly.talk()
    dolly.shear()
    dolly.talk()
