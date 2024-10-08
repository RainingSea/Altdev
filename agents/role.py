from pydantic import BaseModel
from abc import ABC, abstractmethod
from utils.commen import write_to_file,write_to_file_overwrite


class Role(BaseModel, ABC):
    name: str = ""
    profile: str = ""

    def say_your_name(self):
        print(self.name)

    def save_file(self, file_dir_name, content):
        # use method from project utils
        write_to_file(file_dir_name, content)
    
    def save_file_overwrite(self, file_dir_name, content):
        write_to_file_overwrite(file_dir_name, content)

    @abstractmethod
    def go():
        pass

    def align_recv():
        pass
