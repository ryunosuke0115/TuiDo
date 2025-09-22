from textual.widgets import Input, TextArea
from textual import events

class CustomInput(Input):
    def key_enter(self):
        self.screen.focus_next()

class CustomTextArea(TextArea):
    def key_up(self):
        self.screen.focus_previous()

    def key_down(self):
        self.screen.focus_next()

    def key_j(self):
        self.screen.focus_next()

    def key_k(self):
        self.screen.focus_previous()

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.screen.focus_next()
            event.prevent_default()
            event.stop()
        elif event.key in ("up", "down"):
            if event.key == "down":
                self.screen.focus_next()
            else:
                self.screen.focus_previous()
            event.prevent_default()
            event.stop()
