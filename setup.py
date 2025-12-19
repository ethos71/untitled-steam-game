from setuptools import setup, find_packages

setup(
    name="untitled-steam-game",
    version="0.1.0",
    description="A NES-style roguelike game with steampunk and apocalypse themes",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        'console_scripts': [
            'untitled-game=main:main',
        ],
    },
    python_requires='>=3.8',
)
