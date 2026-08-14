# Template public API: manifest and config

This document explains the public API template authors rely on when creating a new project template in `devinit`.

The key idea is simple:

- `manifest.toml` describes what the template is and which packs/options it exposes.
- `config.toml` (and the config module in `devinit/config`) provides default values and user preferences.
- The generator merges those values, resolves selected packs, and renders files from the template directory.

In other words, a new template is not just a directory of files. It is a contract that lives in a `manifest.toml` plus a set of pack directories and runtime config defaults.

---

## 1. The shape of a template

A template lives under a path like:

```text
devinit/templates/python/fastapi-web/
```

and typically contains:

- `manifest.toml` — the template definition
- `config.toml` — optional template-local examples or comments that describe defaults and expected settings
- one or more pack folders such as `api/`, `auth/jwt/`, `db/sqlite/`, `docker/`, etc.
- `.j2` templates that are rendered with Jinja

The important design rule is that the manifest is the source of truth for the template's public choices, while the config file acts as the default configuration layer that makes those choices usable in real projects.

---

## 2. The manifest contract

A template manifest is a TOML file like this:

```toml
name = "fastapi-web"
display_name = "FastAPI Application"
version = "1.0.0"
description = "A full FastAPI web application"
language = "python"

[requirements]
python = ">=3.12"

[args]
context = [
    "fullname",
    "year",
]
options = [
  "actions",
  "async",
  "auth",
  "database",
  "docker",
  "git",
  "github",
  "migrations",
  "orm",
  "pm",
]
```

The manifest is the template's public definition.

### Required metadata

A template should define fields such as:

- `name`: internal template identifier
- `language`: language family or stack such as `python`, `go`, or `node`
- `display_name`: human-readable title
- `version`: template version
- `description`: summary text

These fields describe what the template is and where it belongs in the template registry.

### Dependency definitions

The manifest can declare installable dependencies under `[dependencies.*]`:

```toml
[dependencies.auth.jwt]
packages = [
    "python-jose",
    "passlib[bcrypt]",
]

[dependencies.database.sqlite]
packages = [
    "aiosqlite",
]
```

This gives the template a structured dependency graph keyed by option or feature selection.

### Argument definitions

Templates expose their user-facing options through `[arguments.*]` entries. These are the public knobs that appear in the creation flow.

The most important thing to remember is that each argument should describe both:

1. the user-visible option
2. the pack or directory it should enable when selected

Example choice argument:

```toml
[arguments.database]
type = "choice"
description = "Database backend"
default = "sqlite"

[arguments.database.choices.mysql]
pack = "db/mysql"

[arguments.database.choices.none]
pack = ""

[arguments.database.choices.sqlite]
pack = "db/sqlite"
```

Example boolean argument:

```toml
[arguments.docker]
type = "boolean"
description = "Generate Docker support"
pack = "docker"
default = true
```



The `pack` field is important because it tells `devinit` which subdirectory to render.

### Grouped variants

Some templates need mutually exclusive or combinable structure modes. Example:

```toml
[arguments.router]
type = "variant"
group = "structure"
default = "none"

[arguments.web]
type = "variant"
group = "structure"
default = "none"

[groups.structure]
"" = "api"
router = "api-router"
web = "web"
"router,web" = "web-router"
```

This is how the system turns selected choices into actual file packs.

---

## 3. Config files for template authors

The config layer matters because template authors should not hardcode every possible value into their manifest. Instead, they should rely on a layered defaults model so users can set preferences once and reuse them.

The standard config file is:

```toml
# ~/.config/devinit/config.toml
```

This file is organized into sections such as:

- `[defaults]`
- `[python]`
- `[js]`
- `[java]`
- `[go]`
- etc.

Example:

```toml
[defaults]
path = "."
git = true
docker = false
license = "MIT"

[python]
version = "3.13"
pm = "uv"
```

This is the main public configuration contract for template authors because it tells users which defaults are supported and which values are expected.

### How to design config for a new template

When creating a template, think of the config as the standardized defaults layer that supports your template. If your template has:

- a language/runtime version
- a package manager
- a database choice
- an auth or service mode
- project path defaults

then those should be expressible in config as user-friendly settings.

A template should not invent ad hoc config values unless it truly needs them. The better pattern is to stay within the shared defaults structure and use the manifest to select which features are enabled.

### Good config conventions

- Keep names stable and general
- Prefer shared keys such as `python.version` and `pm`
- Use `defaults` for project-wide defaults
- Use language-specific sections only when the setting belongs to that language or framework
- Keep the values documented in comments or a local `config.toml` example file

For example, a Python template may expose:

```toml
[python]
version = "3.13"
pm = "uv"
```

while a framework-specific template may rely on a manifest option such as:

```toml
[arguments.database]
type = "choice"
default = "sqlite"
```

rather than duplicating all of that in user config.

---

## 4. How the manifest and config work together

A template author should design the manifest and config together.

The pattern is:

- the manifest defines the features and options a user can choose
- the config defines the defaults those choices can inherit
- the template packs contain the files for each feature

As an authoring rule, each user-facing option should be reflected in a coherent config/defaults story.

For example:

```toml
[arguments.docker]
type = "boolean"
pack = "docker"
default = true
```

goes naturally with config defaults such as:

```toml
[defaults]
docker = true
```

Similarly, a choice option like:

```toml
[arguments.database]
type = "choice"
default = "sqlite"
```

can match config expectations like:

```toml
[python]
# shared defaults
```

or a template-local note explaining which database values are valid.

This separation keeps template configuration readable and predictable.

---

## 5. What a new template author must provide

To create a new template, a developer typically does the following:

### Step 1: create the template directory

```text
devinit/templates/python/my-template/
```

Inside it, create a `manifest.toml` and the pack directories that will be rendered.

### Step 2: define the template contract in the manifest

Your manifest should declare:

- the template name and language
- available options
- any dependencies and config values
- which subpacks correspond to each option
- any grouped variants needed for a structure decision

### Step 3: add the actual pack files

Files are organized under subdirectories, for example:

```text
devinit/templates/python/my-template/
  manifest.toml
  api/
    pyproject.toml.j2
    app/
      __init__.py
  docker/
    Dockerfile.j2
```

The key idea is that each feature pack should correspond to a manifest option or a structural choice.

### Step 4: use context values in templates

The pack renderer creates a Jinja environment with custom delimiters:

```python
env = Environment(
    variable_start_string="{{{",
    variable_end_string="}}}",
    block_start_string="{{%",
    block_end_string="%}}",
    trim_blocks=True,
    lstrip_blocks=True,
)
```

This means template files can reference variables like:

```jinja2
project_name = "{{{ project }}}"
author = "{{{ fullname }}}"
```

Use names that are meaningful, stable, and already implied by the template's public API.

### Step 5: wire the option to the pack

If a boolean or choice option should include files, set its `pack` field in the manifest. For example:

```toml
[arguments.docker]
type = "boolean"
pack = "docker"
default = true
```

This keeps the mapping between the public option and the generated files explicit.

---

## 6. Practical authoring guidance

When building a new template, treat the manifest as the public API and the config as the shared defaults API.

Good template conventions:

- keep `manifest.toml` declarative and explicit
- use `pack` fields to associate options with directories
- keep template values aligned with user-level config keys
- prefer small, composable packs over one large monolith
- keep the option names readable and feature-focused
- document defaults in comments or a `config.toml` example
- avoid duplicating config values that already exist at the global level

A template that follows this pattern will work naturally with the existing generator, config loader, and CLI flows.

---

## 7. Summary

The public API for template authoring is a combination of:

- `manifest.toml`: the template contract and public options
- config defaults: the reusable defaults layer for real projects
- template packs: the concrete files for each feature or mode

If you are making a new template, the most important design questions are:

1. What options do users choose?
2. What defaults should those options inherit?
3. Which pack directories does each option enable?
4. What does the resulting project structure look like?

Those four questions define the template's public API in a way that is clear to both users and future template authors.
