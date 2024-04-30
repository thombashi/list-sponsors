# **list-sponsors**


## Summary
A CLI tool to list GitHub sponsors of a user/organization with a specified format.


## Installation

```
pip install list-sponsors
```


## Command help

```
usage: list-sponsors [-h] [-V] [--name GITHUB_LOGIN_NAME] [--token GITHUB_TOKEN] [--format {md,markdown,rst,restructuredtext,html}] [--avatar-size SIZE] [--debug | --quiet]

A CLI tool to list GitHub sponsors of a user/organization with specified format.

Require a GitHub personal access token either by
--token option or GITHUB_TOKEN environment variable.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  --name GITHUB_LOGIN_NAME
                        login name of a GitHub user. if this option is not specified, use the login name of the GitHub personal access token.
  --token GITHUB_TOKEN  GitHub personal access token.
  --format {md,markdown,rst,restructuredtext,html}
                        defaults to markdown.
  --avatar-size SIZE    avatar size will be SIZExSIZE defaults to 48.
  --debug               for debug print.
  --quiet               suppress execution log messages.

Issue tracker: https://github.com/thombashi/list-sponsors/issues
```

## Usage
List your sponsors:

```
export GITHUB_TOKEN=<PAT>
list-sponsors
```

### Output: raw markdown
```md
[![onetime: Dmitry Belyaev (b4tman)](https://avatars.githubusercontent.com/u/3658062?s=48&v=4 "onetime: Dmitry Belyaev (b4tman)")](https://github.com/b4tman)
[![Charles Becker (chasbecker)](https://avatars.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4 "Charles Becker (chasbecker)")](https://github.com/chasbecker)
[![onetime: Arturi0](https://avatars.githubusercontent.com/u/46711571?s=48&u=57687c0e02d5d6e8eeaf9177f7b7af4c9f275eb5&v=4 "onetime: Arturi0")](https://github.com/Arturi0)
```

### Output: rendered
[![onetime: Dmitry Belyaev (b4tman)](https://avatars.githubusercontent.com/u/3658062?s=48&v=4 "onetime: Dmitry Belyaev (b4tman)")](https://github.com/b4tman)
[![Charles Becker (chasbecker)](https://avatars.githubusercontent.com/u/44389260?s=48&u=6da7176e51ae2654bcfd22564772ef8a3bb22318&v=4 "Charles Becker (chasbecker)")](https://github.com/chasbecker)
[![onetime: Arturi0](https://avatars.githubusercontent.com/u/46711571?s=48&u=57687c0e02d5d6e8eeaf9177f7b7af4c9f275eb5&v=4 "onetime: Arturi0")](https://github.com/Arturi0)


## Dependencies
- Python 3.8+
- [Python package dependencies (automatically installed)](https://github.com/thombashi/list-sponsors/network/dependencies)
