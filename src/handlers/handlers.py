from textual import events

class KeyboardHandler:
    def __init__(self, app):
        self.app = app

    def handle_global_keys(self, event: events.Key) -> bool:
        if self.app.app_mode == "delete":
            return self._handle_delete_confirm_keys(event)
        elif self.app.app_mode in ["create", "edit"]:
            try:
                tag_form = self.app.query_one("#tag-form")
                if not tag_form.has_class("hidden"):
                    return self._handle_tag_form_keys(event)
                else:
                    return self._handle_form_keys(event)
            except:
                return self._handle_form_keys(event)
        elif self.app.app_mode == "search_form":
            return self._handle_search_form_keys(event)
        return False

    def _handle_tag_form_keys(self, event: events.Key) -> bool:
        focused = self.app.focused
        if not focused or not hasattr(focused, 'id'):
            return False

        if focused.id == "tag-name":
            if event.key in ("down"):
                self.app.query_one("#tag-description").focus()
                event.prevent_default()
                event.stop()
                return True
        elif focused.id == "tag-description":
            if event.key in ("up"):
                self.app.query_one("#tag-name").focus()
                event.prevent_default()
                event.stop()
                return True
            elif event.key in ("down"):
                self.app.query_one("#save-tag-btn").focus()
                event.prevent_default()
                event.stop()
                return True
        elif focused.id in ["save-tag-btn", "clear-tag-btn", "cancel-tag-btn"]:
            if event.key in ("up"):
                self.app.query_one("#tag-description").focus()
                event.prevent_default()
                event.stop()
                return True
            elif event.key == "left":
                if focused.id == "clear-tag-btn":
                    self.app.query_one("#save-tag-btn").focus()
                elif focused.id == "cancel-tag-btn":
                    self.app.query_one("#clear-tag-btn").focus()
                event.prevent_default()
                event.stop()
                return True
            elif event.key == "right":
                if focused.id == "save-tag-btn":
                    self.app.query_one("#clear-tag-btn").focus()
                elif focused.id == "clear-tag-btn":
                    self.app.query_one("#cancel-tag-btn").focus()
                event.prevent_default()
                event.stop()
                return True

        return False

    def _handle_delete_confirm_keys(self, event: events.Key) -> bool:
        is_tag_delete = self.app.pending_delete_tag is not None and self.app.pending_delete_task is None

        if event.key == "y":
            if is_tag_delete:
                self.app.confirm_delete_tag()
            else:
                self.app.confirm_delete()
            event.prevent_default(); event.stop(); return True
        elif event.key in ("n", "escape"):
            if is_tag_delete:
                self.app.cancel_delete_tag()
            else:
                self.app.cancel_delete()
            event.prevent_default(); event.stop(); return True
        elif event.key in ("left", "right", "h", "l"):
            try:
                pairs = [
                    ("#cancel-delete-btn", "#confirm-delete-btn"),
                    ("#cancel-delete-tag-btn", "#confirm-delete-tag-btn"),
                ]
                focused = self.app.focused
                focused_id = getattr(focused, "id", None)

                if focused_id is None:
                    for left_id, right_id in pairs:
                        if not self.app.query_one(left_id).parent.parent.has_class("hidden"):
                            self.app.query_one(left_id).focus()
                            break
                    event.prevent_default(); event.stop(); return True

                for left_id, right_id in pairs:
                    if self.app.query_one(left_id).parent.parent.has_class("hidden"):
                        continue

                    if focused_id == left_id.lstrip('#') and event.key in ("right", "l"):
                        self.app.query_one(right_id).focus()
                        break
                    elif focused_id == right_id.lstrip('#') and event.key in ("left", "h"):
                        self.app.query_one(left_id).focus()
                        break

            except Exception:
                pass
            event.prevent_default(); event.stop(); return True
        return False

    def _handle_form_keys(self, event: events.Key) -> bool:
        focused = self.app.focused
        if not focused or not hasattr(focused, 'id'):
            return False

        field_navigation = {
            "task-name": {
                "up": None,
                "down": "#due-date",
            },
            "due-date": {
                "up": "#task-name",
                "down": "#description",
            },
            "description": {
                "up": "#due-date",
                "down": "#tags-input",
            },
            "tags-input": {
                "up": "#description",
                "down": "#save-btn",
            }
        }

        button_navigation = {
            "save-btn": {
                "up": "#tags-input",
                "right": "#clear-btn"
            },
            "clear-btn": {
                "up": "#tags-input",
                "left": "#save-btn",
                "right": "#cancel-btn"
            },
            "cancel-btn": {
                "up": "#tags-input",
                "left": "#clear-btn"
            }
        }

        current_id = focused.id

        if current_id in field_navigation:
            nav = field_navigation[current_id]
            if event.key in nav and nav[event.key]:
                self.app.query_one(nav[event.key]).focus()
                event.prevent_default()
                event.stop()
                return True

        elif current_id in button_navigation:
            nav = button_navigation[current_id]
            if event.key in nav and nav[event.key]:
                self.app.query_one(nav[event.key]).focus()
                event.prevent_default()
                event.stop()
                return True
            elif event.key in ("down"):
                event.prevent_default()
                event.stop()
                return True

        return False


    def _handle_search_form_keys(self, event: events.Key) -> bool:
        focused = self.app.focused
        if not focused or not hasattr(focused, 'id'):
            return False

        field_navigation = {
            "search-input": {
                "down": "#search-btn",
            }
        }

        button_navigation = {
            "search-btn": {
                "up": "#search-input",
                "right": "#search-clear-btn",
            },
            "search-clear-btn": {
                "up": "#search-input",
                "left": "#search-btn",
                "right": "#search-cancel-btn"
            },
            "search-cancel-btn": {
                "up": "#search-input",
                "left": "#search-clear-btn",
            }
        }

        current_id = focused.id

        if current_id in field_navigation:
            nav = field_navigation[current_id]
            if event.key in nav and nav[event.key]:
                self.app.query_one(nav[event.key]).focus()
                event.prevent_default()
                event.stop()
                return True

        elif current_id in button_navigation:
            nav = button_navigation[current_id]
            if event.key in nav and nav[event.key]:
                self.app.query_one(nav[event.key]).focus()
                event.prevent_default()
                event.stop()
                return True

        return False

class ActionHandler:
    def __init__(self, app):
        self.app = app

    def handle_move_down(self):
        if self.app.app_mode in ["list", "search_results"]:
            if self.app.app_mode == "search_results":
                pending_source = self.app.search_pending_results
                completed_source = self.app.search_completed_results
            else:
                pending_source = self.app.controller.pending_tasks
                completed_source = self.app.controller.completed_tasks

            if self.app.current_tab == "pending":
                pending_list = self.app.query_one("#pending-tasks")
                if (pending_list.index is not None and
                    pending_list.index < len(pending_source) - 1):
                    pending_list.index += 1
            elif self.app.current_tab == "completed":
                completed_list = self.app.query_one("#completed-tasks")
                if (completed_list.index is not None and
                    completed_list.index < len(completed_source) - 1):
                    completed_list.index += 1
            elif self.app.current_tab == "tags":
                tags_list = self.app.query_one("#tags-list")
                if (tags_list.index is not None and
                    tags_list.index < len(self.app.controller.tags) - 1):
                    tags_list.index += 1

    def handle_move_up(self):
        if self.app.app_mode in ["list", "search_results"]:
            if self.app.current_tab == "pending":
                pending_list = self.app.query_one("#pending-tasks")
                if pending_list.index is not None and pending_list.index > 0:
                    pending_list.index -= 1
            elif self.app.current_tab == "completed":
                completed_list = self.app.query_one("#completed-tasks")
                if completed_list.index is not None and completed_list.index > 0:
                    completed_list.index -= 1
            elif self.app.current_tab == "tags":
                tags_list = self.app.query_one("#tags-list")
                if tags_list.index is not None and tags_list.index > 0:
                    tags_list.index -= 1

    def handle_switch_tab_left(self):
        if self.app.app_mode in ["list", "search_results"]:
            if self.app.app_mode == "search_results":
                pending_source = self.app.search_pending_results
                completed_source = self.app.search_completed_results
            else:
                pending_source = self.app.controller.pending_tasks
                completed_source = self.app.controller.completed_tasks
            tabbed_content = self.app.query_one("#task-tabs")

            if self.app.current_tab == "completed":
                # DONE → TODO
                tabbed_content.active = "pending-tab"
                self.app.current_tab = "pending"
                if pending_source:
                    pending_list = self.app.query_one("#pending-tasks")
                    if pending_list.index is None:
                        pending_list.index = 0
                    pending_list.focus()
                    self.app.show_task_details(pending_source[pending_list.index])
            elif self.app.current_tab == "tags":
                # TAGS → COMPLETED
                tabbed_content.active = "completed-tab"
                self.app.current_tab = "completed"
                if completed_source:
                    completed_list = self.app.query_one("#completed-tasks")
                    if completed_list.index is None:
                        completed_list.index = 0
                    completed_list.focus()
                    self.app.show_task_details(completed_source[completed_list.index])

    def handle_switch_tab_right(self):
        if self.app.app_mode in ["list", "search_results"]:
            if self.app.app_mode == "search_results":
                pending_source = self.app.search_pending_results
                completed_source = self.app.search_completed_results
            else:
                pending_source = self.app.controller.pending_tasks
                completed_source = self.app.controller.completed_tasks
            tabbed_content = self.app.query_one("#task-tabs")

            if self.app.current_tab == "pending":
                # TODO → DONE
                tabbed_content.active = "completed-tab"
                self.app.current_tab = "completed"
                if completed_source:
                    completed_list = self.app.query_one("#completed-tasks")
                    if completed_list.index is None:
                        completed_list.index = 0
                    completed_list.focus()
                    self.app.show_task_details(completed_source[completed_list.index])
            elif self.app.current_tab == "completed" and self.app.app_mode != "search_results":
                # COMPLETED → TAGS
                tabbed_content.active = "tags-tab"
                self.app.current_tab = "tags"
                self.app.ui_manager.update_help_text()
                if self.app.controller.tags:
                    tags_list = self.app.query_one("#tags-list")
                    if tags_list.index is None:
                        tags_list.index = 0
                    tags_list.focus()
                    if 0 <= tags_list.index < len(self.app.controller.tags):
                        self.app.ui_manager.show_tag_details(self.app.controller.tags[tags_list.index])

    def handle_insert_mode(self):
        if self.app.app_mode != "list":
            return

        if self.app.current_tab == "tags":
            self.app.show_tag_form()
        else:
            self.app.app_mode = "create"
            self.app.current_editing_task = None
            self.app.clear_form()
            self.app.update_help_text()

            right_title = self.app.query_one("#right-title")
            right_title.update("Create New Task")

            self.app.query_one("#task-details").add_class("hidden")
            self.app.query_one("#search-form").add_class("hidden")
            self.app.query_one("#edit-form").remove_class("hidden")

            task_name_input = self.app.query_one("#task-name")
            task_name_input.focus()

    def handle_edit_mode(self):
        if self.app.app_mode not in ["list", "search_results"]:
            return
        self.app.previous_app_mode = self.app.app_mode

        if self.app.current_tab == "tags":
            selected_tag = self.app.get_currently_selected_tag()
            if selected_tag:
                self.app.edit_tag(selected_tag)
        else:
            selected_task = self.app.get_currently_selected_task()
            if selected_task:
                self.app.edit_task(selected_task)

    def handle_complete_mode(self):
        if self.app.app_mode not in ["list", "search_results"]:
            return
        self.app.previous_app_mode = self.app.app_mode

        selected_task = self.app.get_currently_selected_task()
        if selected_task:
            updated_task = self.app.controller.toggle_task_completion(selected_task.id)
            if updated_task:
                self.app.load_tasks()
                if self.app.app_mode == "search_results":
                    search_term = self.app.previous_search_term
                    self.app.ui_manager.show_search_results(search_term)
                elif self.app.app_mode == "list":
                    return

    def handle_delete_mode(self):
        if self.app.app_mode not in ["list", "search_results"]:
            return
        self.app.previous_app_mode = self.app.app_mode

        if self.app.current_tab == "tags":
            selected_tag = self.app.get_currently_selected_tag()
            if selected_tag:
                self.app.show_tag_delete_confirmation(selected_tag)
        else:
            selected_task = self.app.get_currently_selected_task()
            if selected_task:
                self.app.show_delete_confirmation(selected_task)

    def handle_search_mode(self):
        if self.app.app_mode != "list":
            return

        self.app.app_mode = "search_form"
        self.app.show_search_form()
        self.app.ui_manager.update_help_text()

    def handle_reload(self):
        self.app.load_tasks()

    def handle_back(self):
        self.app.back_to_list()

    def handle_save(self):
        if self.app.app_mode in ["create", "edit"]:
            if self.app.current_tab in ["pending", "completed"]:
                self.app.save_task()
            elif self.app.current_tab == "tags":
                self.app.save_tag()

    def handle_clear_form(self):
        if self.app.app_mode in ["create", "edit"]:
            self.app.clear_form()
