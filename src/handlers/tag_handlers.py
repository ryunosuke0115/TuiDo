class TagHandler:
    def __init__(self, app):
        self.app = app
    def save_tag(self):
        try:
            tag_name = self.app.query_one("#tag-name").value.strip()
            tag_description = self.app.query_one("#tag-description").text.strip()
            if not tag_name:
                return False

            success = False
            if self.app.app_mode == "create":
                tag = self.app.controller.create_new_tag(tag_name, tag_description or None)
                success = tag is not None
            elif self.app.app_mode == "edit" and self.app.current_editing_tag:
                tag = self.app.controller.update_tag(self.app.current_editing_tag, tag_name, tag_description or None)
                success = tag is not None

            if success:
                self.clear_tag_form()
                self.app.load_tasks()
                self.app.ui_manager.back_to_list()
                return True
            else:
                return False
        except Exception as e:
            return False

    def clear_tag_form(self):
        self.app.query_one("#tag-name").value = ""
        self.app.query_one("#tag-description").text = ""

    def confirm_delete_tag(self):
        if self.app.pending_delete_tag:
            success = self.app.controller.delete_tag(self.app.pending_delete_tag)
            self.app.pending_delete_tag = None

            if success:
                self.app.load_tasks()

            self.app.ui_manager.back_to_list()

    def cancel_delete_tag(self):
        self.app.pending_delete_tag = None
        self.app.ui_manager.back_to_list()
