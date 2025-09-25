from datetime import datetime, timezone, timedelta
from .models import Task

class DateTimeHelper:
    JST_TZ = timezone(timedelta(hours=9))

    @staticmethod
    def calculate_time_remaining(due_date_str: str) -> str:
        if not due_date_str:
            return "No deadline"

        now = datetime.now(DateTimeHelper.JST_TZ)

        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            due_date_jst = due_date.astimezone(DateTimeHelper.JST_TZ)

            remaining = due_date_jst - now

            if remaining.total_seconds() < 0:
                overdue = now - due_date_jst
                days = overdue.days
                hours = overdue.seconds // 3600
                if days > 0:
                    return f"Overdue by {days}d"
                else:
                    return f"Overdue by {hours}h"
            else:
                total_hours = remaining.total_seconds() / 3600
                days = remaining.days

                if total_hours <= 24:
                    hours = int(total_hours)
                    return f"{hours}h remaining"
                elif days < 30:
                    return f"{days}d remaining"
                else:
                    months = days // 30
                    return f"{months}m remaining"
        except Exception:
            return "Invalid date"

    @staticmethod
    def convert_from_iso8601_jst(iso_date_str: str) -> str:
        try:
            dt = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
            jst_dt = dt.astimezone(DateTimeHelper.JST_TZ)
            return jst_dt.strftime("%Y-%m-%d-%H:%M")
        except Exception:
            return iso_date_str

    @staticmethod
    def convert_to_iso8601_jst(date_str: str) -> str:
        formats = ["%Y-%m-%d-%H:%M", "%Y-%m-%d"]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if fmt == "%Y-%m-%d":
                    dt = dt.replace(hour=0, minute=0)
                dt_with_tz = dt.replace(second=0, microsecond=0, tzinfo=DateTimeHelper.JST_TZ)
                return dt_with_tz.isoformat()
            except Exception:
                continue
        return "Invalid date format"

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        formats = ["%Y-%m-%d-%H:%M", "%Y-%m-%d"]
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False


class TaskDisplayHelper:
    @staticmethod
    def get_task_display_text(task: Task) -> str:
        if task.is_completed:
            return task.display_name
        else:
            if task.due_date:
                time_remaining = DateTimeHelper.calculate_time_remaining(task.due_date)
                return f"[b u]{task.display_name}[/b u] ({time_remaining})"
            else:
                return f"[b u]{task.display_name}[/b u] (No deadline)"

    @staticmethod
    def format_task_details(task: Task, tags: list) -> str:
        details_text = "Task information:\n\n"

        details_text += f"  [b u]name[/b u]: {task.name}\n"

        if task.created_at:
            formatted_date = DateTimeHelper.convert_from_iso8601_jst(task.created_at)
            details_text += f"  [b u]created_at[/b u]: {formatted_date}\n"

        if task.due_date:
            formatted_date = DateTimeHelper.convert_from_iso8601_jst(task.due_date)
            details_text += f"  [b u]due_date[/b u]: {formatted_date}\n"

        if task.description:
            details_text += f"  [b u]description[/b u]: {task.description or 'None'}\n"

        if tags:
            details_text += "\nTags:\n"
            for tag in tags:
                details_text += f"  - {tag.tag_name}\n"
        else:
            details_text += "\nTags: No tags\n"
        return details_text


class TaskSorter:
    @staticmethod
    def sort_tasks_by_priority(tasks: list) -> list:
        def sort_key(task):
            if not task.due_date:
                # priority 3
                return (3, 0)
            else:
                try:
                    due_datetime = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                    current_time = datetime.now(due_datetime.tzinfo)

                    if due_datetime < current_time:
                        # priority 2
                        return (2, -due_datetime.timestamp())
                    else:
                        # priority 1
                        return (1, due_datetime.timestamp())
                except Exception:
                    return (3, 0)

        return sorted(tasks, key=sort_key)
