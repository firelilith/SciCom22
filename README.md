# Dependencies

To run this project, a current version of Python 3 as well as Rust are needed. For instructions, see 

https://wiki.python.org/moin/BeginnersGuide/Download  
https://www.rust-lang.org/tools/install

# Install

To install, first clone this repository and cd into it:

```bash
git clone https://github.com/thatGuySpectre/SciCom22
cd SciCom22
```

It is recommended to use a virtual python environment:

```bash
python3 -m venv venv/
source venv/bin/activate
```

Then install poetry, to install dependencies

```bash
pip install poetry
poetry install
pip install .
```

You can now import the module `scicom` in python files within the venv, or call default examples in /tests directly.

# Usage


This module provides several ways to simulate gravitational interactions, as well as visualisation options. 

To start a simulation, you need to provide starting conditions in a YAML file. Several examples are provided in `scicom/presets`.
