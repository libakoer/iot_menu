
from textual.widgets import Button
from textual.screen import Screen
from textual.app import ComposeResult
from pathlib import Path
from messages.DeploySuccessMessage import DeploySuccess

class AdoptScreen(Screen):
    def __init__(self, start_path: str = None, **kwargs):
            super().__init__(**kwargs)
            self.current_path = Path(start_path or Path.cwd())
    def compose(self) -> ComposeResult:
        ##to do
        yield Button("No, go back", id="pop")