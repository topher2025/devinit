# devinit

`devinit` is a project scaffolding tool for creating starter app layouts from reusable templates. Instead of manually creating folders, config files, and starter code each time, you can generate a project in a single command and then start building on top of it.


## Install


### Install from the source code

From a local checkout of this repository:

```bash
cd /path/to/devinit
python -m pip install -e .
```

If you use `uv`:

```bash
cd /path/to/devinit
uv pip install -e .
```

After installation, run:

```bash
devinit --help
```

## What `devinit` is for

`devinit` helps you do two main things:

1. Set project defaults once with `devinit config`
2. Generate a new starter project with `devinit create`

That means you can keep common preferences like default output path, Git setup, and Docker flags all in one place and reuse them across future projects.

## Configure defaults with `devinit config`

The config commands edit your global devinit config file. You do not need to include the full nested path in most cases; `devinit` resolves keys automatically unless the path is ambiguous.

### Open the config file directly

```bash
devinit config edit
```

This opens the configuration file in your default editor so you can tweak values like the default project path, license, Git settings, and language/template defaults.

### Set a config value

```bash
devinit config set docker true
```

This changes the default `docker` setting, which is the same as setting:

```toml
[defaults]
docker = true
```

You can also use the dotted form:

```bash
devinit config set python.version 3.13
```

And because the config supports both `.` and `/` separators, this is equivalent:

```bash
devinit config set python/version 3.13
```

It also supports nested project-type keys like these:

```bash
devinit config set python.flask.docker true
devinit config set flask/docker true
```

Those resolve to the same setting.

### Get a config value

```bash
devinit config get docker
```

```bash
devinit config get python.version
```

### Remove a setting

```bash
devinit config unset docker
```

### Reset config

```bash
devinit config reset
```

### Example config

```toml
[defaults]
path = "~/code"
git = true
docker = false
license = "MIT"

[python]
version = "3.13"
pm = "uv"

[python.flask]
docker = true
```

You can think of the config as a reusable defaults layer for future project creation.

## Create a project with `devinit create`

The `create` command scaffolds a project from a template. The current templates are mostly Python-based, but the workflow is still a general project generator.

### Basic usage

```bash
devinit create python flask my_app
```

This generates a new Flask project named `my_app` using the default output path and config values.

### Override the target directory

```bash
devinit create python flask my_app --path ~/code
```

### Common options

```bash
devinit create python flask my_app \
  --path ~/code \
  --entry main \
  --git \
  --docker \
  --version 3.13 \
  --github \
  --public \
  --license MIT
```

Common flags include:

- `--path`: output directory for the new project
- `--entry`: entry filename or module name
- `--git / --no-git`: initialize a Git repository
- `--docker / --no-docker`: include Docker support
- `--version`: language version to use
- `--github / --no-github`: create a GitHub repo after generation
- `--public / --private`: repo visibility when GitHub is enabled
- `--license`: project license

## Typical workflow

A normal workflow looks like this:

```bash
devinit config set path ~/code
devinit config set git true
devinit config set python.version 3.13
devinit config set python.flask.docker true
devinit create python flask api-service --path ~/code
```

That sets your defaults once and then creates a project from them when you need a new app.

## Quick reference

```bash
devinit --help
devinit config --help
devinit create --help
devinit create python flask --help
```

## Notes

- `devinit` is meant to make project setup faster, not to replace your normal development workflow.
- Global config values are useful for standard defaults, while per-command flags still let you override them for a single project.
- `devinit` and all templates ship with defaults, so even if there are no user-specified config values, there will be defaults automatically applied.

For information on authoring custom templates, see [docs/creating-custom-templates.md](docs/creating-custom-templates.md).
