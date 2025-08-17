from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Header, Footer, Static
from textual.binding import Binding
from textual import events

class FileManager(App):
    """
    A Textual-based file manager with directory history navigation.
    - Arrow keys to move
    - Enter to expand directories; if already expanded, pressing Enter again navigates into it
    - Backspace to go up
    - "[" or "Left" to go back in history
    - "]" or "Right" to go forward in history
    """
    BINDINGS = [
        Binding("enter", "noop", "Expand or navigate directory", show=False),  # handled in on_key
        Binding("backspace", "up", "Go up", show=True),
        Binding("[", "history_back", "Back (history)", show=True),
        Binding("left", "history_back", "Back (history)", show=True),
        Binding("]", "history_forward", "Forward (history)", show=True),
        Binding("right", "history_forward", "Forward (history)", show=True),
    ]

    def __init__(self, start_path: str = None, **kwargs):
        super().__init__(**kwargs)
        initial = Path(start_path or Path.cwd())
        self.history = [initial]
        self.history_index = 0
        self.current_path = initial

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"Current Path: {self.current_path}", id="path_display")
        yield DirectoryTree(self.current_path, id="dir_tree")
        yield Footer()

    def on_mount(self) -> None:
        self.dir_tree = self.query_one("#dir_tree", DirectoryTree)
        self.path_display = self.query_one("#path_display", Static)
        self.set_focus(self.dir_tree)

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter" and self.focused is self.dir_tree:
            node = self.dir_tree.cursor_node
            entry = node.data
            path = Path(entry.path)
            if path.is_dir():
                if node.is_expanded:
                    # Already expanded: navigate into it
                    self._navigate_to(path)
                else:
                    # First press: expand the directory in-place
                    node.toggle()
                event.stop()
            else:
                self.log(f"Selected file: {path}")
                event.stop()

    def action_up(self) -> None:
        parent = self.current_path.parent
        if parent != self.current_path:
            self._navigate_to(parent)

    def action_history_back(self) -> None:
        if self.history_index > 0:
            self.history_index -= 1
            self._load_path(self.history[self.history_index])

    def action_history_forward(self) -> None:
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._load_path(self.history[self.history_index])

    def _navigate_to(self, new_path: Path) -> None:
        """Navigate to a new path and record it in history."""
        self.history = self.history[: self.history_index + 1]
        self.history.append(new_path)
        self.history_index += 1
        self._load_path(new_path)

    def _load_path(self, path: Path) -> None:
        """Load the given path without modifying history."""
        self.current_path = path
        self.path_display.update(f"Current Path: {self.current_path}")
        self.dir_tree.path = self.current_path
        self.dir_tree.reload()

if __name__ == "__main__":
    import sys
    start = sys.argv[1] if len(sys.argv) > 1 else None
    FileManager(start_path=start).run()
