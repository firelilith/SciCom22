from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="scicom-project",
    version="0.1.0",
    description="relativistic and newtonian three-body-simulation",
    author="Spectre",
    packages=["pykanka"],
    install_requires=["numpy", "scipy", "einsteinpy"]
)