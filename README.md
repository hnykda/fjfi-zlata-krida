# fjfi-zlata-krida

## Instalace
1. Potřebujete Python (testováno na verzi 3.5) a pak knihovny `pandas` a `beautifulsoup`. Ty lze (máte-li python v `PATH`) nainstalovat pomocí `python install -r requirements.txt` (případně jen `pip pandas beautifulsoup4`). Pokud máte ubuntu, můžete knihovny a python nainstalovat jako: `sudo apt-get install python3-pandas python3-bs4`.
2. Pak stačí exekuovat skript jak je popsáno níže

## Použití
### Nápověda
Nápovědu vyvoláte pomocí `--help`:

```
$ python anketa.py --help      
usage: anketa.py [-h] [-u URL] [-n POCET_UCITELU] [-s SLEEP] [-p PATH] [-d]

Zpracovani ankety FJFI na geraldine serverech

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL ankety, hodnoceni dle jmena ucitele
  -n POCET_UCITELU, --pocet_ucitelu POCET_UCITELU
                        Kolik ucitelu se ma zpracovat (slouzi pro debug -
                        nechat prazdne)
  -s SLEEP, --sleep SLEEP
                        Delay, ktery bude nastaven kvuli snizeni pozadavku na
                        server
  -p PATH, --path PATH  Nazev adresare s vystupnimi soubory
  -d, --save_dicts      Ulozi pomocne dictionaries (pro debug)
```

### Spuštění zpracování
Skript potřebuje ve skutečni jen jeden parametr a tím je adresa za `-u/--url`.

Touto adresou je odkaz na *Seznam vyučujících dle jména*. Příkladem je třeba: http://geraldine.fjfi.cvut.cz/WORK/Anketa/LS2015/67_pub/teachers/index.html .

Skript pak tedy stačí sputit jako `python anketa.py --url http://geraldine.fjfi.cvut.cz/WORK/Anketa/LS2015/67_pub/teachers/index.html` a spustí se zpracování.

# TODO:
Ve skriptu lze nalézt různá TODO. Kromě toho by mu vůbec neuškodil celkový rewrite, tohle je hrozná prasárna, ale nechtělo se mi s tím více hrát. Dependencies jsou také jak bagr na vejce...
