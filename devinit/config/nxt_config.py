from .loaders import load_config_document, load_defaults_config_document, USER_CONFIG
import tomlkit
from importlib.resources import files
from pathlib import Path
import shutil
from functools import wraps
import os
import sys
import subprocess
from devinit.utils.xp import open_file
from devinit.exceptions import ConfigNoValidPath



def public(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._write_defaults()
        self._refresh_prefs()
        result = func(self, *args, **kwargs)
        return result
    return wrapper



class Config:
    def __init__(self):
        self._write_defaults()
        self.defaults = load_defaults_config_document()
        self.prefs = load_config_document()

    @classmethod
    def _checkey(cls, k: str, d: dict, c: list, u=False):
        l = []
        if k in d:
            u=True
        if u:
            l.append(c + [k])

        for kk, vv in d.items():
            if isinstance(vv, dict):
                l.extend(cls._checkey(k, vv, c + [kk], u))
        
        return l

    @staticmethod
    def _is_subset(alpha, beta):
        al, bl = len(alpha), len(beta)
        if bl == 0:
            return True
        if bl > al:
            return False

        for i in range(al - bl + 1):
            if alpha[i:i+bl] == beta:
                return True
        return False


    def _refresh_prefs(self):
        self.prefs = load_config_document()

    def _overwrite_prefs(self):
        with USER_CONFIG.open("w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(self.prefs))

    @classmethod
    def _write_defaults(cls):
        default = files("devinit.config") / "config.toml"
        if not USER_CONFIG.exists():
            USER_CONFIG.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(Path(str(default)), USER_CONFIG)


    def _resolve_path(self, arg: list) -> list:
        matches: list[list[str]] = []
        valid = []
        if len(arg) == 0:
            pass
        elif len(arg) == 1:
            if arg[0] in self.defaults:
                matches.append([arg[0]])
            elif arg[0] in self.defaults["defaults"]:
                matches.append(["defaults", arg[0]])
        else:
            matches.extend(self._checkey(arg[-1], self.defaults, [], u=arg[-1] in self.defaults["defaults"]))

        for l in matches:
            if self._is_subset(l, arg):
                valid.append(l)
        
        if len(valid) != 1:
            raise ConfigNoValidPath
        return valid[0]



    @public
    def set_value(self, k:list, v:str):
        if len(k) == 1 and k[0] == "fullname":
            self.prefs["fullname"] = v
        else:
            key = self._resolve_path(k)
            cur = self.prefs
            for w in key[:-1]:
                cur = cur.setdefault(w, {})
            cur[key[-1]] = v
        self._overwrite_prefs()

    @public
    def get_value(self, k:list):
        key = self._resolve_path(k)
        cur = self.prefs
        for w in key[:-1]:
            cur = cur.setdefault(w, {})
        return cur[key[-1]]

    @public
    def unset_value(self, k:list):
        key = self._resolve_path(k)

        cur = self.prefs
        for w in key[:-1]:
            cur = cur.setdefault(w, {})
        cur[key[-1]] = None
        self._overwrite_prefs()

    @public
    def reset(self):
        self.prefs = {}
        self._overwrite_prefs()


    @public
    def list(self, k:list=[]):
        key = self._resolve_path(k)
        
        cur = self.prefs
        for w in key[:-1]:
            cur = cur.setdefault(w, {})
        return cur

    @public
    def edit(self):
        open_file(USER_CONFIG)