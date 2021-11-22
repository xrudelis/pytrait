from abc import ABCMeta
from typing import Any, Dict, Generator, Tuple

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

    allowed_attrs = (
        "__doc__",
        "__module__",
        "__qualname__",
    )

    # Keep track of all available traits by name
    trait_registry: Dict[str, "Trait"] = dict()

    def __new__(meta, name: str, bases: Tuple[type], attrs: Dict[str, Any], **kwargs):
        cls = super().__new__(meta, name, bases, attrs)
        # Disallow instantiation by defining __init__()
        setattr(cls, "__init__", _disallowed_init)
        return cls

    def __init__(cls, name: str, bases: Tuple[type], attrs: Dict[str, Any]):
        if __debug__:
            cls.require_inherit_traits(name, bases)
            cls.require_method_attrs(name, attrs)
        Trait.trait_registry[name] = cls
        super(ABCMeta, cls).__init__(name, bases, attrs)

    def __repr__(cls):
        return f"{cls.__class__.__name__} {cls.__module__}.{cls.__qualname__}"

    def require_inherit_traits(cls, name: str, bases: Tuple[type]):
        """Require that we only inhert from Trait classes."""
        for base in bases:
            if base.__class__ is not Trait:
                raise pytrait.InheritanceError(
                    f"{name} must inherit from Traits only, "
                    f"got: {base.__name__} of type {base.__class__.__name__}"
                )

    def require_method_attrs(cls, name: str, attrs: Dict[str, Any]):
        """
        Require that the class has no non-method attributes.

        State should be defined in Structs only.
        """
        non_method_attrs = list()
        for attr, value in attrs.items():
            if attr not in cls.allowed_attrs and not callable(value):
                non_method_attrs.append(attr)
        if non_method_attrs:
            non_method_attrs = ", ".join(non_method_attrs)
            raise pytrait.NonMethodAttrError(
                f"{cls.__class__.__name__} {name} must not have non-method "
                f"attributes, got: {non_method_attrs}"
            )

    def supertraits(cls) -> Generator["Trait", None, None]:
        """Yields this class and any supertraits recursively."""
        yield cls
        for base in cls.__bases__:
            if base is object:
                return
            yield from base.supertraits()
