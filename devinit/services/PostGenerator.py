from devinit.services.git import Git
from devinit.services.github import GitHub
from devinit.services.dependencies import Dependencies


class PostGenerator:
    @classmethod
    def run(cls, context: dict):
        if context["git"] or context["github"]:
            git = Git(context["path"])
            if git:
                git.init()
                git.add(".")
                git.commit("Initial Commit")
                yield {"level": "INFO", "category": "Git", "description": "Initialized Git"}
            else:
                yield {"level": "WARNING", "category": "Git", "description": "Failed to find git"}
        if context["github"]:
            yield {"level": "WARNING", "category": "GitHub", "description": "GitHub operations aren't supported yet"}
    

    @classmethod
    def cnt(cls, context:dict):
        c = 0

        if context["git"] or context["github"]: c+=1
        if context["github"]: c+=1

        return c