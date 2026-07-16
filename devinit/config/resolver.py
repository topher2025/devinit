from devinit.generators.manifest import Manifest
from devinit.config.loaders import *

class Resolver:
    @classmethod
    def resolve(cls, context: dict | list, manifest: Manifest) -> dict:
        if isinstance(context, list):
            cli = cls.list_to_dict(context)
        else:
            cli = context

        defaults = load_defaults_config()
        prefs = load_config()

        ctx = manifest.to_dict()
        ctx = cls.merge(defaults, ctx)
        ctx = cls.merge(prefs, ctx)
        ctx = cls.merge(cli, ctx)

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