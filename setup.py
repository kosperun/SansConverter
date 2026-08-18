import pathlib

from setuptools import find_packages, setup

version_globals = {}
exec((pathlib.Path(__file__).parent / "src" / "_version.py").read_text(), version_globals)

setup(
    name="sansconverter",
    version=version_globals["__version__"],
    description="A converter for different Sanskrit transliteration systems",
    author="Kostiantyn Perun",
    author_email="kosperun@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt6==6.7.0",
        "pyqt6-qt6==6.7.0",
    ],
    extras_require={
        "dev": [
            "flake8==5.0.4",
            "black==22.6.0",
            "pre-commit==2.20.0",
            "pylint==2.14.5",
            "ipython==8.4.0",
            "pytest==8.2.2",
        ]
    },
    entry_points={
        "gui_scripts": [
            "SansConverter=sans_converter:main",
        ]
    },
    include_package_data=True,
)
