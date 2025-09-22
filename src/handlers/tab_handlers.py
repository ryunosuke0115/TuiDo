class TabHandler:
    def __init__(self, app):
        self.app = app

    def handle_tab_changed(self, tab_id: str):
        if tab_id == "pending-tab":
            self.app.current_tab = "pending"
            if self.app.controller.pending_tasks:
                pending_list = self.app.query_one("#pending-tasks")
                if pending_list.index is not None and 0 <= pending_list.index < len(self.app.controller.pending_tasks):
                    self.app.ui_manager.show_task_details(self.app.controller.pending_tasks[pending_list.index])
        elif tab_id == "completed-tab":
            self.app.current_tab = "completed"
            if self.app.controller.completed_tasks:
                completed_list = self.app.query_one("#completed-tasks")
                if completed_list.index is not None and 0 <= completed_list.index < len(self.app.controller.completed_tasks):
                    self.app.ui_manager.show_task_details(self.app.controller.completed_tasks[completed_list.index])
        elif tab_id == "tags-tab":
            self.app.current_tab = "tags"
            self.app.ui_manager.update_help_text()
            if self.app.controller.tags:
                tags_list = self.app.query_one("#tags-list")
                if tags_list.index is not None and 0 <= tags_list.index < len(self.app.controller.tags):
                    self.app.ui_manager.show_tag_details(self.app.controller.tags[tags_list.index])

    def handle_task_highlighted(self, tab_type: str, index: int):
        if self.app.app_mode != "list":
            return

        if tab_type == "pending":
            if (index is not None and 0 <= index < len(self.app.controller.pending_tasks)
                and self.app.controller.pending_tasks):
                selected_task = self.app.controller.pending_tasks[index]
                self.app.ui_manager.show_task_details(selected_task)
        elif tab_type == "completed":
            if (index is not None and 0 <= index < len(self.app.controller.completed_tasks)
                and self.app.controller.completed_tasks):
                selected_task = self.app.controller.completed_tasks[index]
                self.app.ui_manager.show_task_details(selected_task)
        elif tab_type == "tags":
            if (index is not None and 0 <= index < len(self.app.controller.tags)
                and self.app.controller.tags):
                selected_tag = self.app.controller.tags[index]
                self.app.ui_manager.show_tag_details(selected_tag)
