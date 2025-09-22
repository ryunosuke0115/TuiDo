from app.models import Task

class TaskHandler:
    def __init__(self, app):
        self.app = app

    def save_task(self):
        try:
            task_name = self.app.query_one("#task-name").value.strip()
            due_date = self.app.query_one("#due-date").value.strip()
            description = self.app.query_one("#description").text.strip()
            tags_input = self.app.query_one("#tags-input").text.strip()

            if not task_name:
                return False

            tags = []
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            if self.app.app_mode == "create":
                task = self.app.controller.create_new_task(
                    name=task_name,
                    description=description or None,
                    due_date=due_date or None,
                    tags=tags
                )

                if not task:
                    return False

            elif self.app.app_mode == "edit":
                task = self.app.controller.update_task(
                    task_id=self.app.current_editing_task.id,
                    name=task_name,
                    description=description or None,
                    due_date=due_date or None,
                    tags=tags
                )

                if not task:
                    return False

            self.app.ui_manager.clear_form()
            self.app.load_tasks()
            self.app.ui_manager.back_to_list()
            return True

        except ValueError as e:
            return False
        except Exception as e:
            return False

    def confirm_delete(self):
        if self.app.pending_delete_task:
            success = self.app.controller.delete_task(self.app.pending_delete_task.id)
            if success:
                self.app.load_tasks()

            self.app.pending_delete_task = None
            self.app.ui_manager.back_to_list()

    def cancel_delete(self):
        self.app.pending_delete_task = None
        self.app.ui_manager.back_to_list()

    def toggle_task_completion(self, task: Task) -> bool:
        updated_task = self.app.controller.toggle_task_completion(task.id)
        if updated_task:
            return True
        else:
            return False

    def perform_search(self):
        search_term = self.app.query_one("#search-input").value.strip()
        if search_term:
            tasks = self.app.controller.search_tasks(search_term)
            self.app.ui_manager.show_search_results(tasks, search_term)
        else:
            self.app.ui_manager.back_to_list()

    def cancel_search(self):
        self.app.ui_manager.back_to_list()

    def clear_search_input(self):
        self.app.query_one("#search-input").value = ""
