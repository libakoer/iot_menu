from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Header, Footer, Static, Button, Label, Input
from textual.binding import Binding
from textual import events, on
from textual.containers import Container, VerticalScroll, Horizontal
from textual.message import Message
from textual.screen import Screen


from screens.SucessScreen import  Success
from screens.DeployScreen import DeployScreen
from screens.NewFolderScreen import NewFolder
from screens.AdoptScreen import AdoptScreen
from screens.WifiSetupSystemconfScreen import WifiSetupSystemconf
from screens.OpenwrtSetupScreen import OpenwrtSetup



from menus.BasicMenu import BasicMenu
from menus.AdvancedMenu import AdvancedMenu
from menus.WifiMenu import WifiMenu


from messages.DeploySuccessMessage import DeploySuccess


class IotMenu(App[None]):
    SCREENS= {
        "deploy": DeployScreen,
        "adopt": AdoptScreen,
        "folder": NewFolder,
        "wifi_conf": WifiSetupSystemconf,
        "openwrt": OpenwrtSetup

    }
    CSS_PATH = "tcss/iot_menu.tcss"
    """
    A Textual-based file manager without directory history.
    - Arrow keys to move
    - Enter to expand directories; if already expanded, pressing Enter again navigates into it
    - Backspace to go up
    """
    BINDINGS = [
        Binding("enter", "noop", "Expand or navigate directory", show=False),  # handled in on_key
        Binding("backspace", "up", "Go up", show=True),
    ]

    def __init__(self, start_path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.current_path = Path(start_path or Path.cwd())

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Container(id="left_panel"):
                yield Static(f"Current Path: {self.current_path}", id="path_display")
                yield DirectoryTree(self.current_path, id="dir_tree")
            yield Container(BasicMenu(), id="right_panel")       
        yield Footer()

    @on(DeploySuccess)
    def sucess_page(self)-> None:
        self.push_screen(Success())



    @on(Button.Pressed, "#deploy,#adopt,#folder,#wifi_conf, #openwrt")
    def action_deployment_screen(self, event: Button.Pressed)-> None:
        self.push_screen(event.button.id)



    @on(Button.Pressed, "#advanced")
    def action_remove_Basic_menu_and_add_Advanced(self)-> None:
        new_Advanced_menu=AdvancedMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Advanced_menu)


    @on(Button.Pressed, "#back")
    def action_remove_menu_and_add_Basic(self)-> None:
        new_Basic_menu=BasicMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Basic_menu)

    @on(Button.Pressed, "#wifi")
    def action_remove_Basic_menu_and_add_wifi(self)-> None:
        new_Wifi_menu=WifiMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Wifi_menu)


    @on(Button.Pressed, "#pop")
    def pop_screen_new(self)->None:
        self.pop_screen()


    @on(Button.Pressed, "#exit")
    def exit_the_app(self)->None:
        self.exit()

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
                    self._load_path(path)
                event.stop()
            else:
                self.log(f"Selected file: {path}")
                event.stop()

    def action_up(self) -> None:
        parent = self.current_path.parent
        if parent != self.current_path:
            self._load_path(parent)

    def _load_path(self, path: Path) -> None:
        """Load the given path."""
        self.current_path = path
        self.path_display.update(f"Current Path: {self.current_path}")
        self.dir_tree.path = self.current_path
        self.dir_tree.reload()

if __name__ == "__main__":
    import sys
    start = sys.argv[1] if len(sys.argv) > 1 else None
    IotMenu(start_path=start).run()

