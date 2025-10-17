from typing import List, Optional, Dict, Any

class DatabaseService:
    def __init__(self, supabase, user_id: str = ""):
        self.supabase = supabase
        self.user_id = user_id

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        response = (
            self.supabase.table("task_table")
            .select("*")
            .eq("user_id", self.user_id)
            .execute()
        )
        return response.data or []

    def create_task(self, task_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        task_data["user_id"] = self.user_id
        response = (
            self.supabase.table("task_table")
            .insert(task_data)
            .execute()
        )
        return response.data[0] if response.data else None

    def update_task(self, task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase.table("task_table")
            .update(updates)
            .eq("id", task_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def delete_task(self, task_id: int) -> bool:
        response = (
            self.supabase.table("task_table")
            .delete()
            .eq("id", task_id)
            .eq("user_id", self.user_id)
            .execute()
        )
        return bool(response.data)

    def get_tasks_by_tag_name(self, search_term: str) -> List[Dict[str, Any]]:
        response = (
            self.supabase.table("task_tag_view")
            .select("*")
            .eq("task_user_id", self.user_id)
            .eq("tag_user_id", self.user_id)
            .ilike("tag_name", search_term)
            .execute()
        )
        return response.data or []

    def get_tags_for_task(self, task_id: int) -> List[Dict[str, Any]]:
        response = (
            self.supabase.table("task_tag_view")
            .select("*")
            .eq("task_id", task_id)
            .eq("task_user_id", self.user_id)
            .eq("tag_user_id", self.user_id)
            .execute()
        )
        return response.data or []

    def get_tag_by_name(self, tag_name: str) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase.table("tag_table")
            .select("*")
            .eq("name", tag_name)
            .eq("user_id", self.user_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def create_tag(self, tag_name: str) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase.table("tag_table")
            .insert({"name": tag_name, "user_id": self.user_id})
            .execute()
        )
        return response.data[0] if response.data else None

    def create_tag_with_description(self, tag_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        tag_data["user_id"] = self.user_id
        response = (
            self.supabase.table("tag_table")
            .insert(tag_data)
            .execute()
        )
        return response.data[0] if response.data else None

    def link_task_tag(self, task_id: int, tag_id: int) -> bool:
        response = (
            self.supabase.table("task_tag_join_table")
            .insert({"task_id": task_id, "tag_id": tag_id})
            .execute()
        )
        return bool(response.data)

    def remove_all_task_tags(self, task_id: int) -> bool:
        response = (
            self.supabase.table("task_tag_join_table")
            .delete()
            .eq("task_id", task_id)
            .execute()
        )
        return True

    def get_all_tags(self) -> List[Dict[str, Any]]:
        response = (
            self.supabase.table("tag_table")
            .select("*")
            .eq("user_id", self.user_id)
            .execute()
        )
        return response.data or []

    def update_tag(self, tag_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase.table("tag_table")
            .update(updates)
            .eq("id", tag_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def delete_tag(self, tag_id: int) -> bool:
        response = (
            self.supabase.table("tag_table")
            .delete()
            .eq("id", tag_id)
            .eq("user_id", self.user_id)
            .execute()
        )
        return True
