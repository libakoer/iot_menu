from textual.widgets import Label, Button, Header
from textual.screen import Screen
from textual.app import ComposeResult
from pathlib import Path
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on
class DeployScreen(Screen):
        def __init__(self, start_path: str = None, **kwargs):
            super().__init__(**kwargs)
            self.current_path = Path(start_path or Path.cwd())
        def compose(self) -> ComposeResult:
            yield Header()
            yield Label("You are baout to deploy from the following path:")
            yield Label(f"{self.current_path}")
            yield Label("Are you sure?")
            yield Button("Yes, run deploy", id="deploy_logic")
            yield Button("No, go back", id="pop")
        @on(Button.Pressed, "#deploy_logic")
        def deploymentLogic(self)->None:
            self.post_message(DeploySuccess())
            self.app.pop_screen()
