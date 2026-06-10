"""Task model — represents a unit of work within a project."""

from datetime import datetime


class Task:
    """A task belonging to a project."""

    def __init__(self, title: str, description: str = "", completed: bool = False,
                 created_at: str = None, task_id: int = None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def complete(self):
        """Mark this task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Serialize task to a dictionary for JSON storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize a task from a dictionary."""
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            task_id=data.get("task_id"),
        )

    def __repr__(self):
        status = "✓" if self.completed else "○"
        return f"Task({status} {self.title!r})"
