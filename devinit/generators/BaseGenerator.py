from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class BaseGenerator:
    template_name: str

    @classmethod
    def get_template_root(cls) -> Path:
        return (
            Path(__file__).parent.parent
            / "templates"
            / cls.template_name
        )
    

    @staticmethod
    def _load_env(template_dir):
        return Environment(
            loader=FileSystemLoader(template_dir),
            keep_trailing_newline=True,
            block_start_string="{{%",
            block_end_string="%}}",
            variable_start_string="{{{",
            variable_end_string="}}}",
            comment_start_string="{{#",
            comment_end_string="#}}",
        )

    @classmethod
    def render_template_dir(
        cls,
        template_dir: Path,
        output_dir: Path,
        context: dict,
    ):
        env = cls._load_env(template_dir)

        for source_path in template_dir.rglob("*"):
            if source_path.is_dir():
                continue

            # Path inside template directory
            relative = source_path.relative_to(template_dir)

            # Allow dynamic filenames/folders
            rendered_relative = Path(
                env.from_string(relative.as_posix())
                .render(**context)
            )

            if source_path.suffix == ".j2":
                output_path = output_dir / rendered_relative.with_suffix("")

                # IMPORTANT:
                # Use original relative path to find template
                template = env.get_template(relative.as_posix())

                content = template.render(**context)

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                output_path.write_text(
                    content,
                    encoding="utf-8",
                )

            else:
                output_path = output_dir / rendered_relative

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                output_path.write_bytes(
                    source_path.read_bytes()
                )


    @classmethod
    def render_license(cls, context: dict):
        if context["license"] == "":
            return
        output_path = context["path"] / "LICENSE"

        if context["license"].upper() == "MIT":
            template_path = "MIT.j2"
        else:
            return
        
        env = cls._load_env(
            Path(__file__).parent.parent / "templates" / "license"
        )
        template = env.get_template(template_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            template.render(**context),
            encoding="utf-8"
        )
            