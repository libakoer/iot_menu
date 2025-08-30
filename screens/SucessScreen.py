from textual.widgets import Label, Button
from textual.screen import Screen
from textual.app import ComposeResult
class Success(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Success")
        yield Button("Go back", id="pop")