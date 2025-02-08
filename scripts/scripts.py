import time

from phi.tools import Toolkit
from phi.utils.log import logger
from phi.agent import Agent
from phi.model.ollama import Ollama

from parrot.ADBController import ADBController
# from parrot import OCRLib


def sleep(timeout: int):
    time.sleep(timeout)
    logger.info(f"Wait for {timeout} seconds")


def find_string_in_file(string: str, inputfile: str):
    with open(inputfile, 'r') as f:
        b = f.read()
    if string in b:
       logger.info(f"{string} is avialable in the {inputfile}")
       return "Available"
    logger.critical(f"{string} is not avialable in the {inputfile}")


class ADBInterface(Toolkit, ADBController):
    def __init__(self, name: str = "toolkit"):
        super().__init__()
        self.__register_tools()

    def __register_tools(self):
        self.register(self.adb_select_device)
        self.register(self.adb_home)
        self.register(self.adb_take_screenshot)
        self.register(self.adb_pull_xml_screen)
        self.register(self.adb_scroll_down)
        self.register(self.adb_shell)
        self.register(self.adb_open_an_application)
        self.register(self.adb_close_current_application)
        self.register(self.get_current_application_package_name)
        # self.register(OCRLib.image_to_text)
        # self.register(OCRLib.verify_image_contains_text)


if __name__ == "__main__":
    agent = Agent(
        model=Ollama(id="llama3.1:8b", host="172.236.140.158:11434"),
        tools=[ADBInterface(), find_string_in_file, sleep],
        # storage=SqlAgentStorage(table_name="agent_sessions", db_file="/tmp/agent_storage.db"),
        show_tool_calls=True,
        # add_history_to_messages=True,
        num_history_responses=5,
        markdown=True)

    while True:
        prompt = input(">> ")
        if prompt == "exit":
            break
        agent.print_response(prompt)
