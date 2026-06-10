"""CLI command handlers — one function per subcommand."""

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_users, save_users, find_user
from utils import display


# ── User commands ──────────────────────────────────────────────────────────────

def cmd_add_user(args):
    users = load_users()
    if find_user(users, args.name):
        display.print_error(f"User '{args.name}' already exists.")
        return
    user = User(name=args.name, email=args.email or "")
    user.user_id = len(users) + 1
    users.append(user)
    save_users(users)
    display.print_success(f"User '{args.name}' created (ID: {user.user_id}).")


def cmd_list_users(args):
    users = load_users()
    display.print_users(users)


# ── Project commands ───────────────────────────────────────────────────────────

def cmd_add_project(args):
    users = load_users()
    user = find_user(users, args.user)
    if not user:
        display.print_error(f"User '{args.user}' not found. Create them first with add-user.")
        return
    if user.get_project(args.title):
        display.print_error(f"Project '{args.title}' already exists for {args.user}.")
        return
    project = Project(
        title=args.title,
        description=args.description or "",
        deadline=args.deadline or None,
    )
    user.add_project(project)
    save_users(users)
    display.print_success(f"Project '{args.title}' added to {args.user} (ID: {project.project_id}).")


def cmd_list_projects(args):
    users = load_users()
    user = find_user(users, args.user)
    if not user:
        display.print_error(f"User '{args.user}' not found.")
        return
    display.print_projects(user)


# ── Task commands ──────────────────────────────────────────────────────────────

def cmd_add_task(args):
    users = load_users()
    # Find which user owns this project
    owner = None
    project = None
    for u in users:
        p = u.get_project(args.project)
        if p:
            owner = u
            project = p
            break
    if not project:
        display.print_error(f"Project '{args.project}' not found. Create it first with add-project.")
        return
    if project.get_task(args.title):
        display.print_error(f"Task '{args.title}' already exists in project '{args.project}'.")
        return
    task = Task(title=args.title, description=args.description or "")
    project.add_task(task)
    save_users(users)
    display.print_success(f"Task '{args.title}' added to project '{args.project}' (ID: {task.task_id}).")


def cmd_list_tasks(args):
    users = load_users()
    for u in users:
        project = u.get_project(args.project)
        if project:
            display.print_tasks(project)
            return
    display.print_error(f"Project '{args.project}' not found.")


def cmd_complete_task(args):
    users = load_users()
    for u in users:
        project = u.get_project(args.project)
        if project:
            task = project.get_task(args.title)
            if not task:
                display.print_error(f"Task '{args.title}' not found in project '{args.project}'.")
                return
            if task.completed:
                display.print_info(f"Task '{args.title}' is already marked complete.")
                return
            task.complete()
            save_users(users)
            display.print_success(f"Task '{args.title}' marked as complete! 🎉")
            display.print_info(f"Project progress: {project.progress} ({project.completed_tasks}/{project.total_tasks} tasks done)")
            return
    display.print_error(f"Project '{args.project}' not found.")


# ── Filter command ─────────────────────────────────────────────────────────────

def cmd_filter_tasks(args):
    """Filter tasks across all projects by status."""
    users = load_users()
    status_filter = args.status.lower()  # 'pending', 'completed', or 'all'

    from rich.table import Table
    from rich.console import Console
    from rich import box

    console = Console()
    table = Table(title=f"🔍 Tasks — Filter: {status_filter.title()}", box=box.ROUNDED, show_lines=True)
    table.add_column("User", style="cyan")
    table.add_column("Project", style="bold")
    table.add_column("Task")
    table.add_column("Status", justify="center")

    found = False
    for u in users:
        for p in u.projects:
            for t in p.tasks:
                if status_filter == "all":
                    match = True
                elif status_filter == "completed":
                    match = t.completed
                else:  # pending
                    match = not t.completed

                if match:
                    found = True
                    status = "[green]✓ Done[/green]" if t.completed else "[yellow]○ Pending[/yellow]"
                    table.add_row(u.name, p.title, t.title, status)

    if not found:
        display.print_info(f"No {status_filter} tasks found.")
    else:
        console.print(table)
