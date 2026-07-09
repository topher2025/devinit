from pathlib import Path

from devinit.generators.BaseGenerator import BaseGenerator
from devinit.services.PostGenerator import PostGenerator

class FlaskGenerator(BaseGenerator):
    template_name = "python/flask"

    @classmethod
    def generate(
        cls,
        project_name: str,
        output_dir: Path,
        context: dict,
    ):
        template_root = cls.get_template_root()
        packs = ["common"]

        if context["blueprints"]:
            packs.append("blueprints")
        if context["docker"]:
            packs.append("docker")
        if context["git"]:
            packs.append("git")
            
        yield len(packs) + PostGenerator.cnt(context)
        print(f"packs: {packs}")

        for pack in packs:
            cls.render_template_dir(template_root / pack, output_dir, context)
            yield(f"Rendered the '{pack}' pack")
        
        for message in PostGenerator.run(context):
            yield message