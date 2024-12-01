from view import MastermindApp
from settings import Settings

if __name__ == "__main__":
    settings = Settings(language='en')
    app = MastermindApp(settings)
    app.run()