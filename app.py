from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Header, Footer, Static, Button
from textual.binding import Binding
from textual import events, on
from textual.containers import Container, Horizontal

from screens.sucess_screen import Success
from screens.deploy_screen import DeployScreen
from screens.new_folder_screen import NewFolder
from screens.adopt_screen import AdoptScreen
from screens.wifi_setup_system_conf_screen import WifiSetupSystemconf
from screens.open_wrt_setup_screen import OpenwrtSetup
from screens.failed_screen import Failed
from screens.open_wrt_router_screen import OpenWrtRouterIp
from screens.pre_flash_wemos_d1_mini import WemosPre
from screens.initialize_serial import InitializeSerial

from menus.basic_menu import BasicMenu
from menus.advanced_menu import AdvancedMenu
from menus.wifi_menu import WifiMenu
from messages.refresh_screen import Refresh

from messages.deploy_success_message import DeploySuccess
from messages.deploy_failed_message import DeployFailed

from script_activation_logic.find_router_ip_logic import router_ip

class IotMenu(App[None]):
    """
    A Textual-based file manager without directory history.
    - Arrow keys to move
    - Enter to expand directories; if already expanded, pressing Enter again navigates into it
    - Backspace to go up
    """
    CSS_PATH = "tcss/iot_menu.tcss"

    BINDINGS = [
        Binding("enter", "noop", "Expand or navigate directory", show=False),  # handled in on_key
        Binding("backspace", "up", "Go up", show=True),
    ]

    def __init__(self, start_path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.current_path = Path(start_path or Path.cwd())

        # SCREENS nüüd funktsioonid, et saaks path kaasa anda
        self.SCREENS = {
            "deploy": lambda: DeployScreen(self.current_path),
            "adopt": lambda: AdoptScreen(self.current_path),
            "folder": lambda: NewFolder(self.current_path),
            "wifi_conf": lambda: WifiSetupSystemconf(False,self.current_path),
            "openwrt": lambda: OpenwrtSetup(self.current_path),
            "wemos": lambda: WemosPre(self.current_path),
            "initialize": lambda: InitializeSerial(self.current_path),
        }

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Container(id="left_panel"):
                yield Static(f"Current Path: {self.current_path}", id="path_display")
                yield DirectoryTree(self.current_path, id="dir_tree")
            yield Container(BasicMenu(), id="right_panel")
        yield Footer()

    @on(DeploySuccess)
    def sucess_page(self, message: DeploySuccess) -> None:
        self.pop_screen()
        self.pop_screen()
        self.push_screen(Success(message.message))
    @on(Refresh)
    def refresh_screen(self)->None:
        self._load_path(self.current_path)

    @on(DeployFailed)
    def failed_page(self, error: DeployFailed) -> None:
        self.pop_screen()
        self.push_screen(Failed(error.error, error.code))

    @on(Button.Pressed, "#deploy,#adopt,#folder,#wifi_conf,#openwrt,#wemos,#initialize")
    def action_deployment_screen(self, event: Button.Pressed) -> None:
        screen_factory = self.SCREENS.get(event.button.id)
        if screen_factory:
            self.push_screen(screen_factory())

    @on(Button.Pressed, "#advanced")
    def action_remove_Basic_menu_and_add_Advanced(self) -> None:
        new_Advanced_menu = AdvancedMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Advanced_menu)

    @on(Button.Pressed, "#back")
    def action_remove_menu_and_add_Basic(self) -> None:
        new_Basic_menu = BasicMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Basic_menu)

    @on(Button.Pressed, "#wifi")
    def action_remove_Basic_menu_and_add_wifi(self) -> None:
        new_Wifi_menu = WifiMenu()
        self.query_one("#right_panel").remove_children()
        self.query_one("#right_panel").mount(new_Wifi_menu)

    @on(Button.Pressed, "#pop")
    def pop_screen_new(self) -> None:
        self.pop_screen()
    
    @on(Button.Pressed, "#pop2")
    def pop_screen_new_2(self) -> None:
        self.pop_screen()
        self.pop_screen()

    @on(Button.Pressed, "#exit")
    def exit_the_app(self) -> None:
        self.exit()
        
    @on(Button.Pressed, "#openwrt_submit")
    def open_wrt_logic(self)-> None:
            info=router_ip(self.current_path)
            self.pop_screen()
            self.push_screen(OpenWrtRouterIp(info,self.current_path))

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
