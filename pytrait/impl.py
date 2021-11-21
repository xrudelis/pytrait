from typing import Dict, List

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
    """

    registry: Dict[str, List["Impl"]] = dict()
    blanket_registry: Dict[str, List["Impl"]] = dict()

    def __init__(
        cls,
        name,
        bases,
        attrs,
        check_naming_convention: bool = True,
    ):
        if cls.__class__ is Impl:
            # We require an explicit base class here, unlike with Struct, because if the
            # substring "For" is in either a trait or target name, then our naming
            # convention would be ambiguous.
            if len(bases) != 1:
                basenames = tuple(base.__name__ for base in bases)
                raise pytrait.InheritanceError(
                    f"Impl {name} must list exactly 1 Trait as a base class, got: "
                    f"{basenames}"
                )
            base = bases[0]
            cls.trait_name = base.__name__
            prefix_len = len(f"Impl{cls.trait_name}For")
            cls.target_name = name[prefix_len:]

            # Look for target in Trait registry so that we know if this is a blanket
            # impl or not
            blanket_impl = cls.target_name in Trait.trait_registry

            if __debug__:
                if base.__class__ is not Trait:
                    raise pytrait.InheritanceError(
                        f"Impl {name} must inherit from a class of type "
                        f"Trait, got {base.__class__.__name__}"
                    )

                if check_naming_convention:
                    if not name.startswith(f"Impl{cls.trait_name}For"):
                        raise pytrait.NamingConventionError(
                            "We recommend naming all Impl classes like "
                            "ImplTraitForStruct."
                        )

                # Check that we implement all Trait abstract methods
                base_abstractmethods = set(base.__abstractmethods__)
                for attr, value in attrs.items():
                    if callable(value):
                        if hasattr(base, attr):
                            if attr in base_abstractmethods:
                                base_abstractmethods.remove(attr)

                if base_abstractmethods:
                    abstractmethods = ", ".join(
                        f"{name}()" for name in base_abstractmethods
                    )
                    raise pytrait.PytraitError(
                        f"Impl {name} must implement required methods: "
                        f"{abstractmethods}"
                    )

            # Add this class to the registry, so that it is automatically chosen as a
            # superclass for the relevant struct(s)

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

        super().__init__(name, bases, attrs)
