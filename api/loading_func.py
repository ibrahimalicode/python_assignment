from PyQt5.QtCore import Qt, QThread, pyqtSignal
from api.openai_client import get_gpt_response

class GPTResponseThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        response = get_gpt_response(self.prompt)
        self.response_received.emit(response)