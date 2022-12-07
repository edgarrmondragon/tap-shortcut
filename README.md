<div align="center">

# tap-shortcut

<div>
  <a href="https://results.pre-commit.ci/latest/github/edgarrmondragon/tap-shortcut/main">
    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/edgarrmondragon/tap-shortcut/main.svg"/>
  </a>
  <a href="https://github.com/edgarrmondragon/tap-shortcut/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/edgarrmondragon/tap-shortcut"/>
  </a>
</div>

Singer tap for Shortcut. Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

</div>

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`

## Settings

| Setting | Required | Default | Description    |
|:--------|:--------:|:-------:|:---------------|
| token   | True     | None    | Shortcut Token |

A full list of supported settings and capabilities is available by running: `tap-shortcut --about`

### Source Authentication and Authorization

See https://developer.shortcut.com/api/rest/v3#Authentication.

## Usage

You can easily run `tap-shortcut` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-shortcut --version
tap-shortcut --help
tap-shortcut --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-shortcut` CLI interface directly using `poetry run`:

```bash
poetry run tap-shortcut --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-shortcut
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-shortcut --version
# OR run a test `elt` pipeline:
meltano elt tap-shortcut target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
