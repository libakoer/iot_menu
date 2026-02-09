# screens/web_starter_screen.py
from __future__ import annotations

import asyncio
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Button, Log
from textual.screen import Screen
from textual import on

from messages.deploy_failed_message import DeployFailed
from messages.web_output import WebOutput


class WebStarter(Screen):
    """
    Ekraan, mis näitab web starteri olekut ja logi.
    Protsess ise jookseb App-i tasemel. Ekraan võib tulla ja minna.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_label = Label("Status: Stopped", id="status")
        self.log_widget = Log(id="log")       
        self._popping: bool = False
        self._stopping: bool = False  


    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("You're about to start the web kit in IoT"),
            self.status_label,
            Button("Start web starter", id="start"),
            Button("Stop web starter", id="stop"),
            Button("Go back", id="pop"),
            self.log_widget,
        )

    async def on_mount(self) -> None:
        """Taasesita buffer ja kuva hetkestaatus ekraani avamisel."""
        app = self.app
        running = app.web_starter is not None and app.web_starter.returncode is None
        self.status_label.update("Status: Running ✅" if running else "Status: Stopped ❌")

        # Taasesita olemasolev buffer
        if app.web_log_buffer:
            self.log_widget.clear()
            for line in app.web_log_buffer:
                self.log_widget.write_line(line)

    async def on_button_pressed(self, event: Button.Pressed):
        app = self.app

        if event.button.id == "start":
            try:
                await app.start_web_starter()
                # Uuenda olekut
                running = app.web_starter is not None and app.web_starter.returncode is None
                self.status_label.update("Status: Running ✅" if running else "Status: Stopped ❌")

                # Logi teade
                if running and app.web_starter:
                    self.log_widget.write_line(f"Web starter launched (PID={app.web_starter.pid})")
                else:
                    self.log_widget.write_line("Web starter did not start.")
            except Exception:
                # Kui käivitus ebaõnnestus (nt pole IoT keskkonnas)
                self.post_message(DeployFailed("You're not in IoT", 4))
            finally:
                event.stop()  # Ära lase sündmusel mullitada App-i tasemele

        
        elif event.button.id == "stop":
            # väldi korduvat stop'i
            if self._stopping:
                event.stop(); return
            self._stopping = True
            # Stop ei tohi logi/ekraaniga võidu rabeleda; stopib vaid backend'i
            try:
                await app.stop_backend()
                self.status_label.update("Status: Stopped ❌")
                # (stoppimise logirida tuleb App-ist WebOutputi kaudu)
            finally:
                self._stopping = False
            event.stop()


        
        elif event.button.id == "pop":
            # --- DEBOUNCE / LOCK: ainult 1 pop ---
            if self._popping:
                event.stop(); return
            self._popping = True
            # keelame nupu, et kasutaja ei saaks topeltklikkida
            try:
                self.query_one("#pop", Button).disabled = True
            except Exception:
                pass
            
            try:
                self.app.pop_screen()
            except Exception:
                # igaks juhuks neelame, kui virnas enam ei ole mida poppida
                pass
            finally:
                event.stop()



    @on(WebOutput)
    def _on_web_output(self, msg: WebOutput) -> None:
        """Lisa saabuv logirida logi vidinasse, kui ekraan on aktiivne."""
        if self.is_mounted:
            self.log_widget.write_line(msg.line)