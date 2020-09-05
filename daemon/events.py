class event:
    _registry = {}

    def __init__(self, label: str):
        self.label = label

    def __call__(self, func: callable):
        self.__class__._registry[self.label] = func
        return func

    @classmethod
    def dispatch(cls, label: str):
        callback = cls._registry.get(label)
        # exact match
        if callback:
            return callback()

        # prefixed match?
        for _label, callback in cls._registry.items():
            if not label.startswith(_label):
                continue

            args = label[len(_label) :].split(":")
            return callback(*args)

        return None
