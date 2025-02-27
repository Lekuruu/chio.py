
import setuptools
import chio
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, "README.md")

with open(readme_path, "r") as f:
    long_description = f.read()

setuptools.setup(
    name="chio",
    version=chio.__version__,
    author=chio.__author__,
    author_email=chio.__email__,
    description="A python library for serializing and deserializing bancho packets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["osu", "osugame", "python", "bancho"],
)
