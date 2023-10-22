from setuptools import setup, find_packages

setup(
    name="PokedexEPD",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'epdlib==0.6'
    ],
    author="Michael",
    author_email="michael@wilkowski.net",
    description="Displays Pokedex entries on an e-paper display",
    license="MIT",
    keywords="pokedex epaper display",
    url="https://github.com/wilks7/PokedexEPD",
)
