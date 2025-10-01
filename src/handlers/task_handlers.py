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

            if self.app.previous_app_mode == "search_results":
                self.app.controller.load_all_tasks()
                search_term = self.app.previous_search_term
                self.app.ui_manager.show_search_results(search_term)
            else:
                self.app.ui_manager.clear_form()
                self.app.load_tasks()
                self.app.ui_manager.back_to_list()
            return True

        except ValueError as e:
            return False
        except Exception as e:
            return False

    def confirm_delete(self):
        if not self.app.pending_delete_task:
            return

        task_to_delete = self.app.pending_delete_task
        success = self.app.controller.delete_task(task_to_delete.id)
        self.app.pending_delete_task = None

        if success:
            if task_to_delete.is_completed:
                if task_to_delete in self.app.controller.completed_tasks:
                    self.app.controller.completed_tasks.remove(task_to_delete)
            else:
                if task_to_delete in self.app.controller.pending_tasks:
                    self.app.controller.pending_tasks.remove(task_to_delete)

            if self.app.previous_app_mode == "search_results":
                if task_to_delete.is_completed:
                    if task_to_delete in self.app.search_completed_results:
                        self.app.search_completed_results.remove(task_to_delete)
                else:
                    if task_to_delete in self.app.search_pending_results:
                        self.app.search_pending_results.remove(task_to_delete)

            self.app.app_mode = self.app.previous_app_mode
            self.app.ui_manager._hide_all_views()
            self.app.query_one("#task-tabs").remove_class("hidden")
            self.app.query_one("#task-details").remove_class("hidden")
            self.app.ui_manager.load_task_lists()
            self.app.ui_manager.update_help_text()
        else:
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

    def cancel_search(self):
        self.app.query_one("#task-tabs").remove_class("hidden")
        self.app.query_one("#search-form").add_class("hidden")
        self.app.ui_manager.back_to_list()

    def clear_search_input(self):
        self.app.query_one("#search-input").text = ""

    def perform_search(self):
        search_term = self.app.query_one("#search-input").text.strip()
        self.app.ui_manager.show_search_results(search_term)
