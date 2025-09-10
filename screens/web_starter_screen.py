from textual.widgets import Label, Button, Input
from textual.screen import Screen
from textual.app import ComposeResult, App
from pathlib import Path
from messages.deploy_success_message import DeploySuccess
from textual import events, on


class WebStarter(Screen):
    def compose(self) -> ComposeResult:
        yield Label("You're about to start the web kit in IoT")
        yield Button("Start web starter", id="web")
        yield Button("Go back", id="pop")