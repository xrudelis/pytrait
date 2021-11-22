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


class Person(metaclass=Trait):
    @abstractmethod
    def first_name(self) -> str:
        pass

    @abstractmethod
    def last_name(self) -> str:
        pass


class ImplAnimal(Animal, metaclass=Impl, target="Person"):
    """All people are also animals"""

    def name(self) -> str:
        return f"{self.first_name()} {self.last_name()}"

    def noise(self) -> str:
        return "Hello"


class ImplPerson(Person, metaclass=Impl, target="Englishman"):
    def first_name(self) -> str:
        return self._first_name

    def last_name(self) -> str:
        return "Smith"


class Englishman(metaclass=Struct):
    _first_name: str

    def noise(self) -> str:
        return "Good day to you, sir!"


if __name__ == "__main__":
    johnny = Englishman("John")
    johnny.talk()
