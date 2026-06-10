"""User model — top-level entity that owns projects."""

from datetime import datetime
from models.project import Project


class User:
    """A user who owns one or more projects."""

    def __init__(self, name: str, email: str = "", created_at: str = None, user_id: int = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.projects: list[Project] = []

    # ── Project management ─────────────────────────────────────────────────────

    def add_project(self, project: Project):
        """Add a project to this user, auto-assigning an ID."""
        project.project_id = len(self.projects) + 1
        self.projects.append(project)

    def get_project(self, title: str) -> Project | None:
        """Return a project by title (case-insensitive), or None."""
        return next((p for p in self.projects if p.title.lower() == title.lower()), None)

    def get_project_by_id(self, project_id: int) -> Project | None:
        """Return a project by its ID, or None."""
        return next((p for p in self.projects if p.project_id == project_id), None)

    # ── Serialization ──────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            name=data["name"],
            email=data.get("email", ""),
            created_at=data.get("created_at"),
            user_id=data.get("user_id"),
        )
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return user

    def __repr__(self):
        return f"User({self.name!r}, projects={len(self.projects)})"
