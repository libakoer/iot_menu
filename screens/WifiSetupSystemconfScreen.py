from textual.widgets import Button, Input
from textual.screen import Screen
from textual.app import ComposeResult
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on

class WifiSetupSystemconf(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Please choose a SSID for your gateway:", id="SSID")
        yield Input(placeholder="Please create a new password:", id="pass")
        yield Input(placeholder="Please confirm your new password:", id="new_pass")
        yield Input(placeholder="The MQTT host IP:", id="ip")
        yield Button("Submit", id="wifi_systemconf_submit")
        yield Button("Go back", id="pop")
    @on(Button.Pressed, "#wifi_systemconf_submit")
    def WifiSystemconfLogic(self)-> None:
        ssid=self.query_one("#SSID", Input).value
        password=self.query_one("#pass", Input).value
        retry=self.query_one("#new_pass", Input).value
        ip=self.query_one("#ip", Input).value
        ##todo logic
        self.post_message(DeploySuccess())
        self.app.pop_screen()
