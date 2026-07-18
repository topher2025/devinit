from devinit.generators.manifest import Manifest

class PackResolver:
    def __init__(self, manifest: Manifest, ctx: dict) -> None:
        self.manifest = manifest
        self.packs = []
        self.ctx = ctx

    def resolve(self):
        self.select_packs()
        for pack in self.packs:
            self.render_pack(pack)



    def select_packs(self) -> list:
        for arg in self.ctx:
            if hasattr(self.manifest.arguments, arg):
                argument = getattr(self.manifest.arguments, arg)
                if hasattr(argument, "pack"):
                    self.packs.append(getattr(argument, "pack"))
                elif hasattr(argument.choices, self.ctx[arg]):
                    choice = getattr(argument.choices, self.ctx[arg])
                    if hasattr(choice, "pack"):
                        self.packs.append(getattr(argument, "pack"))
                
        return self.packs
        
    
    def render_pack(self, pack):
        pass


