from devinit.generators.manifest import Manifest
from devinit.config.loaders import *

class Resolver:
    @classmethod
    def resolve(cls, context: dict | list, manifest: Manifest, **kwargs) -> dict:
        if isinstance(context, list):
            cli = cls.list_to_dict(context)
        else:
            cli = context

        ctx = manifest.data
        
        defaults = load_defaults_config(lang=ctx["language"], framework=ctx["name"])
        prefs = load_config(lang=ctx["language"], framework=ctx["name"])

        ctx = cls.merge(defaults, ctx)
        ctx = cls.merge(prefs, ctx)
        ctx = cls.merge(cli, ctx)
        #ctx = cls._clean(ctx, manifest)
        ctx = cls._add_reqs(ctx, kwargs)
        print(ctx)
        return ctx
    

    @staticmethod
    def list_to_dict(ctx: list) -> dict:
        d = {}
        k ,v = None, None

        for item in ctx:
            if item.startswith("--"):
                if k:
                    d[k] = True
                if "=" not in item:
                    k = item[2:]
                else:
                    k, v = item.split("=")
                    k = k[2:]
            elif k:
                if item != "=":
                    v = item
            
            if k is not None and v is not None:
                d[k] = v
                k, v = None, None

        if k:
            d[k] = True

        return d

    @staticmethod
    def merge(alpha: dict, beta: dict) -> dict:
        merged = {}

        for key, value in alpha.items():
            merged[key] = value
        for key, value in beta.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key] = Resolver.merge(merged[key], beta[key])
                elif isinstance(value, list) and isinstance(merged[key], list):
                    merged[key] = Resolver._merge_list(merged[key], value)
            if key not in merged:
                merged[key] = value

        return merged
    
    @staticmethod
    def _merge_list(alpha: list, beta: list) -> list:
        merged = []

        for value in alpha:
            merged.append(value)
        for value in beta:
            merged.append(value)

        return merged
    
    @classmethod
    def _clean(cls, ctx: dict, manifest: Manifest) -> dict:
        keys = []
        new_ctx = {}
        keys.extend(manifest.context)
        keys.extend(manifest.options)
        print(keys)
        print()
        print(ctx)

        for k, v in ctx.items():
            if k in keys:
                new_ctx[k] = v
                print(f"ctx \n{new_ctx}]\n")
            if isinstance(v, list):
                for item in v:
                    if item in keys:
                        new_ctx[k] = item

        return new_ctx
    
    @staticmethod
    def _add_reqs(ctx:dict, inputs:dict={}) -> dict:
        reqs = {}
        reqs_list = ["src", "project"]

        for k,v in ctx.items():
            reqs[k] = v

        for req in reqs_list:
            if req in ctx: reqs[req] = ctx[req]
            elif req in inputs: reqs[req] = inputs[req]
            else: reqs[req] = ""

        return reqs
    

