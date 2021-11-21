from abc import ABCMeta
from typing import Dict

import pytrait


def _disallowed_init(self, *args, **kwargs):
    # Raises an error like "Trait MyTrait cannot be instantiated" or
    # "Impl ImplMyTraitForMyStruct cannot be instantiated"
    raise pytrait.DisallowedInitError(
        f"{self.__class__.__class__.__name__} {self.__class__.__name__} cannot "
        f"be instantiated."
    )


class Trait(ABCMeta):
    """
    Use metaclass=Trait when declaring a class, in order for the class to define a
    Trait. Traits should have no explicit base class.

    Traits are very similar to abstract classes and interfaces. Like interfaces, the
    main goal is to define the available behavior for other types. Like abstract
    classes, traits can have some implementation defined for methods. But unlike
    abstract classes, Traits never inherit, and methods are either strictly abstract
    without implementation, or are concrete methods that cannot be overridden.
    """

    disallow_non_function_attrs = True
    disallow_instantiation = True
    allowed_attrs = (
        "__doc__",
        "__module__",
        "__qualname__"
    )

    # Keep track of all available traits by name
    trait_registry: Dict[str, "Trait"] = dict()

    def __new__(meta, name, bases, attrs, **kwargs):
        cls = super().__new__(meta, name, bases, attrs)
        if meta is Trait:
            Trait.trait_registry[name] = cls
        # Disallow instantiation by defining __init__()
        if meta.disallow_instantiation:
            setattr(cls, "__init__", _disallowed_init)
        return cls

    def __init__(cls, name, bases, attrs):
        if __debug__:
            if cls.__class__ is Trait:
                if len(bases) > 0:
                    basenames = ", ".join(base.__name__ for base in bases)
                    raise pytrait.InheritanceError(
                        f"Traits must not inherit from any provided classes, "
                        f"got: {basenames}"
                    )
            # Check that Trait, Impl classes have no non-method attributes.
            # State should be defined in Structs.
            non_method_attrs = list()
            for attr, value in attrs.items():
                if attr in cls.allowed_attrs:
                    continue
                if cls.disallow_non_function_attrs and not callable(value):
                    non_method_attrs.append(attr)
            if non_method_attrs:
                non_method_attrs = ", ".join(non_method_attrs)
                raise pytrait.NonMethodAttrError(
                    f"{cls.__class__.__name__} {name} must not have non-method "
                    f"attributes, got: {non_method_attrs}"
                )

        super().__init__(name, bases, attrs)
