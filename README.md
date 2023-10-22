# PokedexEPD

Display Pokedex entries on an e-paper display.

## Installation

First, install `PokedexEPD`:
```pip install git+https://github.com/YOUR_USERNAME/PokedexEPD.git```

### Dependencies based on Screen Type

After installing `PokedexEPD`, you need to install one of the following extras based on your screen type:

#### WaveShare non-IT8951 Screens

Install with `waveshare_epd` extra:
```pip install -e "git+https://github.com/waveshare/e-Paper.git#egg=waveshare_epd&subdirectory=RaspberryPi_JetsonNano/python"```

#### IT8951 based Screens

Install with `IT8951` extra:
```pip install -e "git+https://github.com/GregDMeyer/IT8951#egg=IT8951"```
