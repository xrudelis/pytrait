from pytrait import Trait, Impl, Struct, abstractmethod


class Building(metaclass=Trait):
    @abstractmethod
    def floor_area(self) -> float:
        pass


class Residence(Building, metaclass=Trait):
    """
    Residence has Building as a supertrait, so it is a superset of Building.

    All types implementing Residence must also implement Building's interface.

    Among Traits, multiple inheritance is allowed.
    """

    @abstractmethod
    def number_of_residents(self) -> int:
        pass


class ImplResidenceForApartmentBuilding(Residence, metaclass=Impl):
    def floor_area(self) -> float:
        return self._floor_area

    def number_of_residents(self) -> int:
        # One resident per 60 square meters
        return int(self._floor_area // 60)


class ApartmentBuilding(metaclass=Struct):
    _floor_area: float


if __name__ == "__main__":
    apartment_building = ApartmentBuilding(150.0)
    print(apartment_building.number_of_residents())
    print(apartment_building.traits)
