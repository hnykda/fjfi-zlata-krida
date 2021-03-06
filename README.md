# Spracování výsledků ankety FJFI pro soutěž Zlatá křída

## Instalace
### Rychlá varianta
Ve složce se skriptem `anketa.py` a `requirements.txt`.
```
python3 -m venv anketa-venv
source anketa-venv/bin/activate
pip install -r requirements.txt
python3 ankety.py -u <URL_NA_SEZNAM_UCITELU_DLE_JMENA>
```

### Vysvětlení + pomalá varianta
Potřebujete Python verze 3 (testováno na verzi 3.5) a pak knihovny `pandas` a `beautifulsoup`. Ty lze (máte-li python v `PATH`) nainstalovat pomocí `pip install -r requirements.txt` (případně jen `pip pandas beautifulsoup4`). Pokud máte ubuntu, můžete knihovny a python nainstalovat jako: `sudo apt-get install python3-pandas python3-bs4` a jiné obdoby dle distribuce. Jako vždy, [google je váš kamarád](http://lmgtfy.com/?q=how+to+install+python)... 

Pak stačí exekuovat skript pomocí `python3 anketa.py` jak je popsáno níže.

## Použití
### Nápověda
Nápovědu vyvoláte pomocí `--help`:

```
$ python3 anketa.py --help      
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

### Spuštění vyhodnocení
Skript potřebuje ve skutečni jen jeden parametr a tím je adresa za `-u/--url`.

Touto adresou je odkaz na *Seznam vyučujících dle jména* z roku, který chcete vyhodnotit. Příkladem je třeba: http://geraldine.fjfi.cvut.cz/WORK/Anketa/LS2015/67_pub/teachers/index.html .

Skript pak tedy stačí sputit jako `python anketa.py --url http://geraldine.fjfi.cvut.cz/WORK/Anketa/LS2015/67_pub/teachers/index.html` a spustí se zpracování. Vytvoří se v dané složce adresář s několik výstupními soubory a logovacími informacemi. Nejdůležitější je pak soubor `prosli.csv`, který obsahuje (snad) srozumitelné metriky a údaje podstatné k vyhodnocení.

# TODO
Ve skriptu lze nalézt různá TODO. Kromě toho by mu vůbec neuškodil celkový rewrite, tohle je hrozná prasárna, ale nechtělo se mi s tím více hrát. Dependencies jsou také jak bagr na vejce... Shrnutí, co by se dalo zlepšit:

1. Dostat se rovnou k databázi, ze které se to tahá na web. Pak by to stačilo na pár selectů a nemusely by se dělat takové opičárny se scrapováním... To za mého působení nebylo možné, protože databáze se střežila jako Fort Knox.
2. logging pomocí `logging` modulu
3. Odstranění `pandas` jako dependencies (dicts a tuples by stačily)

Než to ale někdo začne dělat, měl by si odpovědět na otázku, zda to u skriptu, který se spustí jednou za půl roku na 1 minutu, je potřeba...
