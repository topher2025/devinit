from pathlib import Path

from devinit.config.resolver import Resolver
from devinit.generators.post_processor import PostProcessor
from devinit.generators.template import Template
from devinit.generators.manifest import Manifest


class Generator:
    def __init__(self, template: Template, context: dict, post_processor: PostProcessor = PostProcessor()) -> None:
        self.template = template
        self.context = context
        self.post_processor = post_processor
        


    @classmethod
    def from_list(cls, template_path: Path, name:str, context:list, post_processor: PostProcessor = PostProcessor()) -> Generator:
        template = Template(template_path)
        manifest = Manifest(template_path / "manifest.toml")
        cxt = Resolver.resolve(context, manifest)
        return cls(template, cxt, post_processor)
    

    def generate(self) -> None:
        pass


    