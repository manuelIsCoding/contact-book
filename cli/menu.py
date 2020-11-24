from typing import List, Any

class Menu:
    def __init__(self, options: List[str]) -> None:
        if not len(options):
            raise ValueError('Menu options list is empty.')

        self.options = options
    
    def display(self) -> None:
        for index, option in enumerate(self.options):
            print(f'[{index}]: {option}')

    def get_option(self, prompt: str) -> int:
        user_option = input(prompt)
        if not self._validate_option(user_option):
            return self.get_option(prompt)
        
        return self.options[int(user_option)]

    def _validate_option(self, option: str) -> Any:
        try:
            self.options[int(option)]
            return True
        except:
            print('Invalid option')
            return False
