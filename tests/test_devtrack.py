"""
Tests for DevTrack CLI — covers models, storage, and CLI commands.
Run with: pytest tests/ -v
"""

import pytest
import os
import json
import tempfile
from unittest.mock import patch

from models.task import Task
from models.project import Project
from models.user import User


# ── Task tests ─────────────────────────────────────────────────────────────────

class TestTask:
    def test_task_creation(self):
        task = Task(title="Write tests", description="Add pytest coverage")
        assert task.title == "Write tests"
        assert task.description == "Add pytest coverage"
        assert task.completed is False

    def test_task_complete(self):
        task = Task(title="Deploy app")
        task.complete()
        assert task.completed is True

    def test_task_serialization(self):
        task = Task(title="Review PR", description="Check the diff", task_id=1)
        data = task.to_dict()
        assert data["title"] == "Review PR"
        assert data["completed"] is False
        assert data["task_id"] == 1

    def test_task_deserialization(self):
        data = {"title": "Fix bug", "description": "Null pointer", "completed": True,
                "created_at": "2025-01-01 10:00", "task_id": 2}
        task = Task.from_dict(data)
        assert task.title == "Fix bug"
        assert task.completed is True
        assert task.task_id == 2

    def test_task_repr(self):
        task = Task(title="Do something")
        assert "Do something" in repr(task)


# ── Project tests ──────────────────────────────────────────────────────────────

class TestProject:
    def test_project_creation(self):
        project = Project(title="API Redesign", deadline="2025-06-30")
        assert project.title == "API Redesign"
        assert project.deadline == "2025-06-30"
        assert project.tasks == []

    def test_add_task(self):
        project = Project(title="My Project")
        task = Task(title="Task A")
        project.add_task(task)
        assert len(project.tasks) == 1
        assert task.task_id == 1

    def test_get_task_by_title(self):
        project = Project(title="My Project")
        project.add_task(Task(title="Alpha"))
        result = project.get_task("alpha")  # case-insensitive
        assert result is not None
        assert result.title == "Alpha"

    def test_get_task_not_found(self):
        project = Project(title="My Project")
        assert project.get_task("Nonexistent") is None

    def test_progress_empty(self):
        project = Project(title="Empty")
        assert project.progress == "0%"

    def test_progress_partial(self):
        project = Project(title="Partial")
        t1 = Task(title="T1")
        t2 = Task(title="T2")
        project.add_task(t1)
        project.add_task(t2)
        t1.complete()
        assert project.progress == "50%"
        assert project.completed_tasks == 1

    def test_progress_full(self):
        project = Project(title="Done")
        t = Task(title="Only task")
        project.add_task(t)
        t.complete()
        assert project.progress == "100%"

    def test_project_serialization_roundtrip(self):
        project = Project(title="Roundtrip", description="Test", deadline="2025-12-31")
        task = Task(title="Step 1")
        project.add_task(task)
        data = project.to_dict()
        restored = Project.from_dict(data)
        assert restored.title == "Roundtrip"
        assert len(restored.tasks) == 1
        assert restored.tasks[0].title == "Step 1"


# ── User tests ─────────────────────────────────────────────────────────────────

class TestUser:
    def test_user_creation(self):
        user = User(name="Alex", email="alex@test.com")
        assert user.name == "Alex"
        assert user.email == "alex@test.com"
        assert user.projects == []

    def test_add_project(self):
        user = User(name="Sam")
        project = Project(title="DevTrack")
        user.add_project(project)
        assert len(user.projects) == 1
        assert project.project_id == 1

    def test_get_project_case_insensitive(self):
        user = User(name="Jordan")
        user.add_project(Project(title="Backend API"))
        result = user.get_project("backend api")
        assert result is not None

    def test_get_project_not_found(self):
        user = User(name="Casey")
        assert user.get_project("Ghost Project") is None

    def test_user_serialization_roundtrip(self):
        user = User(name="River", email="river@test.com", user_id=1)
        project = Project(title="Cloud Migration")
        project.add_task(Task(title="Audit current infra"))
        user.add_project(project)

        data = user.to_dict()
        restored = User.from_dict(data)

        assert restored.name == "River"
        assert len(restored.projects) == 1
        assert restored.projects[0].title == "Cloud Migration"
        assert len(restored.projects[0].tasks) == 1


# ── Storage tests ──────────────────────────────────────────────────────────────

class TestStorage:
    def test_save_and_load(self, tmp_path):
        """Test that users survive a save/load cycle."""
        from utils import storage
        original_path = storage.DATA_FILE
        storage.DATA_FILE = str(tmp_path / "test_data.json")

        try:
            user = User(name="Tester", email="t@t.com", user_id=1)
            project = Project(title="Test Project", project_id=1)
            project.add_task(Task(title="Do a thing", task_id=1))
            user.projects = [project]

            storage.save_users([user])
            loaded = storage.load_users()

            assert len(loaded) == 1
            assert loaded[0].name == "Tester"
            assert loaded[0].projects[0].title == "Test Project"
            assert loaded[0].projects[0].tasks[0].title == "Do a thing"
        finally:
            storage.DATA_FILE = original_path

    def test_load_missing_file(self, tmp_path):
        from utils import storage
        original_path = storage.DATA_FILE
        storage.DATA_FILE = str(tmp_path / "nonexistent.json")
        try:
            result = storage.load_users()
            assert result == []
        finally:
            storage.DATA_FILE = original_path

    def test_find_user(self):
        from utils.storage import find_user
        users = [User(name="Alice"), User(name="Bob")]
        assert find_user(users, "alice") is not None
        assert find_user(users, "Charlie") is None
