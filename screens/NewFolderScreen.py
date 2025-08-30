from textual.widgets import  Button, Input
from textual.screen import Screen
from textual.app import ComposeResult
from pathlib import Path
from messages.DeploySuccessMessage import DeploySuccess
from textual import events, on


class NewFolder(Screen):
    def __init__(self, start_path: str = None, **kwargs):
            super().__init__(**kwargs)
            self.current_path = Path(start_path or Path.cwd())
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Input the new Node name:")
        yield Button("Submit", id="submit_folder_name")
        yield Button("No, go back", id="pop")
    @on(Button.Pressed, "#submit_folder_name")
    def folderCreating(self)-> None:
        ##todo: create folder logic
        self.post_message(DeploySuccess())
        self.app.pop_screen()