class FactoryParam():
    name: str
    type: str
    required: bool

    def __init__(self, name: str, type: str, required: bool):
        self.name = name
        self.type = type
        self.required = required