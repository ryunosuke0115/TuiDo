import os
from typing import List, Optional, Dict, Any
from supabase import create_client, Client

from dotenv import load_dotenv
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


class DatabaseService:
    @staticmethod
    def get_all_tasks() -> List[Dict[str, Any]]:
        response = (
            supabase.table("task_table")
            .select("*")
            .execute()
        )
        return response.data or []

    @staticmethod
    def create_task(task_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("task_table")
            .insert(task_data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def update_task(task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("task_table")
            .update(updates)
            .eq("id", task_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete_task(task_id: int) -> bool:
        response = (
            supabase.table("task_table")
            .delete()
            .eq("id", task_id)
            .execute()
        )
        return bool(response.data)

    @staticmethod
    def search_tasks(search_term: str) -> List[Dict[str, Any]]:
        response = (
            supabase.table("task_table")
            .select("*")
            .or_(f"name.ilike.%{search_term}%,description.ilike.%{search_term}%")
            .execute()
        )
        return response.data or []

    @staticmethod
    def get_tags_for_task(task_id: int) -> List[Dict[str, Any]]:
        response = (
            supabase.table("task_tag_view")
            .select("*")
            .eq("task_id", task_id)
            .execute()
        )
        return response.data or []

    @staticmethod
    def get_tag_by_name(tag_name: str) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("tag_table")
            .select("*")
            .eq("name", tag_name)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def create_tag(tag_name: str) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("tag_table")
            .insert({"name": tag_name})
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def create_tag_with_description(tag_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("tag_table")
            .insert(tag_data)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def link_task_tag(task_id: int, tag_id: int) -> bool:
        response = (
            supabase.table("task_tag_join_table")
            .insert({"task_id": task_id, "tag_id": tag_id})
            .execute()
        )
        return bool(response.data)

    @staticmethod
    def remove_all_task_tags(task_id: int) -> bool:
        response = (
            supabase.table("task_tag_join_table")
            .delete()
            .eq("task_id", task_id)
            .execute()
        )
        return True

    @staticmethod
    def get_all_tags() -> List[Dict[str, Any]]:
        response = (
            supabase.table("tag_table")
            .select("*")
            .execute()
        )
        return response.data or []

    @staticmethod
    def update_tag(tag_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = (
            supabase.table("tag_table")
            .update(updates)
            .eq("id", tag_id)
            .execute()
        )
        return response.data[0] if response.data else None

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        response = (
            supabase.table("tag_table")
            .delete()
            .eq("id", tag_id)
            .execute()
        )
        return True
