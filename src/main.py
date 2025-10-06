from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Header, Footer, Static, Label, ListView, TabbedContent, TabPane
from textual import on, events
from typing import List

from app.models import Task, Tag
from app.controllers import Controller
from ui.widgets import CustomInput, CustomTextArea
from handlers.handlers import KeyboardHandler, ActionHandler
from ui.ui_manager import UIManager
from handlers.task_handlers import TaskHandler
from handlers.tag_handlers import TagHandler
from handlers.tab_handlers import TabHandler

class TodoApp(App):
    BINDINGS = [
        ("j", "move_down", ""),
        ("k", "move_up", ""),
        ("down", "move_down", ""),
        ("up", "move_up", ""),
        ("left", "switch_tab_left", ""),
        ("right", "switch_tab_right", ""),
        ("h", "switch_tab_left", ""),
        ("l", "switch_tab_right", ""),
        ("tab", "focus_next", ""),
        ("shift+tab", "focus_previous", ""),
        ("q", "quit", "Quit"),
        ("escape", "back", ""),
        ("enter", "submit", "Submit/Activate"),
        ("ctrl+s", "save", "Save"),
        ("ctrl+r", "reload", "Reload"),
        ("ctrl+c", "clear_form", ""),
        ("i", "insert_mode", "Create"),
        ("e", "edit_mode", "Edit"),
        ("d", "delete_mode", "Delete"),
        ("f", "search_mode", "Search"),
        ("space", "complete_mode", "Toggle complete"),
    ]

    CSS = """
    Screen {
        background: $background;
    }

    #main-container {
        height: 100%;
    }

    #left-panel {
        width: 50%;
        padding: 1;
        border-right: solid $accent;
    }

    #right-panel {
        width: 50%;
        padding: 1;
        height: 100%;
        overflow: hidden;
    }

    #edit-form {
        height: auto;
        overflow: hidden;
        padding-top: 0;
        margin-top: 0 !important;
    }

    #edit-form Label:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    #task-details {
        height: auto;
        max-height: 80vh;
        overflow: hidden;
    }

    .label {
        margin-bottom: 0;
        margin-top: 0;
        color: $text;
        text-style: bold;
    }

    #left-title {
        margin-bottom: 0;
        margin-top: 0;
        padding-bottom: 0;
    }

    #right-title {
        margin-bottom: 0;
        margin-top: 0;
        padding-bottom: 0;
    }

    Input {
        width: 100%;
        margin-bottom: 0;
        margin-top: 0;
    }

    Input:focus {
        border: thick $accent;
    }

    TextArea {
        width: 100%;
        height: 3;
        margin-bottom: 0;
        margin-top: 0;
    }

    TextArea:focus {
        border: thick $accent;
    }

    .button-container {
        align: center middle;
        margin-top: 1;
        margin-bottom: 1;
    }

    Button {
        margin: 0 1;
    }

    Button:focus {
        text-style: bold;
        background: $accent;
    }

    ListView {
        border: round $accent;
    }

    ListView:focus {
        border: thick $accent;
    }

    ListItem {
        padding: 0 1;
    }

    ListItem {
        overflow: hidden;
        text-overflow: ellipsis;
    }

    ListItem:focus {
        background: $accent;
        color: $text;
    }

    .status {
        margin-top: 0;
        margin-bottom: 0;
        height: auto;
        background: $surface;
        border: round $accent;
        padding: 1;
    }

    .help-text {
        margin-top: 1;
        color: $text-muted;
        text-align: center;
    }

    Vertical {
        padding: 0;
        margin: 0;
    }

    Container {
        padding: 0;
        margin: 0;
    }

    .hidden {
        display: none;
    }

    #search-form {
        margin-bottom: 1;
        padding: 1;
        border: round $accent;
        background: $surface;
    }

    #search-input {
        margin-bottom: 1;
    }

    # #search-btn {
    #     margin: 0 1;
    #     height: 1;
    #     border: none;
    # }

    # #search-cancel-btn {
    #     margin: 0 1;
    #     height: 1;
    #     border: none;
    # }
    """

    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.keyboard_handler = KeyboardHandler(self)
        self.action_handler = ActionHandler(self)
        self.ui_manager = UIManager(self)
        self.task_handler = TaskHandler(self)
        self.tag_handler = TagHandler(self)
        self.tab_handler = TabHandler(self)

        self.current_editing_task: Task = None
        self.current_editing_tag: Tag = None
        self.pending_delete_task: Task = None
        self.pending_delete_tag: Tag = None
        self.current_tab = "pending"
        self.app_mode = "list"
        self.previous_app_mode = "list"

        self.search_pending_results: List[Task] = []
        self.search_completed_results: List[Task] = []
        self.previous_search_term = ""

        self.theme = "nord"

        self.controller.load_all_tasks()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            # 画面左側
            Container(
                Vertical(
                    Label("Search Tasks:", classes="label"),
                    CustomTextArea(placeholder="Enter search keyword...", id="search-input"),

                    Horizontal(
                        Button("Search", variant="primary", id="search-btn"),
                        Button("Clear", variant="default", id="search-clear-btn"),
                        Button("Cancel", variant="default", id="search-cancel-btn"),
                        classes="button-container"
                    ),
                    Static("↑↓/jk: Move, Enter: Search, Esc: Cancel", classes="help-text"),
                    id="search-form",
                    classes="hidden"
                ),
                Static("Task List", id="left-title", classes="label"),
                TabbedContent(id="task-tabs"),
                Static("", id="help-text", classes="help-text"),
                id="left-panel"
            ),

            # 画面右側
            Vertical(
                Static("Details", id="right-title", classes="label"),

                Static("Select a task to view details", id="task-details", classes="status"),

                Container(
                    Label("Task Name (required):", classes="label"),
                    CustomInput(placeholder="Enter task name...", id="task-name"),

                    Label("Deadline (YYYY-MM-DD or YYYY-MM-DD-HH:MM, optional):", classes="label"),
                    CustomInput(placeholder="e.g., 2024-12-31 or 2024-12-31-23:59", id="due-date"),

                    Label("Description:", classes="label"),
                    CustomTextArea(placeholder="Enter task description...", id="description"),

                    Label("Tags (comma-separated, optional):", classes="label"),
                    CustomTextArea(placeholder="e.g., work, urgent, project", id="tags-input"),

                    Horizontal(
                        Button("Save", variant="primary", id="save-btn"),
                        Button("Clear", variant="default", id="clear-btn"),
                        Button("Cancel", variant="default", id="cancel-btn"),
                        classes="button-container"
                    ),

                    Static("Enter: next field, Ctrl+S: save, Esc: cancel", classes="help-text"),
                    id="edit-form",
                    classes="hidden"
                ),

                Vertical(
                    Static("", id="delete-confirm-title", classes="label"),
                    Static("", id="delete-confirm-message", classes="status"),
                    Horizontal(
                        Button("NO - CANCEL", variant="default", id="cancel-delete-btn"),
                        Button("YES - DELETE", variant="error", id="confirm-delete-btn"),
                        classes="button-container"
                    ),
                    Static("Press 'y' to delete, 'n' to cancel", classes="help-text"),
                    id="delete-confirm-view",
                    classes="hidden"
                ),

                Container(
                    Label("Tag Name (required):", classes="label"),
                    CustomInput(placeholder="Enter tag name...", id="tag-name"),

                    Label("Description (optional):", classes="label"),
                    CustomTextArea(placeholder="Enter tag description...", id="tag-description"),

                    Horizontal(
                        Button("Save Tag", variant="primary", id="save-tag-btn"),
                        Button("Clear", variant="default", id="clear-tag-btn"),
                        Button("Cancel", variant="default", id="cancel-tag-btn"),
                        classes="button-container"
                    ),

                    Static("↑↓/jk: Move field, Ctrl+S: save, Esc: cancel", classes="help-text"),
                    id="tag-form",
                    classes="hidden"
                ),

                Vertical(
                    Static("", id="delete-tag-confirm-title", classes="label"),
                    Static("", id="delete-tag-confirm-message", classes="status"),
                    Horizontal(
                        Button("NO - CANCEL", variant="default", id="cancel-delete-tag-btn"),
                        Button("YES - DELETE", variant="error", id="confirm-delete-tag-btn"),
                        classes="button-container"
                    ),
                    Static("Press 'y' to delete, 'n' to cancel", classes="help-text"),
                    id="delete-tag-confirm-view",
                    classes="hidden"
                ),
                id="right-panel"
            ),
            id="main-container"
        )
        yield Footer()

    def on_mount(self):
        tabbed_content = self.query_one("#task-tabs", TabbedContent)
        tabbed_content.add_pane(TabPane("TODO", ListView(id="pending-tasks"), id="pending-tab"))
        tabbed_content.add_pane(TabPane("DONE", ListView(id="completed-tasks"), id="completed-tab"))
        tabbed_content.add_pane(TabPane("TAGS", ListView(id="tags-list"), id="tags-tab"))

        self.call_after_refresh(self.ui_manager.load_task_lists)
        self.ui_manager.update_help_text()

    def load_tasks(self):
        if not self.controller.load_all_tasks():
            return
        self.ui_manager.load_task_lists()

    def get_currently_selected_task(self) -> Task:
        if self.app_mode == "search_results":
            pending_source = self.search_pending_results
            completed_source = self.search_completed_results
        else:
            pending_source = self.controller.pending_tasks
            completed_source = self.controller.completed_tasks

        if self.current_tab == "pending":
            pending_list = self.query_one("#pending-tasks", ListView)
            if pending_list.index is not None and 0 <= pending_list.index < len(pending_source):
                return pending_source[pending_list.index]
        elif self.current_tab == "completed":
            completed_list = self.query_one("#completed-tasks", ListView)
            if completed_list.index is not None and 0 <= completed_list.index < len(completed_source):
                return completed_source[completed_list.index]
        return None

    def get_currently_selected_tag(self) -> Tag:
        if self.current_tab == "tags":
            tags_list = self.query_one("#tags-list", ListView)
            if tags_list.index is not None and 0 <= tags_list.index < len(self.controller.tags):
                return self.controller.tags[tags_list.index]
        return None

    def show_task_details(self, task: Task):
        self.ui_manager.show_task_details(task)

    def edit_task(self, task: Task):
        self.ui_manager.show_edit_form(task)

    def show_tag_form(self, tag: Tag = None):
        self.ui_manager.show_tag_form(tag)

    def edit_tag(self, tag: Tag):
        self.ui_manager.show_tag_form(tag)

    def show_delete_confirmation(self, task: Task):
        self.ui_manager.show_delete_confirmation(task)

    def show_tag_delete_confirmation(self, tag: Tag):
        self.ui_manager.show_tag_delete_confirmation(tag)

    def show_search_form(self):
        self.ui_manager.show_search_form()

    def back_to_list(self):
        self.ui_manager.back_to_list()

    def clear_form(self):
        self.ui_manager.clear_form()

    def update_help_text(self):
        self.ui_manager.update_help_text()

    def save_task(self):
        self.task_handler.save_task()

    def confirm_delete(self):
        self.task_handler.confirm_delete()

    def cancel_delete(self):
        self.task_handler.cancel_delete()

    def save_tag(self):
        self.tag_handler.save_tag()

    def clear_tag_form(self):
        self.tag_handler.clear_tag_form()

    def confirm_delete_tag(self):
        self.tag_handler.confirm_delete_tag()

    def cancel_delete_tag(self):
        self.tag_handler.cancel_delete_tag()

    # イベントハンドラ

    def on_key(self, event: events.Key) -> None:
        self.keyboard_handler.handle_global_keys(event)

    @on(TabbedContent.TabActivated)
    def on_tab_changed(self, event: TabbedContent.TabActivated) -> None:
        self.tab_handler.handle_tab_changed(event.tab.id)

    @on(ListView.Highlighted, "#pending-tasks")
    def on_pending_task_highlighted(self, event: ListView.Highlighted) -> None:
        self.tab_handler.handle_task_highlighted("pending", event.list_view.index)

    @on(ListView.Highlighted, "#completed-tasks")
    def on_completed_task_highlighted(self, event: ListView.Highlighted) -> None:
        self.tab_handler.handle_task_highlighted("completed", event.list_view.index)

    @on(ListView.Highlighted, "#tags-list")
    def on_tags_task_highlighted(self, event: ListView.Highlighted) -> None:
        self.tab_handler.handle_task_highlighted("tags", event.list_view.index)

    # アクションハンドラ

    def action_move_down(self):
        self.action_handler.handle_move_down()

    def action_move_up(self):
        self.action_handler.handle_move_up()

    def action_switch_tab_left(self):
        self.action_handler.handle_switch_tab_left()

    def action_switch_tab_right(self):
        self.action_handler.handle_switch_tab_right()

    def action_insert_mode(self):
        self.action_handler.handle_insert_mode()

    def action_edit_mode(self):
        self.action_handler.handle_edit_mode()

    def action_complete_mode(self):
        self.action_handler.handle_complete_mode()

    def action_delete_mode(self):
        self.action_handler.handle_delete_mode()

    def action_search_mode(self):
        self.action_handler.handle_search_mode()

    def action_reload(self):
        self.action_handler.handle_reload()

    def action_back(self):
        self.action_handler.handle_back()

    def action_save(self):
        self.action_handler.handle_save()

    def action_clear_form(self):
        self.action_handler.handle_clear_form()

    # ボタンのイベントハンドラ

    @on(Button.Pressed, "#save-btn")
    def on_save_btn_pressed(self):
        self.task_handler.save_task()

    @on(Button.Pressed, "#clear-btn")
    def on_clear_btn_pressed(self):
        self.ui_manager.clear_form()

    @on(Button.Pressed, "#cancel-btn")
    def on_cancel_btn_pressed(self):
        self.ui_manager.back_to_list()

    @on(Button.Pressed, "#confirm-delete-btn")
    def on_confirm_delete_btn_pressed(self):
        self.task_handler.confirm_delete()

    @on(Button.Pressed, "#cancel-delete-btn")
    def on_cancel_delete_btn_pressed(self):
        self.task_handler.cancel_delete()

    @on(Button.Pressed, "#save-tag-btn")
    def on_save_tag_btn_pressed(self):
        self.tag_handler.save_tag()

    @on(Button.Pressed, "#clear-tag-btn")
    def on_clear_tag_btn_pressed(self):
        self.tag_handler.clear_tag_form()

    @on(Button.Pressed, "#cancel-tag-btn")
    def on_cancel_tag_btn_pressed(self):
        self.ui_manager.back_to_list()

    @on(Button.Pressed, "#confirm-delete-tag-btn")
    def on_confirm_delete_tag_btn_pressed(self):
        self.tag_handler.confirm_delete_tag()

    @on(Button.Pressed, "#cancel-delete-tag-btn")
    def on_cancel_delete_tag_btn_pressed(self):
        self.tag_handler.cancel_delete_tag()

    @on(Button.Pressed, "#search-btn")
    def on_search_btn_pressed(self):
        self.task_handler.perform_search()

    @on(Button.Pressed, "#search-clear-btn")
    def on_search_clear_btn_pressed(self):
        self.task_handler.clear_search_input()

    @on(Button.Pressed, "#search-cancel-btn")
    def on_search_cancel_btn_pressed(self):
        self.task_handler.cancel_search()

    @on(Button.Pressed, "#back-btn")
    def on_back_btn_pressed(self):
        self.ui_manager.back_to_list()

def main():
    print("Loading ...")
    app = TodoApp()
    app.title = "TuiDo"
    app.sub_title = "Todo Manager App"
    print("Running TuiDo ...")
    app.run(mouse=False)

if __name__ == "__main__":
    main()
