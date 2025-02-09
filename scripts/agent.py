import os
import json
import xml.etree.ElementTree as ET
import re
import time
from phi.agent import Agent
from phi.tools import Toolkit
from phi.model.ollama import Ollama
from phi.model.openai import OpenAIChat
from phi.tools.github import GithubTools
from ADBController import ADBController

class CalculatorTool(Toolkit):

    def __init__(self):
        super().__init__(name="Calculator_Tool")
        self._adb_controller = ADBController()
        self._register_tools()

    def open_calculator(self):
        """Use this to open the calculator application to be tested."""
        device = os.getenv("ANDROID_DEVICE")
        if device is None:
            raise ValueError("ANDROID_DEVICE is not specified")
        self._adb_controller.adb_select_device(os.getenv("ANDROID_DEVICE"))
        self._adb_controller.adb_open_an_application("com.zilogic.z_calc")
        self._adb_controller.adb_pull_xml_screen("/tmp/out.xml")
        return "Opened Calculator"

    def click_button(self, name: str):
        """Use this to click on a button in the calculator. Specify the button
        name as argument `name`

        Examples

        To click on the button "1"

        click_button("1")

        To click on the button "+"

        click_button("+")
        """
        coord = self._get_ui_coordinates("/tmp/out.xml", text=name)
        if coord is None:
            raise ValueError("button not found")
        self._adb_controller.adb_tap(coord)
        return f"Clicked {name}"

    def read_display(self):
        """Use this to read the display of the calculator."""
        self._adb_controller.adb_pull_xml_screen("/tmp/out.xml")
        text = self._get_ui_text("/tmp/out.xml", "com.zilogic.z_calc:id/calculator_display")
        if text is None:
            text = ""
        return text

    def check_closed(self) -> str:
        """Use this to check if the calculator has closed or crashsed."""

        name = self._adb_controller.get_current_application_package_name()
        if name != "com.zilogic.z_calc":
            return "Calculator is Closed"
        else:
            return "Calculator is Open"

    def _register_tools(self):
        self.register(self.open_calculator)
        self.register(self.click_button)
        self.register(self.read_display)
        self.register(self.check_closed)

    def _get_ui_text(self, xml_dump, resource_id=None):
        """
        Extracts the text of a UI element from a uiautomator XML dump.

        :param xml_dump: Path to the XML dump file.
        :param resource_id: The resource-id of the UI component (optional).
        :return: (x, y) coordinates of the UI component's center or None if not found.
        """
        tree = ET.parse(xml_dump)
        root = tree.getroot()

        for node in root.iter("node"):
            if (resource_id and node.get("resource-id") == resource_id):
                text = node.get("text")
                return text
        return None

    def _get_ui_coordinates(self, xml_dump, resource_id=None, text=None):
        """
        Extracts the (x, y) center coordinates of a UI element from a uiautomator XML dump.

        :param xml_dump: Path to the XML dump file.
        :param resource_id: The resource-id of the UI component (optional).
        :param text: The text of the UI component (optional).
        :return: (x, y) coordinates of the UI component's center or None if not found.
        """
        tree = ET.parse(xml_dump)
        root = tree.getroot()

        for node in root.iter("node"):
            if (resource_id and node.get("resource-id") == resource_id) or (text and node.get("text") == text):
                bounds = node.get("bounds")
                if bounds:
                    match = re.findall(r"\d+", bounds)
                    if match and len(match) == 4:
                        x1, y1, x2, y2 = map(int, match)
                        return ((x1 + x2) // 2, (y1 + y2) // 2)  # Return center coordinates
        return None

class GitHubTool(Toolkit):

    def __init__(self):
        super().__init__(name="GitHub_Tool")
        self.github_repo = GithubTools(access_token=os.getenv('GITHUB_ACCESS_TOKEN'))
        self._register_tools()

    def _register_tools(self):
        self.register(self.github_repo.list_issues)
        self.register(self.github_repo.get_issue)
        self.register(self.github_repo.comment_on_issue)
        self.register(self.github_repo.edit_issue)


if __name__ == "__main__":
    model = OpenAIChat(id="gpt-4o")

    tester = Agent(
        name="Tester",
        model=model,
        role="Executes tests on the calculator app.",
        instructions=[
            "Use GitHub_Tool to answer questions about the GitHub repo: zilogic-systems/calc-llm",
            "Use Calculator_Tool to access and control UI of the Calculator",
            "To perform 1 + 2 in the calculator, "
            "open the calculator, "
            "click 'C' to clear the calculator, "
            "click 1, "
            "click +, "
            "click 2, "
            "click '=' ",
            "To perform 100 + 200 in the calculator, "
            "open the calculator, "
            "'C' to clear the calculator, "
            "click 1, click 0, click 0, "
            "click +, "
            "click 2, click 0, click 0, "
            "click '=' ",
            "To perform 1 / 2 in the calculator, "
            "open the calculator, "
            "click 'C' to clear the calculator, "
            "click 1, "
            "click ÷, "
            "click 2, "
            "click '=' "
        ],
        tools=[GitHubTool(), CalculatorTool()],
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
        tester.print_response(prompt)

