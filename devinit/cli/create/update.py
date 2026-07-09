from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

def updater(generator, context, name, output):
    gen = generator.generate(name, output, context)

    total = next(gen)

    
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("Starting Generator", total=total)
        for event in gen:
            progress.update(task, description=event)
            progress.advance(task)

