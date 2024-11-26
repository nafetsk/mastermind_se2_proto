import json
import os

class Settings:
    def __init__(self, language='de'):
        self.language = language
        self.texts = {}
        self.load_settings()

    def set_language(self, language):
        self.language = language
        self.load_settings()

    def load_settings(self):
        file_path = os.path.join(os.path.dirname(__file__), f'text/{self.language}.json')
        with open(file_path, 'r') as file:
            self.texts = json.load(file)

    def get_text(self, key):
        return self.texts.get(key, key)