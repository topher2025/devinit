from rich.console import Console, Group
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text


LEVEL_STYLES = {
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red",
}

console = Console()


def updater(generator, context, name, output):
    total = generator.cnt(context)
    gen = generator.generate(name, output, context)

    log = []

    progress = Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
    )

    task = progress.add_task("Generating project...", total=total)

    with Live(
        Group(*log, progress),
        console=console,
        refresh_per_second=10,
    ) as live:

        for event in gen:
            level = event["level"].lower()

            line = Text.assemble(
                (
                    f"{level.upper():<8}",
                    LEVEL_STYLES.get(level, "white"),
                ),
                (" "),
                (f"{event['category']:<12}", "bold blue"),
                (" "),
                event["description"],
            )

            log.append(line)

            progress.update(
                task,
                advance=1,
                description="Generating Project...",
            )

            # Rebuild the layout with the new log line.
            live.update(Group(*log, progress))

    console.print("\n[green]✓ Project generated successfully![/green]")