import io
import os
from typing import Any

from setuptools import find_packages, setup


def read(*paths: str, **kwargs: Any) -> str:
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path: str) -> list:
    return [line.strip() for line in read(path).split("\n") if not line.startswith(('"', "#", "-", "git+"))]


setup(
    name="project_name",
    version=read("project_name", "VERSION"),
    description="project_description",
    url="https://github.com/author_name/project_urlname/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="author_name",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["project_name = project_name.__main__:main"]},
    extras_require={"test": read_requirements("requirements-test.txt")},
)
