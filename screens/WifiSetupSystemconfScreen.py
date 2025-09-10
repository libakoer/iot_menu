from textual.widgets import Button, Input
from textual.screen import Screen
from textual.app import ComposeResult
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on
from script_activation_logic.Wifi_setup_systemconf_script import deploy_script
from pathlib import Path
from screens.LoadingScreen import LoadingScreen
from messages.DeployFailedMessage import DeployFailed
from messages.DeploySuccessMessage import DeploySuccess
import threading


class WifiSetupSystemconf(Screen):
    def __init__(self, current_path: str = None, **kwargs):
            super().__init__(**kwargs)
            self.current_path = Path(current_path or Path.cwd())
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Please choose a SSID for your gateway:", id="SSID")
        yield Input(placeholder="Please create a new password:", id="pass")
        yield Input(placeholder="Please confirm your new password:", id="new_pass")
        yield Input(placeholder="The MQTT host IP:", id="ip")
        yield Input(placeholder="The default Accesspoint host IP for external router is", id="gateway", value="192.168.14.1")

        yield Button("Submit", id="wifi_systemconf_submit")
        yield Button("Go back", id="pop")
    @on(Button.Pressed, "#wifi_systemconf_submit")
    def WifiSystemconfLogic(self)-> None:
        ssid=self.query_one("#SSID", Input).value
        password=self.query_one("#pass", Input).value
        retry=self.query_one("#new_pass", Input).value
        ip=self.query_one("#ip", Input).value
        gateway=self.query_one("#gateway", Input).value
        self.app.push_screen(LoadingScreen())
        def task():
            answer =deploy_script(self.current_path,ssid,password,retry,ip,gateway)
            if answer[1] !="":
                    self.post_message(DeployFailed(answer[1], answer[2]))
            else:
                self.post_message(DeploySuccess(answer[0]))

        threading.Thread(target=task, daemon=True).start()