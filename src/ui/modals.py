from textual.screen import ModalScreen
from textual.containers import Container, Horizontal
from textual.widgets import Button, Static
from textual import on
from .widgets import CustomInput

class SearchModal(ModalScreen):
    def compose(self):
        yield Container(
            Static("Search Tasks", classes="modal-title"),
            CustomInput(placeholder="Enter search keyword...", id="search-input"),
            Horizontal(
                Button("Search", variant="primary", id="search-btn"),
                Button("Cancel", variant="default", id="cancel-btn"),
                classes="button-container"
            ),
            id="search-modal"
        )

    def on_mount(self):
        self.query_one("#search-input").focus()

    @on(Button.Pressed, "#search-btn")
    def search_tasks_handler(self):
        search_term = self.query_one("#search-input").value.strip()
        if search_term:
            self.dismiss({"action": "search", "term": search_term})
        else:
            self.dismiss(None)

    @on(Button.Pressed, "#cancel-btn")
    def cancel_search(self):
        self.dismiss(None)
