from setuptools import setup


VERSION = "0.2.0"
LICENSE = "MIT"
DESCRIPTION = "A module to generate VapourSynth's stub file for intellicode."

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="vsstubs",
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaltyChiang/VapourSynth-Plugins-Stub-Generator",
    author="SaltyChiang",
    author_email="SaltyChiang@users.noreply.github.com",
    packages=["vsstubs"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["vsstubs = vsstubs.main:main"]},
)
