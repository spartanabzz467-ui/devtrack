"""
DevTrack CLI — Developer Project Management Tool
Entry point: python main.py <command> [options]
"""

import argparse
import sys
from utils.display import print_banner
from cli.commands import (
    cmd_add_user, cmd_list_users,
    cmd_add_project, cmd_list_projects,
    cmd_add_task, cmd_list_tasks, cmd_complete_task,
    cmd_filter_tasks,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devtrack",
        description="DevTrack CLI — Manage users, projects, and tasks from your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add-user --name "Alex"
  python main.py add-project --user "Alex" --title "CLI Tool" --deadline "2025-12-31"
  python main.py add-task --project "CLI Tool" --title "Implement argparse"
  python main.py complete-task --project "CLI Tool" --title "Implement argparse"
  python main.py list-tasks --project "CLI Tool"
  python main.py filter-tasks --status pending
        """,
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # ── add-user ───────────────────────────────────────────────────────────────
    p_add_user = subparsers.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name", required=True, help="User's full name")
    p_add_user.add_argument("--email", help="User's email address (optional)")
    p_add_user.set_defaults(func=cmd_add_user)

    # ── list-users ─────────────────────────────────────────────────────────────
    p_list_users = subparsers.add_parser("list-users", help="List all users")
    p_list_users.set_defaults(func=cmd_list_users)

    # ── add-project ────────────────────────────────────────────────────────────
    p_add_project = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_project.add_argument("--user", required=True, help="Name of the user")
    p_add_project.add_argument("--title", required=True, help="Project title")
    p_add_project.add_argument("--description", help="Short project description (optional)")
    p_add_project.add_argument("--deadline", help="Deadline date e.g. 2025-12-31 (optional)")
    p_add_project.set_defaults(func=cmd_add_project)

    # ── list-projects ──────────────────────────────────────────────────────────
    p_list_projects = subparsers.add_parser("list-projects", help="List all projects for a user")
    p_list_projects.add_argument("--user", required=True, help="Name of the user")
    p_list_projects.set_defaults(func=cmd_list_projects)

    # ── add-task ───────────────────────────────────────────────────────────────
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--description", help="Short task description (optional)")
    p_add_task.set_defaults(func=cmd_add_task)

    # ── list-tasks ─────────────────────────────────────────────────────────────
    p_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks for a project")
    p_list_tasks.add_argument("--project", required=True, help="Project title")
    p_list_tasks.set_defaults(func=cmd_list_tasks)

    # ── complete-task ──────────────────────────────────────────────────────────
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--project", required=True, help="Project title")
    p_complete.add_argument("--title", required=True, help="Task title to complete")
    p_complete.set_defaults(func=cmd_complete_task)

    # ── filter-tasks ───────────────────────────────────────────────────────────
    p_filter = subparsers.add_parser("filter-tasks", help="Filter tasks by status across all projects")
    p_filter.add_argument("--status", required=True, choices=["pending", "completed", "all"],
                          help="Filter by: pending, completed, or all")
    p_filter.set_defaults(func=cmd_filter_tasks)

    return parser


def main():
    print_banner()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
