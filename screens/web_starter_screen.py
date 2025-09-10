from textual.app import ComposeResult
from textual.widgets import Label, Button, Log
from textual.containers import Vertical
from textual.screen import Screen
from messages.deploy_failed_message import DeployFailed
import asyncio


class WebStarter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_label = Label("Status: Stopped", id="status")
        self.log_widget = Log(id="log")   # <-- uus nimi

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("You're about to start the web kit in IoT"),
            self.status_label,
            Button("Start web starter", id="start"),
            Button("Stop web starter", id="stop"),
            Button("Go back", id="pop"),
            self.log_widget,   # <-- kasutame uut nime
        )

    async def on_button_pressed(self, event: Button.Pressed):
        app = self.app  # viide App klassile

        if event.button.id == "start":
            if app.web_starter is None:
                try:
                    app.web_starter = await asyncio.create_subprocess_exec(
                        "web_starter",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.STDOUT,
                    )
                    self.status_label.update("Status: Running ✅")
                    self.log_widget.write_line(
                        f"Web starter launched (PID={app.web_starter.pid})"
                    )
                    asyncio.create_task(self.stream_output(app.web_starter))
                except:
                    self.post_message(DeployFailed("You're not in IoT",4))

        elif event.button.id == "stop":
            await app.stop_backend()
            self.status_label.update("Status: Stopped ❌")
            self.log_widget.write_line("Web starter stopped")

    async def stream_output(self, process):
        """Read and display stdout in the log in real time."""
        assert process.stdout is not None
        async for raw_line in process.stdout:
            line = raw_line.decode(errors="replace").rstrip()
            self.log_widget.write_line(line)
