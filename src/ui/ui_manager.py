from app.models import Task, Tag
from app.helpers import TaskSorter
from typing import List
from textual.widgets import Label, ListItem

class UIManager:
    def __init__(self, app):
        self.app = app

    def update_help_text(self):
        try:
            help_text_widget = self.app.query_one("#help-text")

            help_messages = {
                "list": "↑↓/jk: Move, ←→/hl: Switch tab, i: New, e: Edit, d: Delete, Space: Complete, f: Search, q: Quit",
                "create": "↑↓/jk: Move field, Enter: Next field, Ctrl+S: Save, Esc: Cancel",
                "edit": "↑↓/jk: Move field, Enter: Next field, Ctrl+S: Save, Esc: Cancel",
                "delete_confirm": "←→: Switch button, y: Delete, n/Esc: Cancel",
                "search_form": "↑↓/jk: Move, Enter: Search, Esc: Cancel",
                "search_results": "Esc: Back to task list"
            }

            if self.app.app_mode == "list" and self.app.current_tab == "tags":
                help_messages["list"] = "↑↓/jk: Move, ←→/hl: Switch tab, i: New tag, e: Edit tag, d: Delete tag, q: Quit"

            message = help_messages.get(self.app.app_mode, "")
            help_text_widget.update(message)
        except Exception:
            pass

    def show_task_details(self, task: Task):
        try:
            details_text = self.app.controller.get_task_details_text(task)
            task_details = self.app.query_one("#task-details")
            task_details.update(details_text)
        except Exception as e:
            pass

    def show_delete_confirmation(self, task: Task):
        self.app.app_mode = "delete"
        self.app.pending_delete_task = task
        self.update_help_text()

        right_title = self.app.query_one("#right-title")
        right_title.update("DELETE CONFIRMATION")

        delete_title = self.app.query_one("#delete-confirm-title")
        delete_title.update(f"Delete Task: {task.name}")

        delete_message = self.app.query_one("#delete-confirm-message")
        delete_message.update(
            f"⚠️  WARNING: This action cannot be undone!\n\n"
            f"Task Name: {task.name}\n"
            f"Description: {task.description or 'No description'}\n\n"
            f"Are you sure you want to delete this task?"
        )

        self._hide_all_views()
        self.app.query_one("#delete-confirm-view").remove_class("hidden")

        self.app.query_one("#cancel-delete-btn").focus()

    def show_tag_form(self, tag: Tag = None):
        if tag:
            self.app.app_mode = "edit"
            self.app.current_editing_tag = tag

            self.app.query_one("#tag-name").value = tag.tag_name
            self.app.query_one("#tag-description").text = ""

            right_title = self.app.query_one("#right-title")
            right_title.update(f"Edit Tag: {tag.tag_name}")
        else:
            self.app.app_mode = "create"
            self.app.current_editing_tag = None

            self.app.query_one("#tag-name").value = ""
            self.app.query_one("#tag-description").text = ""

            right_title = self.app.query_one("#right-title")
            right_title.update("Create New Tag")

        self.update_help_text()

        self._hide_all_views()
        self.app.query_one("#tag-form").remove_class("hidden")

        tag_name_input = self.app.query_one("#tag-name")
        tag_name_input.focus()

    def show_tag_delete_confirmation(self, tag: Tag):
        self.app.app_mode = "delete"
        self.app.pending_delete_tag = tag
        self.update_help_text()

        right_title = self.app.query_one("#right-title")
        right_title.update("DELETE TAG CONFIRMATION")

        delete_title = self.app.query_one("#delete-tag-confirm-title")
        delete_title.update(f"Delete Tag: {tag.tag_name}")

        task_count = self.app.controller.count_tasks_with_tag(tag)
        delete_message = self.app.query_one("#delete-tag-confirm-message")
        delete_message.update(
            f"⚠️  WARNING: This action cannot be undone!\n\n"
            f"Tag Name: {tag.tag_name}\n"
            f"Used by {task_count} task(s)\n\n"
            f"Are you sure you want to delete this tag?"
        )

        self._hide_all_views()
        self.app.query_one("#delete-tag-confirm-view").remove_class("hidden")

        self.app.query_one("#cancel-delete-tag-btn").focus()

    def show_edit_form(self, task: Task = None):
        if task:
            self.app.app_mode = "edit"
            self.app.current_editing_task = task

            edit_data = self.app.controller.prepare_task_for_editing(task)

            self.app.query_one("#task-name").value = edit_data['name']
            self.app.query_one("#due-date").value = edit_data['due_date']
            self.app.query_one("#description").text = edit_data['description']
            self.app.query_one("#tags-input").text = edit_data['tags']

            right_title = self.app.query_one("#right-title")
            right_title.update(f"Edit Task: {task.name}")
        else:
            self.app.app_mode = "create"
            self.app.current_editing_task = None

            right_title = self.app.query_one("#right-title")
            right_title.update("Create New Task")

        self.update_help_text()

        self._hide_all_views()
        self.app.query_one("#edit-form").remove_class("hidden")

        task_name_input = self.app.query_one("#task-name")
        task_name_input.focus()

    def back_to_list(self):
        self.app.previous_search_term = ""
        if self.app.app_mode in ["edit", "delete"]:
            self.app.app_mode = self.app.previous_app_mode

            self.app.current_editing_task = None
            self.app.pending_delete_task = None

            self._hide_all_views()
            self.app.query_one("#task-tabs").remove_class("hidden")
            self.app.query_one("#task-details").remove_class("hidden")
            if self.app.previous_app_mode != "search_results":
                left_title = self.app.query_one("#left-title")
                left_title.update("Task List")
            right_title = self.app.query_one("#right-title")
            right_title.update("Details")

            self.update_help_text()
            self.app.query_one("#pending-tasks").focus()
            return

        self.app.search_pending_results = []
        self.app.search_completed_results = []
        if self.app.app_mode == "list":
            return
        self.app.app_mode = "list"
        self.app.current_editing_task = None
        self.app.current_editing_tag = None
        self.app.pending_delete_task = None
        self.app.pending_delete_tag = None

        if self.app.current_tab == "tags":
            self.load_tag_list()

            if self.app.controller.tags:
                tags_list = self.app.query_one("#tags-list")
                tags_list.index = 0
                tags_list.focus()
                self.show_tag_details(self.app.controller.tags[0])
            else:
                task_details = self.app.query_one("#task-details")
                task_details.update("No tags available")
        elif self.app.current_tab == "pending":
            if self.app.controller.pending_tasks:
                pending_list = self.app.query_one("#pending-tasks")
                pending_list.index = 0
                pending_list.focus()
                self.show_task_details(self.app.controller.pending_tasks[0])
        elif self.app.current_tab == "completed":
            if self.app.controller.completed_tasks:
                completed_list = self.app.query_one("#completed-tasks")
                completed_list.index = 0
                completed_list.focus()
                self.show_task_details(self.app.controller.completed_tasks[0])

        self.load_task_lists()
        self.update_help_text()

        left_title = self.app.query_one("#left-title")
        left_title.update("Task List")
        right_title = self.app.query_one("#right-title")
        right_title.update("Details")

        self._hide_all_views()
        self.app.query_one("#task-details").remove_class("hidden")
        self.app.query_one("#task-tabs").remove_class("hidden")

        selected_task = self.app.get_currently_selected_task()
        if selected_task:
            self.show_task_details(selected_task)

        if self.app.current_tab == "pending" and self.app.controller.pending_tasks:
            self.app.query_one("#pending-tasks").focus()
        elif self.app.current_tab == "completed" and self.app.controller.completed_tasks:
            self.app.query_one("#completed-tasks").focus()

    def clear_form(self):
        self.app.query_one("#task-name").value = ""
        self.app.query_one("#due-date").value = ""
        self.app.query_one("#description").text = ""
        self.app.query_one("#tags-input").text = ""

    def show_tag_details(self, tag: Tag):
        try:
            task_count = self.app.controller.count_tasks_with_tag(tag)
            details_text = f"Tag Information:\n\n"
            details_text += f"  [b u]name[/b u]: {tag.tag_name}\n"
            if tag.description:
                details_text += f"  [b u]description[/b u]: {tag.description}\n\n"
            else:
                details_text += "\n"
            details_text += f"This tag is used by the following {task_count} tasks:\n"

            for task in self.app.controller.pending_tasks + self.app.controller.completed_tasks:
                task_tags = self.app.controller.get_tags_for_task(task.id)
                if any(t.id == tag.id for t in task_tags):
                    status = "✓" if task.is_completed else "○"
                    details_text += f"  {status} {task.name}\n"

            if task_count == 0:
                details_text += "  No tasks using this tag\n"
            task_details = self.app.query_one("#task-details")
            task_details.update(details_text)
        except Exception as e:
            pass

    def load_tag_list(self):
        try:
            tags_list = self.app.query_one("#tags-list")
            tags_list.clear()

            for tag in self.app.controller.tags:
                task_count = self.app.controller.count_tasks_with_tag(tag)
                completed_task_count = self.app.controller.count_completed_tasks_with_tag(tag)
                display_text = f"[b u]{tag.tag_name}[/b u] ({completed_task_count} / {task_count} tasks)"
                tags_list.append(ListItem(Label(display_text)))

            if not self.app.controller.tags:
                tags_list.append(ListItem(Label("No tags available")))
        except Exception as e:
            pass

    def load_task_lists(self):
        try:
            pending_list = self.app.query_one("#pending-tasks")
            completed_list = self.app.query_one("#completed-tasks")
            pending_list.clear()
            completed_list.clear()

            if self.app.app_mode == "search_results":
                pending_source = self.app.search_pending_results
                completed_source = self.app.search_completed_results
            else:
                pending_source = self.app.controller.pending_tasks
                completed_source = self.app.controller.completed_tasks

            for task in pending_source:
                task_text = self.app.controller.get_task_display_text(task)
                pending_list.append(ListItem(Label(task_text)))

            for task in completed_source:
                task_text = self.app.controller.get_task_display_text(task)
                completed_list.append(ListItem(Label(task_text)))

            self.load_tag_list()

            if self.app.current_tab == "tags":
                self.load_tag_list()

                tags_list = self.app.query_one("#tags-list")
                if self.app.controller.tags:
                    tags_list.index = 0
                    tags_list.focus()
                    self.show_tag_details(self.app.controller.tags[0])
                else:
                    tags_list.append(ListItem(Label("No tags available")))
                    task_details = self.app.query_one("#task-details")
                    task_details.update("No tags available")
            elif pending_source:
                pending_list.index = 0
                self.app.current_tab = "pending"
                pending_list.focus()
                self.show_task_details(pending_source[0])
            elif completed_source:
                completed_list.index = 0
                self.app.current_tab = "completed"
                completed_list.focus()
                self.show_task_details(completed_source[0])
            else:
                pending_list.append(ListItem(Label("No pending tasks")))
                completed_list.append(ListItem(Label("No completed tasks")))
                task_details = self.app.query_one("#task-details")
                task_details.update("No tasks available")

        except Exception as e:
            pass

    def _hide_all_views(self):
        views_to_hide = [
            "#task-details", "#edit-form", "#tag-form", "#search-form","#delete-confirm-view","#delete-tag-confirm-view"
        ]

        for view_id in views_to_hide:
            try:
                self.app.query_one(view_id).add_class("hidden")
            except Exception:
                pass

    def show_search_form(self):
        self.app.query_one("#edit-form").add_class("hidden")
        self.app.query_one("#tag-form").add_class("hidden")
        self.app.query_one("#delete-confirm-view").add_class("hidden")
        self.app.query_one("#delete-tag-confirm-view").add_class("hidden")
        self.app.query_one("#task-tabs").add_class("hidden")

        search_form = self.app.query_one("#search-form")
        search_form.remove_class("hidden")

        search_input = self.app.query_one("#search-input")
        self.app.call_after_refresh(lambda: self.app.set_focus(search_input))

    def show_search_results(self, search_term: str):
        self.app.previous_search_term = search_term
        if not search_term:
            self.app.task_handler.cancel_search()
            return

        try:
            self.app.app_mode = "search_results"
            self.update_help_text()

            left_title = self.app.query_one("#left-title")
            left_title.update(f"Results for Tag: '{search_term}'")
            right_title = self.app.query_one("#right-title")
            right_title.update("Details")

            self._hide_all_views()
            self.app.query_one("#task-tabs").remove_class("hidden")
            self.app.query_one("#task-details").remove_class("hidden")

            search_results_data = self.app.controller.search_tasks_by_tag_name(search_term)

            search_pending_tasks = [t for t in search_results_data if not t.is_completed]
            search_completed_tasks = [t for t in search_results_data if t.is_completed]

            search_pending_tasks = TaskSorter.sort_tasks_by_priority(search_pending_tasks)
            search_completed_tasks = TaskSorter.sort_tasks_by_priority(search_completed_tasks)

            self.app.search_pending_results = search_pending_tasks
            self.app.search_completed_results = search_completed_tasks

            pending_list = self.app.query_one("#pending-tasks")
            completed_list = self.app.query_one("#completed-tasks")
            pending_list.clear()
            completed_list.clear()

            for task in search_pending_tasks:
                task_text = self.app.controller.get_task_display_text(task)
                pending_list.append(ListItem(Label(task_text)))

            for task in search_completed_tasks:
                task_text = self.app.controller.get_task_display_text(task)
                completed_list.append(ListItem(Label(task_text)))

            if search_pending_tasks:
                pending_list.index = 0
                self.app.current_tab = "pending"
                pending_list.focus()
                self.show_task_details(search_pending_tasks[0])
            elif search_completed_tasks:
                completed_list.index = 0
                self.app.current_tab = "completed"
                completed_list.focus()
                self.show_task_details(search_completed_tasks[0])
            else:
                pending_list.append(ListItem(Label("No matching tasks found")))
                completed_list.append(ListItem(Label("No matching tasks found")))
                task_details = self.app.query_one("#task-details")
                task_details.update(f"No tasks found with tag '{search_term}'")

        except Exception as e:
            pass
