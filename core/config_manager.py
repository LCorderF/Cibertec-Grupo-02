import os
import configparser

class ConfigManager:
    def __init__(self, archivo="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(archivo)

    @property
    def db_file(self):
        return os.path.join(
            self.config["DATABASE"]["DB_PATH"],
            self.config["DATABASE"]["DB_NAME"]
        )

    @property
    def db_path(self):
        return self.config["DATABASE"]["DB_PATH"]

    @property
    def pdf_url(self):
        return (
            self.config["DOWNLOAD"]["BASE_URL"] +
            self.config["DOWNLOAD"]["FILE_URL"]
        )

    @property
    def pdf_file(self):
        return os.path.join(
            self.config["DOWNLOAD"]["DOWNLOAD_PATH"],
            self.config["DOWNLOAD"]["DOWNLOAD_FILE"]
        )

    @property
    def download_path(self):
        return self.config["DOWNLOAD"]["DOWNLOAD_PATH"]

    @property
    def text_file(self):
        return self.config["FILES"]["TEXT_FILE"]

    @property
    def csv_file(self):
        return self.config["FILES"]["CSV_FILE"]
