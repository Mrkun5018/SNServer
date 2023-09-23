class Singleton:
    attribute = '__instance'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, cls.attribute):
            setattr(cls, cls.attribute, object.__new__(cls))
            print(f" - {cls.__name__} start init ...")
        return getattr(cls, Singleton.attribute)

    @classmethod
    def getInstances(cls) -> 'cls':
        assert hasattr(cls, cls.attribute), f"{cls.__name__} is not init ..."
        return getattr(cls, cls.attribute)

