class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age  

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        assert 0 <= value <= 250
        self._age = value
        