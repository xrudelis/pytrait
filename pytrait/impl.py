from abc import ABCMeta
from typing import Any, Dict, Generator, List, Optional, Tuple

import pytrait
from pytrait import Trait


class Impl(Trait):
    """
    Use metaclass=Impl when declaring a class, in order for the class to be an Impl
    in the trait system. Each Impl has one base class, which must be a Trait. Impls
    implement that Trait for either a specific Struct, or for all structs implementing
    a Trait.

    Impl is a metaclass, and must subclass the metaclass Trait because classes of type
    Impl subclass classes of type Trait.

    If `target` is provided (the name of the Struct or Trait this Impl provides
    implementation for), then we relax the requirement for the Impl class to be
    named ImplMyTraitForTarget.
    """

    registry: Dict[str, List["Impl"]] = dict()
    blanket_registry: Dict[str, List["Impl"]] = dict()

    def __init__(
        cls,
        name: str,
        bases: Tuple[type],
        attrs: Dict[str, Any],
        target: Optional[str] = None,
    ):
        # We require an explicit base class here, unlike with Struct, because if the
        # substring "For" is in either a trait or target name, then our naming
        # convention would be ambiguous. Alternatively, the argument "target" can be
        # provided, with the name of the target Struct or Trait.
        if len(bases) != 1:
            basenames = tuple(base.__name__ for base in bases)
            raise pytrait.InheritanceError(
                f"Impl {name} must list exactly 1 Trait as a base class, got: "
                f"{basenames}"
            )

        base = bases[0]
        cls.trait_name = base.__name__
        if target is None:
            prefix_len = len(f"Impl{cls.trait_name}For")
            cls.target_name = name[prefix_len:]
        else:
            cls.target_name = target

        if __debug__:
            cls.require_inherit_traits(name, bases)
            cls.require_method_attrs(name, attrs)
            cls.require_no_abstract_methods(name, base, attrs)
            if target is None:
                cls.require_naming_convention(name, cls.trait_name, cls.target_name)

        # Add this class to the registry, so that it is automatically chosen as a
        # superclass for the relevant struct(s)

        # Look for target in Trait registry so that we know if this is a blanket
        # impl or not
        blanket_impl = cls.target_name in Trait.trait_registry
        if blanket_impl:
            if cls.target_name in Impl.blanket_registry:
                Impl.blanket_registry[cls.target_name].append(cls)
            else:
                Impl.blanket_registry[cls.target_name] = [cls]
        else:
            if cls.target_name in Impl.registry:
                Impl.registry[cls.target_name].append(cls)
            else:
                Impl.registry[cls.target_name] = [cls]

        super(ABCMeta, cls).__init__(name, bases, attrs)

    def require_naming_convention(cls, name: str, trait_name: str, target_name: str):
        if name != f"Impl{trait_name}For{target_name}":
            raise pytrait.NamingConventionError(
                "We require either naming all Impl classes like "
                "ImplTraitForStruct, or providing the target argument."
            )

    def require_no_abstract_methods(cls, name: str, base: Trait, attrs: Dict[str, Any]):
        # Check that we implement all Trait abstract methods
        base_abstractmethods = set(base.__abstractmethods__)
        for attr, value in attrs.items():
            if callable(value) and hasattr(base, attr):
                if attr in base_abstractmethods:
                    base_abstractmethods.remove(attr)

        if base_abstractmethods:
            abstractmethods = ", ".join(f"{name}()" for name in base_abstractmethods)
            raise pytrait.PytraitError(
                f"Impl {name} must implement required methods: " f"{abstractmethods}"
            )

    def traits(cls) -> Generator[Trait, None, None]:
        """
        Yields traits that this Impl implements.

        This can be multiple because Traits are allowed to inherit from any number of
        other Traits.
        """
        for base in cls.__bases__:
            yield from base.supertraits()
