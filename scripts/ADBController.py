#
# Copyright 2024 Zilogic Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Author: code@zilogic.com
Requirements: subprocess
"""
import base64
import subprocess

class ADBError(Exception):
    """Represents an error in the ADB Controller."""

class ADBController:

    def __init__(self, adb_port=5037) -> None:
        self.device = None
        self.port = adb_port

    @staticmethod
    def _execute_command(cmd: list, output=False) -> dict:
        """Executes the commands in the terminal as a subprocess.

        - cmd : Commands to be executed.
        - output : True or False. Defaults to ``False``.

        Returns the status of the result if it passes. But if it fails, it returns an error.
        """
        if not output:
            output = subprocess.PIPE
        adb_output = subprocess.run(cmd, stdout=output,
                                    stderr=subprocess.PIPE, text=True, check=False)
        adb_stdout = f"{adb_output.stdout}\n{adb_output.stderr}"
        status = adb_output.returncode == 0

        result = {"success": status,
                  "stdout" : adb_stdout}
        return result

    def _device_connection(self, device: str, connect=True) -> bool:
        """Connects or Disconnects the ADB Device.

        - device : IP Address of the ADB device.
        - connect : True or False. Defaults to ``True``.

        Raises ADB Error when the device connection or disconnection get failed.

        """
        state = "connect" if connect else "disconnect"
        cmd = ["adb", state, device]
        adb_out = self._execute_command(cmd=cmd)
        for error_msg in ['error', 'No route', 'timed out', 'Connection refused']:
            if error_msg in adb_out['stdout']:
                logger.console(adb_out)
                raise ADBError(f"Failed to {state} ADB: {device}: {error_msg}")
        return True

    def _run_server(self, start=True) -> bool:
        """Starts or stops the server.

        - start : True or False. Defaults to ``True``.

        Raises ADBError when the start or stop the server gets failed;
        but it passes when it is executed.

        """
        status = "start-server" if start else "kill-server"
        start_cmd = ["adb", status, "-p", f'{self.port}']
        adb_out = self._execute_command(start_cmd)
        if adb_out['success']:
            return True
        raise ADBError(f"Failed to adb {status}")

    @staticmethod
    def _log_message(msg: str) -> bool:
        """Displays the log message in the HTML file.

        ``msg`` is the message to be printed.

        """
        print(msg)

    def adb_shell(self, cmd: list) -> str:
        """Executes the command in the ADB Shell.

        Returns the output of the ADB command.

        *Example*

        | ADB Shell | ['input', 'keyevent', '85'] |
        | ADB Shell | ['input', 'keyevent', '126'] |
        """
        adb_cmd = ["adb", "-s", self.device, "shell", *cmd]
        print(adb_cmd)
        adb_out = self._execute_command(adb_cmd)
        if adb_out['success']:
            return adb_out['stdout']
        raise ADBError(f"Failed to execute \n{' '.join(cmd)} in {self.device}")

    def adb_disconnect_all(self) -> None:
        """Disconnects all the remote Android devices.

        Disconnects all remote Android devices previously connected using the
        "ADB IP Connect" keyword.
        """
        cmd = ["adb", "disconnect"]
        self._execute_command(cmd)
        message = "ADB Disconnect All"
        self._log_message(message)
        return

    def adb_start_server(self) -> None:
        """Starts the ADB Server.

        The ADB server runs as a background process on the PC / development
        machine. The ADB server communicates with the daemon running in the
        Android device. The commands are issued to the deamon running in the
        Android device through the ADB server.
        """
        self._run_server(start=True)
        message = "ADB Start server"
        self._log_message(message)
        return

    def adb_select_device(self, device_name: str) -> None:
        """Use this to selects the particular Android Device.

        One of Android devices has to be selected to receive
        subsequent actions. The device is specified using the
        ``device_name`` argument.
        """
        self.device = device_name
        return

    def adb_lock_screen(self) -> None:
        """Locks the Android Device screen.

        Remotely locks the Android device's screen, even if it is not currently
        locked. It simulates the action of locking the screen by hitting the
        device's power button.
        """
        cmd = ['input', 'keyevent', '223']
        self.adb_shell(cmd)
        return

    def adb_wake_screen(self) -> None:
        """Wakes the screen of the connected Android Device.

        If the display is turned off, this keyword will wakeup the device and
        turn on the display. If the Android device is already awake, this
        keyword will have no effect.

        This will generally be the first keyword in a UI based test case.
        """
        cmd = ['input', 'keyevent', '224']
        self.adb_shell(cmd)
        return

    def adb_take_screenshot(self, outputfile: str) -> None:
        """Takes the screenshot of the current screen.

        This keyword captures and stores the current screen in the path
        specified by ``outputfile``. The path specifies a file in the PC.

        *Example*

        | ADB Take Screenshot | screen_capture.png |
        | ADB Take Screenshot | capture_page.png  |

        """
        cmd = ['adb', '-s', self.device, 'exec-out', 'screencap', '-p']
        with open(outputfile, "wb") as img:
            self._execute_command(cmd, output=img) # type: ignore # py
        with open(outputfile, 'rb') as outputimage:
            b64_fbuffer = base64.b64encode(outputimage.read())
        outputfile = f'<img controls src="data:img/png;base64,{b64_fbuffer.decode()}" width = "200"></img>'
        logger.write(outputfile, html=True)
        return

    def adb_close_current_application(self) -> None:
        """Closes the current application.

        Identifies the application running the foreground, and stops the
        application. The application running in the foreground is identified
        using `dumpsys activity` command. And application is terminated using
        the `am force-stop` command.

        Closing the application can be achieved by using `ADB Home` keyword,
        but this might not close the app completely depending on its
        implementation.
        """
        cmd = ['dumpsys', 'activity', '|', 'grep', 'top-activity']
        result = self.adb_shell(cmd)
        package_name = result.split("/")[-2].split(":")[-1]
        cmd = ['am', 'force-stop', f'{package_name}']
        self.adb_shell(cmd)
        return

    def adb_open_an_application(self, package_name: str) -> None:
        """Use this to open the specified Application in the Android Device.

        The application specified by `package_name` is opened.

        NOTE: No applications need to be closed before the execution of the
        ``ADB Open an Application``
        """
        cmd = ['monkey', '-p', package_name, '-v', '20']
        self.adb_shell(cmd)
        return

    def adb_enter_key(self) -> None:
        """Sends an Enter key.

        Sends an Enter key to the Android device by emulating a key event.
        """
        cmd = ["input", "keyevent", "66"]
        self.adb_shell(cmd)
        return

    def get_current_application_package_name(self) -> str:
        """Gets the package name of current application.

        Gets only the top application package name, even if
        numerous applications are running in the background.

        """
        cmd = ['dumpsys', 'activity', '|', 'grep', 'top-activity']
        result = self.adb_shell(cmd)
        package_name = result.split("/")[-2].split(":")[-1]
        return package_name

    def adb_scroll_down(self) -> None:
        """Scrolls the screen downward.

        Swiping down is not advised in every situation unless if you absolutely
        need to scroll down the screen in Android device. If there is no screen
        at all, it won't raise errors.
        """
        cmd = ["input", "swipe", "500", "1000", "300", "300"]
        self.adb_shell(cmd)
        return

    def adb_scroll_up(self) -> None:
        """Scrolls the screen upward.

        Swiping up is not advised in every situation unless
        if you absolutely need to scroll up the screen in android device.
        If there is no screen at all, it won't raise errors.
        """
        cmd = ["input", "swipe", "300", "700", "500", "1500"]
        self.adb_shell(cmd)
        return

    def adb_copy_to_pc(self, android_path: str, pc_path: str) -> None:
        """Copies the file from the Android Device to PC.

        Copies the file from the Android device, specifed by ``android_path`` to
        the path in the PC, specified by ``pc_path``.

        *Example*

        | ADB Copy To PC | /storage/emualated/0/Video/Movie.mp4 | /home/user/Videos/ |
        | ADB Copy To PC | /storage/emualated/0/Music/melody.mp3 | /home/user/song/ |

        """
        cmd = ["adb", "-s", self.device, "pull", android_path, pc_path]
        self._execute_command(cmd)
        return


    def adb_pull_xml_screen(self, output_file) -> None:
        """Generates an XML file containing the UI hierarchy of current Android screen.

        This is required to dump the UI hierarchy of current Android screen. It
        generates an XML file with a dump of the current UI hierarchy. It will
        store the Screen in the path which is specified to ``output_file``.

        *Example*

        | ADB Pull XML Screen | /home/user/Downloads/ |
        | ADB Pull XML Screen | /home/user/Documents/ |

        """
        cmd = ["uiautomator", "dump", "/sdcard/view.xml"]
        self.adb_shell(cmd)
        self.adb_copy_to_pc("/sdcard/view.xml", output_file)
        return

    def adb_home(self) -> None:
        """Gets back to Home Screen in the Android Device.

        Use keyevent to transmit a virtual key press that simulates
        pressing the real Home button.
        """
        cmd = ["input", "keyevent", "3"]
        self.adb_shell(cmd)
        return

    def adb_swipe_right_to_left(self) -> None:
        """Swipes the Android screen from right to left.

        Swiping right to left is not advised in every situation unless
        if you absolutely need to swipe the screen in android device.
        If there is no screen at all, it won't raise errors.
        """
        cmd = ["input", "swipe", "1000", "500", "300", "300"]
        self.adb_shell(cmd)
        return

    def adb_swipe_left_to_right(self) -> None:
        """Swipes the Android screen from left to right.

        Swiping left to right is not advised in every situation unless
        if you absolutely need to swipe the screen in android device.
        If there is no screen at all, it won't raise errors.
        """
        cmd = ["input", "swipe", "700", "300", "1500", "500"]
        self.adb_shell(cmd)
        return

    def adb_tap(self, coord):
        cmd = ["input", "tap", str(coord[0]), str(coord[1])]
        self.adb_shell(cmd)
