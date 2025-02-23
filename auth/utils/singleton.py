class ParametrizedSingletonMeta(type):
    """A metaclass for implementing the Singleton pattern."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ParametrizedSingleton(metaclass=ParametrizedSingletonMeta):
    """Base class for Singleton objects."""

    pass


class SingletonMeta(ParametrizedSingletonMeta):
    """A metaclass for implementing the Singleton pattern."""

    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            instance = super().__call__()
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """Base class for Singleton objects."""

    pass
