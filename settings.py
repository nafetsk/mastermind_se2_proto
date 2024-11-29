import json
import os

class Settings:
    def __init__(self, language='de'):
        self.language = language
        self.MAX_ROUNDS = 10
        self.CODE_LENGTH = 5
        self.COLORS = [1, 2, 3, 4, 5, 6, 7, 8]
        self.texts = {}
        self.load_text()

    def set_language(self, language):
        self.language = language
        self.load_text()

    def load_text(self):
        file_path = os.path.join(os.path.dirname(__file__), f'text/{self.language}.json')
        with open(file_path, 'r') as file:
            self.texts = json.load(file)

    def get_text(self, key):
        return self.texts.get(key, key)