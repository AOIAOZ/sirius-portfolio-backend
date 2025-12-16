class Prompt:
    def __init__(self, prompt: str = None):
        self._prompt = prompt

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, new_prompt):
        self._prompt = new_prompt
