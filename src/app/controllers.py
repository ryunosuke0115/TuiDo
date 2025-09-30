from typing import List, Optional
from .models import Task, Tag
from .services import DatabaseService
from .helpers import DateTimeHelper, TaskDisplayHelper, TaskSorter

class Controller:
    def __init__(self):
        self.pending_tasks: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.tags: List[Tag] = []
        self.task_tags_cache: dict = {}

    def load_all_tasks(self) -> bool:
        try:
            tasks_data = DatabaseService.get_all_tasks()

            all_tasks = [Task(**task_data) for task_data in tasks_data]

            self.task_tags_cache = {}
            for task in all_tasks:
                tags_data = DatabaseService.get_tags_for_task(task.id)
                tags = [Tag(id=tag['tag_id'], tag_name=tag['tag_name']) for tag in tags_data]
                self.task_tags_cache[task.id] = tags

            all_tags_data = DatabaseService.get_all_tags()
            self.all_tags = [Tag(id=tag['id'], tag_name=tag['name'], description=tag.get('description')) for tag in all_tags_data]
            self.tags = self.all_tags

            self.pending_tasks = [task for task in all_tasks if not task.is_completed]
            self.completed_tasks = [task for task in all_tasks if task.is_completed]

            self.pending_tasks = TaskSorter.sort_tasks_by_priority(self.pending_tasks)
            self.completed_tasks = TaskSorter.sort_tasks_by_priority(self.completed_tasks)

            return True
        except Exception as e:
            return False

    def create_new_task(self, name: str, description: str = None, due_date: str = None, tags: List[str] = None) -> Optional[Task]:
        try:
            due_date_iso = None
            if due_date:
                if not DateTimeHelper.validate_date_format(due_date):
                    raise ValueError("Invalid date format. Use YYYY-MM-DD-HH:MM")
                due_date_iso = DateTimeHelper.convert_to_iso8601_jst(due_date)

            task_data = {
                "name": name,
                "description": description,
                "due_date": due_date_iso,
                "is_completed": False
            }

            created_task_data = DatabaseService.create_task(task_data)
            if not created_task_data:
                return None

            task = Task(**created_task_data)

            if tags:
                self._add_tags_to_task(task.id, tags)

            return task
        except Exception as e:
            return None

    def update_task(self, task_id: int, name: str = None, description: str = None, due_date: str = None, tags: List[str] = None) -> Optional[Task]:
        try:
            updates = {}

            if name is not None:
                updates['name'] = name

            updates['description'] = description

            if due_date:
                if not DateTimeHelper.validate_date_format(due_date):
                    raise ValueError("Invalid date format. Use YYYY-MM-DD-HH:MM")
                updates['due_date'] = DateTimeHelper.convert_to_iso8601_jst(due_date)
            else:
                updates['due_date'] = None

            updated_task_data = DatabaseService.update_task(task_id, updates)
            if not updated_task_data:
                return None

            task = Task(**updated_task_data)

            DatabaseService.remove_all_task_tags(task_id)
            if tags:
                self._add_tags_to_task(task_id, tags)
                tags_data = DatabaseService.get_tags_for_task(task_id)
                self.task_tags_cache[task_id] = [
                    Tag(id=tag['tag_id'], tag_name=tag['tag_name']) for tag in tags_data
                ]
            else:
                self.task_tags_cache[task_id] = []

            return task
        except Exception as e:
            return None

    def delete_task(self, task_id: int) -> bool:
        try:
            success = DatabaseService.delete_task(task_id)
            if success and task_id in self.task_tags_cache:
                del self.task_tags_cache[task_id]
            return success
        except Exception as e:
            return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                return None

            new_status = not task.is_completed
            updates = {"is_completed": new_status}

            updated_task_data = DatabaseService.update_task(task_id, updates)
            if updated_task_data:
                return Task(**updated_task_data)
            return None
        except Exception as e:
            return None

    def search_tasks_by_tag_name(self, search_term: str) -> List[Task]:
        try:
            search_results_data = DatabaseService.get_tasks_by_tag_name(search_term)
            search_results = [Task(id=task['task_id'], name=task['task_name'], description=task['task_description'], due_date=task['task_due_date'], is_completed=task['task_is_completed'], created_at=task['task_created_at']) for task in search_results_data]

            return search_results
        except Exception as e:
            return []

    def _add_tags_to_task(self, task_id: int, tag_names: List[str]) -> bool:
        try:
            for tag_name in tag_names:
                existing_tag_data = DatabaseService.get_tag_by_name(tag_name)

                if existing_tag_data:
                    tag_id = existing_tag_data['id']
                else:
                    new_tag_data = DatabaseService.create_tag(tag_name)
                    if not new_tag_data:
                        continue
                    tag_id = new_tag_data['id']

                DatabaseService.link_task_tag(task_id, tag_id)

            tags_data = DatabaseService.get_tags_for_task(task_id)
            self.task_tags_cache[task_id] = [
                Tag(id=tag['tag_id'], tag_name=tag['tag_name']) for tag in tags_data
            ]

            return True
        except Exception as e:
            return False

    def get_all_tags(self) -> List[Tag]:
        return self.all_tags

    def count_completed_tasks_with_tag(self, tag: Tag) -> int:
        count = 0
        for p_task in self.completed_tasks:
            p_task_tags = self.task_tags_cache.get(p_task.id, [])
            if any(t.id == tag.id for t in p_task_tags):
                count += 1
        return count

    def count_tasks_with_tag(self, tag: Tag) -> int:
        count = 0
        for task_tags in self.task_tags_cache.values():
            if any(t.id == tag.id for t in task_tags):
                count += 1
        return count

    def create_new_tag(self, name: str, description: str = None) -> Optional[Tag]:
        try:
            if any(tag.tag_name == name for tag in self.all_tags):
                raise ValueError(f"Tag '{name}' already exists")

            tag_data = {"name": name}
            if description:
                tag_data["description"] = description

            created_tag_data = DatabaseService.create_tag_with_description(tag_data)
            if not created_tag_data:
                return None

            self.load_all_tasks()

            created_tag = Tag(id=created_tag_data['id'], tag_name=created_tag_data['name'],
            description=created_tag_data['description'])
            return created_tag
        except Exception as e:
            return None

    def update_tag(self, tag: Tag, name: str, description: str = None) -> Optional[Tag]:
        try:
            updates = {}
            if any(t.tag_name == name and t.id != tag.id for t in self.all_tags):
                raise ValueError(f"Tag '{name}' already exists")

            updates["name"] = name
            updates["description"] = description

            updated_tag_data = DatabaseService.update_tag(tag.id, updates)
            if not updated_tag_data:
                return None

            self.load_all_tasks()

            updated_tag = Tag(id=updated_tag_data['id'], tag_name=updated_tag_data['name'],
            description=updated_tag_data['description'])
            return updated_tag
        except Exception as e:
            return None

    def delete_tag(self, tag: Tag) -> bool:
        try:
            success = DatabaseService.delete_tag(tag.id)
            if not success:
                return False

            self.load_all_tasks()

            for task_id in list(self.task_tags_cache.keys()):
                self.task_tags_cache[task_id] = [t for t in self.task_tags_cache[task_id] if t.id != tag.id]

            return True
        except Exception as e:
            return False

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.pending_tasks + self.completed_tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_display_text(self, task: Task) -> str:
        return TaskDisplayHelper.get_task_display_text(task)

    def get_task_details_text(self, task: Task) -> str:
        tags = self.task_tags_cache.get(task.id, [])
        return TaskDisplayHelper.format_task_details(task, tags)

    def get_tags_for_task(self, task_id: int) -> List[Tag]:
        return self.task_tags_cache.get(task_id, [])

    def prepare_task_for_editing(self, task: Task) -> dict:
        tags = self.get_tags_for_task(task.id)
        tag_names = [tag.tag_name for tag in tags if tag]

        return {
            'name': task.name,
            'description': task.description or '',
            'due_date': DateTimeHelper.convert_from_iso8601_jst(task.due_date) if task.due_date else '',
            'tags': ', '.join(tag_names)
        }
