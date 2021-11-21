from dataclasses import dataclass
import sys
from typing import Dict

import pytrait
from pytrait import Impl


class Struct(Impl):
    """
    Use metaclass=Struct when declaring a class, in order for the class to be a Struct
    in the trait system. The class will automatically find Impl blocks to inherit from.

    Struct is a metaclass, and must subclass the metaclass Impl because classes of type
    Struct subclass classes of type Impl.
    """

    disallow_non_function_attrs = False
    disallow_instantiation = False

    def __new__(meta, name, bases, attrs, **kwargs):
        """
        Passing keyword args after metaclass=Struct will provide options to dataclass.
        """
        # Automatically add Impls for this Struct to bases
        impl_bases = Impl.registry[name]
        trait_names_to_check_for_blanket_impls = [
            impl.trait_name for impl in impl_bases
        ]
        # Automatically add blanket Impls for this struct to bases.
        # This is "recursive", so if we get a trait satisfied from a blanket
        # implementation, that may afford even more blanket implementations.
        while trait_names_to_check_for_blanket_impls:
            trait_name = trait_names_to_check_for_blanket_impls.pop()
            additional_impls = Impl.blanket_registry.get(trait_name)
            if additional_impls is not None:
                impl_bases.extend(additional_impls)
                trait_names_to_check_for_blanket_impls.extend(
                    [impl.trait_name for impl in additional_impls]
                )
        bases = bases + tuple(impl_bases)
        cls = super().__new__(meta, name, bases, attrs)
        # If we're using Python 3.10 or newer, use the slots feature of dataclasses to
        # prevent the programmer from adding new attrs to a non-frozen dataclass.
        if sys.version_info >= (3, 10, 0):
            if "slots" not in kwargs:
                kwargs["slots"] = True
        # Make the cls be a dataclass
        return dataclass(cls, **kwargs)

    def __init__(cls, name, bases, attrs, **kwargs):
        if __debug__:
            # Mapping from methodname to the name of the trait that we got the
            # method from
            methodnames_seen: Dict[str, str] = dict()
            for base in bases:
                trait_name = base.__bases__[0].__name__
                if base.__class__ is not Impl:
                    raise pytrait.InheritanceError(
                        f"Struct {name} must only inherit from classes of type "
                        f"Impl, got class {base}"
                    )
                for attr, value in attrs.items():
                    if callable(value):
                        # Make sure no two traits clash with the same methods
                        if attr in methodnames_seen:
                            raise pytrait.MultipleImplementationError(
                                f"Method {attr}() defined twice, due to Traits "
                                f"{methodnames_seen[attr]} and "
                                f"{trait_name}"
                            )
                            methodnames_seen[attr] = trait_name
        super().__init__(name, bases, attrs)

    def implements(cls, trait: pytrait.Trait) -> bool:
        return issubclass(cls, trait)

    def traits(cls):
        for impl in cls.__bases__:
            trait = impl.__bases__[0]
            yield trait
