from textual.widgets import Label, Button, Header
from textual.screen import Screen
from textual.app import ComposeResult
from pathlib import Path
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on
from script_activation_logic.Deploy_script import deploy_script
from messages.DeployFailedMessage import DeployFailed
class DeployScreen(Screen):
        def __init__(self, current_path: str = None, **kwargs):
            super().__init__(**kwargs)
            self.current_path = Path(current_path or Path.cwd())
        def compose(self) -> ComposeResult:
            yield Header()
            yield Label("You are baout to deploy from the following path:")
            yield Label(f"{self.current_path}")
            yield Label("Are you sure?")
            yield Button("Yes, run deploy", id="deploy_logic")
            yield Button("No, go back", id="pop")
        @on(Button.Pressed, "#deploy_logic")
        def deploymentLogic(self)->None:
            answer=deploy_script(self.current_path)
            if answer[0]!="":
                self.post_message(DeploySuccess(answer[0]))
                self.app.pop_screen()
            else:
                 self.post_message(DeployFailed(answer[1],answer[2]))
