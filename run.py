from src import config_manager
from src.main import app
from src.config_manager import ConfigManager


if __name__ == "__main__":
    config_manager = ConfigManager()
    app.run(host=config_manager.host, port=int(config_manager.port), debug=True)
