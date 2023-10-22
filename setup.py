from setuptools import setup, find_packages

setup(
    name="PokedexEPD",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # You can also read from requirements.txt
        'epaper==1.0.0'
    ],
    author="Michael",
    author_email="michael@wilkowski.net",
    description="Displays Pokedex entries on an e-paper display",
    license="MIT",
    keywords="pokedex epaper display",
    url="https://github.com/YOUR_USERNAME/PokedexEPD",
)
