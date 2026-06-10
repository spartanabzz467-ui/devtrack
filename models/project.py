"""Project model — represents a project owned by a user, containing tasks."""

from datetime import datetime
from models.task import Task


class Project:
    """A project belonging to a user, containing multiple tasks."""

    def __init__(self, title: str, description: str = "", deadline: str = None,
                 created_at: str = None, project_id: int = None):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tasks: list[Task] = []

    # ── Task management ────────────────────────────────────────────────────────

    def add_task(self, task: Task):
        """Add a task to this project, auto-assigning an ID."""
        task.task_id = len(self.tasks) + 1
        self.tasks.append(task)

    def get_task(self, title: str) -> Task | None:
        """Return a task by title (case-insensitive), or None."""
        return next((t for t in self.tasks if t.title.lower() == title.lower()), None)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Return a task by its ID, or None."""
        return next((t for t in self.tasks if t.task_id == task_id), None)

    # ── Stats ──────────────────────────────────────────────────────────────────

    @property
    def total_tasks(self) -> int:
        return len(self.tasks)

    @property
    def completed_tasks(self) -> int:
        return sum(1 for t in self.tasks if t.completed)

    @property
    def progress(self) -> str:
        if self.total_tasks == 0:
            return "0%"
        pct = int((self.completed_tasks / self.total_tasks) * 100)
        return f"{pct}%"

    # ── Serialization ──────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "created_at": self.created_at,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(
            title=data["title"],
            description=data.get("description", ""),
            deadline=data.get("deadline"),
            created_at=data.get("created_at"),
            project_id=data.get("project_id"),
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project

    def __repr__(self):
        return f"Project({self.title!r}, tasks={self.total_tasks})"
