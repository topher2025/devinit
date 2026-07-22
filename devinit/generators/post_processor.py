from devinit.services import *


class PostProcessor:
    @staticmethod
    def _supported(ctx: dict) -> dict:
        return  {
            "git": Git(ctx["path"]).build_git,
            "github": GitHub().build_github
        }

    def __init__(self, steps: list[str] = [], supported: dict = {}) -> None:
        self.steps = steps
        self.SUPPORTED = supported

    def process(self) -> None:
        for step in self.steps:
            self.SUPPORTED[step]()
            
        return
    
    @classmethod
    def from_ctx(cls, ctx: dict) -> PostProcessor:
        supported = cls._supported(ctx)
        steps: list[str] = []
        
        for step in supported:
            if step in ctx:
                steps.append(step)

        return cls(steps, supported)
