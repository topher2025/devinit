from devinit.generators.manifest import Manifest
from importlib import resources
from pathlib import Path
from importlib.resources.abc import Traversable
from jinja2 import Environment
from datetime import datetime
from typing import Iterator
import shutil


class PackResolver:
    SHIPPED_PACKS: list = ["license", "git"]

    def __init__(self, manifest: Manifest, ctx: dict, shipped: bool = True) -> None:
        self.manifest = manifest
        self.packs = []
        self.ctx = ctx
        self.shipped = shipped
        self.env = self._create_environment()


    def _create_environment(self) -> Environment:
        env = Environment(
            variable_start_string="{{{",
            variable_end_string="}}}",
            block_start_string="{{%",
            block_end_string="%}}",
            trim_blocks=True,
            lstrip_blocks=True,
        )

        env.globals["year"] = datetime.now().year
        env.filters["snake"] = self._snake_case

        return env
    
    @staticmethod
    def _snake_case(value):
        return value.replace("-", "_")

    def resolve(self) -> None:
        self.select_packs()
        print(self.packs)
        for pack in self.packs:
            self.render_pack(pack)

    def _get_pack_path(self, pack: str) -> Path | Traversable:
        if self.shipped:
            return (
            resources.files("devinit.templates")
            .joinpath(self.manifest.language)
            .joinpath(self.manifest.name)
            .joinpath(pack)
        )
        
        return self.ctx["src"] / "packs" / pack
    
    def _walk(self, path: Path | Traversable, rel: Path = Path()) -> Iterator[tuple[Traversable, Path]]:
        for child in path.iterdir():
            child_rel = rel / child.name

            if child.is_dir():
                yield from self._walk(child, child_rel)
            else:
                yield child, child_rel


            

    def select_packs(self):
        groups = {}

        for name, value in self.ctx.items():
            if hasattr(self.manifest.arguments, name):
                argument = getattr(self.manifest.arguments, name)
            else: continue

            # standalone pack
            if hasattr(argument, "pack") and value:
                self.packs.append(argument.pack)

            # variant choice
            if hasattr(argument, "choices"):
                if hasattr(argument.choices, value):
                    choice = getattr(argument.choices, value)

                    if getattr(choice, "pack", ""):
                        self.packs.append(choice.pack)

            # grouped variants
            if hasattr(argument, "group") and value:
                groups.setdefault(argument.group, []).append(name)

        # resolve groups
        for group_name, variants in groups.items():
            key = ",".join(sorted(variants))

            group_cfg = getattr(self.manifest.groups, group_name)

            if hasattr(group_cfg, key):
                self.packs.append(getattr(group_cfg, key))

        return self.packs
            
    def render_pack(self, pack: str) -> None:
        pack_dir = self._get_pack_path(pack)

        for file, rel in self._walk(pack_dir):
            if file.is_file():
                self.render_file(file, pack_dir, rel)


    def render_file(self, source: Path | Traversable, pack_root: Path | Traversable, rel: Path) -> None:        
        destination = Path(self.ctx["path"]) / self.ctx["project"]
        if Path(source.name).suffix == ".j2":
            # Remove the .j2 extension
            destination /= rel.with_suffix("")

            template = self.env.from_string(source.read_text(encoding="utf-8"))
            rendered = template.render(self.ctx)

            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
        else:
            destination /= rel
            destination.parent.mkdir(parents=True, exist_ok=True)

            with source.open("rb") as src, destination.open("wb") as dst:
                shutil.copyfileobj(src, dst)
        print(destination)
        print(self.ctx["path"])