https://pypi.org/project/pytrait/0.0.1/

PyTrait
=======

Do you like Python, but think that multiple inheritance is a bit too flexible? Are you
looking for a more constrained way to define interfaces and re-use code?

Try using PyTraits!

We provide three metaclasses that aid writing code for shared behavior separately from
concrete types. For the most part, `Trait`s define interfaces, `Struct`s define state,
and `Impl`s define implementation. `Trait`s must be defined before any `Impl`s which
implement them, and `Impl`s must be defined before the `Struct`s that use them.

See examples under `examples/`.


Traits
------

Traits are abstract base classes (ABCs). There's really not much else to say, except
that these ABCs are always implemented in `Impl` classes, which themselves have no
abstract methods, but are not concrete classes; instead an `Impl` is associated with
another type that it bestows implementation upon. This would be either a concrete class
(always a `Struct`) or all such concrete classes implementing a given `Trait`.


    from pytrait import Trait, abstractmethod    

    class MyTrait(metaclass=Trait):
        @abstractmethod
        def my_method(self) -> str:
            pass


Structs
-------

Python has _dataclasses_, and they're great. We're using them internally for our
Structs, so whenever you see `metaclass=Struct`, the class is also a dataclass.
Don't get confused with the existing Python module `struct` -- that one is lower-case.


    from pytrait import Struct

    class MyStruct(metaclass=Struct):
        my_message: str = "this is a dataclass"

        def __post_init__(self):
            assert my_message == "this is a dataclass"


Impls
-----

`Impl`s bring together `Trait`s and `Struct`s. They represent the implementation details
that satisfy one particular interface.

Why isn't the implementation just all together under the `Struct`? Organization,
mostly. Also, "blanket" `Impl`s can provide implementation for any `Struct` implementing
a given `Trait`, so `Impl`s allow for greater code re-use.

`Impl`s have to indicate which `Struct`s they bestow implementation upon. You can
follow a strict naming convention, like `ImplMyTraitForMyStruct`. This is sufficient.
Or, you can use any name you want so long as you also provide a keyword argument
`target="StructName"` alongside the `metaclass` argument.


    from pytrait import Impl

    class MyImpl(MyTrait, metaclass=Impl, target="MyStruct"):
        ...


This is used to automate the list of implementations for `MyStruct`; you don't need to
explicitly list any superclasses of `MyStruct`, just based on the `Impl` name it will
inherit from all relevant `Impl`s.


FAQ
===


This reminds me of another programming language
-----------------------------------------------

That is not a question, but you have indeed figured me out. This way of organizing
Python code was heavily inspired by the Rust programming language. But beyond being an
imitation, it's a testament to how powerful Python is. My philosophy is that if
you're not using the flexibility of Python to limit yourself, you're not making use of
the full flexibility of Python.


What doesn't work?
------------------

A Struct can't have traits with overlapping method names. Rust can solve this
with its "fully qualified syntax", or by type constraints, but Python will
by default only resolve to the method from the first listed superclass (see
Python's "Method Resolution Order").

I don't think there's any easy way around this, because in Python there's no clear way
to choose which implementation to use based on type annotation. If you _really_ want to
let a `Struct` implement two traits that have the same method name, you can always wrap
your class definition in a try block and catch the `MultipleImplementationError`. Maybe
you can find a way to make it work.


TODO
====

  - Supertraits
  - better README
