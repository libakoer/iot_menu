from textual.widgets import Label, Button, Input
from textual.screen import Screen
from textual.app import ComposeResult
from pathlib import Path
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on


class OpenwrtSetup(Screen):
    def compose(self) -> ComposeResult:
        yield Label("!!!Make sure you are connected to your router via Ethernet or Wifi!!! " \
        "Make sure your router has internet connection^" \
        "This will create a file that pre configure your gateway credentials. Please" \
        "define the SSID and password for your external WiFi-router running OpenWRT. This" \
        "Wifi credentials will become your default settings." \
        "Do you want to continue editing your Gateway's WiFi configuration?")
        yield Input(placeholder="Please choose a SSID for your gateway:", id="ip_openwrt")
        yield Button("Submit", id="openwrt_submit")
        yield Button("Go back", id="pop")
    @on(Button.Pressed, "#openwrt_submit")
    def OpenWrtLogic(self)-> None:
        ssid=self.query_one("#ip_openwrt", Input).value

                    ##todo logic
        self.post_message(DeploySuccess())
        self.app.pop_screen()