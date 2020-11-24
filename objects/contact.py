class Contact:
    def __init__(self, name: str, phone_num: str) -> None:
        self.name = name
        self.phone_num = phone_num
    
    def __repr__(self) -> str:
        return (f'{self.get_clsname()}({self.name!r}, '
                f'{self.phone_num!r})')
    
    @classmethod
    def get_clsname(cls):
        return cls.__name__
