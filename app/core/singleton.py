def singleton(cls: type):
    _instances = {}

    def instance():
        if cls not in _instances:
            _instances[cls] = cls()
        return _instances[cls]

    return instance
