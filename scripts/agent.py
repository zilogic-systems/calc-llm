import os
import json
from phi.agent import Agent
from phi.tools import Toolkit
from phi.model.ollama import Ollama
from phi.tools.github import GithubTools
from parrot.ADBController import ADBController


class GitHubTool(Toolkit):

    def __init__(self):
        super().__init__()
        self.github_repo = GithubTools(access_token=os.getenv('GITHUB_ACCESS_TOKEN'))
        self.adc_controller = ADBController()
        self._register_tools()

    def _register_tools(self):
        self.register(self.adc_controller.adb_select_device)
        self.register(self.adc_controller.adb_home)
        self.register(self.adc_controller.adb_take_screenshot)
        self.register(self.adc_controller.adb_pull_xml_screen)
        self.register(self.adc_controller.adb_scroll_down)
        self.register(self.adc_controller.adb_shell)
        self.register(self.adc_controller.adb_open_an_application)
        self.register(self.adc_controller.adb_close_current_application)
        self.register(self.adc_controller.get_current_application_package_name)
        self.register(self.github_repo.list_pull_requests)
        self.register(self.github_repo.list_issues)
        self.register(self.github_repo.get_pull_request)
        self.register(self.github_repo.get_issue)
        self.register(self.github_repo.comment_on_issue)
        self.register(self.github_repo.edit_issue)


if __name__ == "__main__":
    agent = Agent(
        # model=Ollama(id="llama3.1"),
        model=Ollama(id="llama3.1:8b", host="172.236.140.158:11434"),
        instructions=[
            "Use your tools to answer questions about the repo: zilogic-systems/calc-llm",
            "Do not create any issues or pull requests unless explicitly asked to do so",
        ],
        tools=[GitHubTool()],
        show_tool_calls=True,
        num_history_responses=5,
        markdown=True,
    )

    while True:
        prompt = input(">>> ")
        if prompt.lower() in {"exit", "exit()", "quit"}:
            break
        if prompt.lower() in {"clear", "cls"}:
            print("\033c", end= " ")
            continue
        agent.print_response(prompt)

