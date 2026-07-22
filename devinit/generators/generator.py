from pathlib import Path

from devinit.config.resolver import Resolver
from devinit.generators.post_processor import PostProcessor
from devinit.generators.template import Template
from devinit.generators.manifest import Manifest
from devinit.generators.pack_resolver import PackResolver


class Generator:
    def __init__(self, manifest: Manifest, context: dict, post_processor: PostProcessor = PostProcessor(), template_path: Path | None = None) -> None:
        self.context = context
        if template_path:
            self.template_path = template_path
            self.shipped = False
        else: self.shipped = True
        self.post_processor = post_processor
        self.manifest = manifest
        


    @classmethod
    def from_list(cls, template_path: Path, name:str, context:list, post_processor: PostProcessor | None = None) -> Generator:
        manifest = Manifest(template_path / "manifest.toml")
        cxt = Resolver.resolve(context, manifest, project=name)
        if post_processor is None: post_processor = PostProcessor.from_ctx(cxt)
        return cls(manifest, cxt, post_processor)
    

    def generate(self) -> None:
        pack_resolver = PackResolver(self.manifest, self.context, shipped=self.shipped)
        pack_resolver.resolve()
        self.post_processor.process()



    