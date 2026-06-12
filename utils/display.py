"""Display utilities — pretty-print tables using the `rich` library."""

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text
from models.user import User
from models.project import Project

console = Console()


def print_users(users: list[User]):
    """Print all users in a formatted table."""
    if not users:
        console.print("[yellow]No users found. Add one with: add-user --name 'Name'[/yellow]")
        return

    table = Table(title=" All Users", box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold cyan")
    table.add_column("Email", style="green")
    table.add_column("Projects", justify="center")
    table.add_column("Created", style="dim")

    for u in users:
        table.add_row(
            str(u.user_id),
            u.name,
            u.email or "—",
            str(len(u.projects)),
            u.created_at,
        )
    console.print(table)


def print_projects(user: User):
    """Print all projects for a user."""
    if not user.projects:
        console.print(f"[yellow]No projects for {user.name}. Add one with: add-project --user '{user.name}' --title 'Title'[/yellow]")
        return

    table = Table(title=f" Projects for {user.name}", box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="bold cyan")
    table.add_column("Description")
    table.add_column("Deadline", style="magenta")
    table.add_column("Progress", justify="center")
    table.add_column("Tasks", justify="center")

    for p in user.projects:
        pct = int(p.progress.replace("%", ""))
        color = "green" if pct == 100 else "yellow" if pct > 0 else "red"
        table.add_row(
            str(p.project_id),
            p.title,
            p.description or "—",
            p.deadline or "—",
            f"[{color}]{p.progress}[/{color}]",
            f"{p.completed_tasks}/{p.total_tasks}",
        )
    console.print(table)


def print_tasks(project: Project):
    """Print all tasks for a project."""
    if not project.tasks:
        console.print(f"[yellow]No tasks for '{project.title}'. Add one with: add-task --project '{project.title}' --title 'Task'[/yellow]")
        return

    table = Table(title=f" Tasks for '{project.title}'", box=box.ROUNDED, show_lines=True)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="bold")
    table.add_column("Description")
    table.add_column("Status", justify="center")
    table.add_column("Created", style="dim")

    for t in project.tasks:
        status = "[green]✓ Done[/green]" if t.completed else "[yellow]○ Pending[/yellow]"
        table.add_row(
            str(t.task_id),
            t.title,
            t.description or "—",
            status,
            t.created_at,
        )
    console.print(table)


def print_success(msg: str):
    console.print(f"[bold green]✓[/bold green] {msg}")


def print_error(msg: str):
    console.print(f"[bold red]✗ Error:[/bold red] {msg}")


def print_info(msg: str):
    console.print(f"[bold blue]ℹ[/bold blue] {msg}")


def print_banner():
    text = Text("DevTrack CLI", style="bold cyan", justify="center")
    console.print(Panel(text, subtitle="[dim]Developer Project Management Tool[/dim]", box=box.DOUBLE))
