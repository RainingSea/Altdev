from pydantic import BaseModel

# message in project
class Message(BaseModel):
    sender: str = ""
    content: str = ""

    def set_content(self):
        return self.content

    def get_content(self):
        return self.content
