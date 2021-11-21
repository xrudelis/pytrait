class PytraitError(RuntimeError):
    pass


class DisallowedInitError(PytraitError):
    pass


class NonMethodAttrError(PytraitError):
    pass


class MultipleImplementationError(PytraitError):
    pass


class InheritanceError(PytraitError):
    pass


class NamingConventionError(PytraitError):
    pass
