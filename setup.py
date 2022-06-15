import pathlib

from setuptools import find_packages, setup

import versioneer


REPO_ROOT = pathlib.Path(__file__).parent

with open(REPO_ROOT / "README.md", encoding="utf-8") as f:
    README = f.read()

REQUIREMENTS = ["pandas"]

setup(
    name="phoenix-scrape",
    version=versioneer.get_version(),
    description="Pulling of data from APIs module of peacebuilders' social media analysis toolkit",
    long_description=README,
    long_description_content_type="text/markdown",
    author="datavaluepeople",
    author_email="opensource@datavaluepeople.com",
    url="https://github.com/datavaluepeople/phoenix-scrape",
    license="GNU General Public License v3 (GPLv3)",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    python_requires=">=3.8",
    cmdclass=versioneer.get_cmdclass(),
)
