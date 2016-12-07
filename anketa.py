from bs4 import BeautifulSoup
import pandas as pd

from urllib import request

from collections import defaultdict
import time

import argparse as argp

"""
Nova verze skriptu pro novy design od LS 2015/2016.

1. Sesbira URL adresy vyucujicich
2. Pro kazdeho vyucujiciho projde jednotlive predmety a ziska pocet hodnoticich a znamku
3. Na zaklade techto informaci vyhodnoti, zda vyucujici postupuje dale, nebo ne.
4. Vysledky ulozi do souboru "prosli.csv" a "neprosli.csv", log se vypisuje do logfile.log

TODO:
* hranice pro prosel/neprosel nastavit jako parametry skriptu
* pri spusteni skriptu bez parametru vypsat help a automaticky nespustit
* Ukazat default hodnoty v argument parseru
* automaticky si najit posledni dostupnou anketu a zpracovat tu defaultne

Contact: hnykdan1@fjfi.cvut.cz
"""


parser = argp.ArgumentParser( description = 'Zpracovani ankety FJFI na geraldine serverech' )
parser.add_argument( '-u', '--url', help = 'URL ankety, hodnoceni dle jmena ucitele',
                  type = str, default = "http://geraldine.fjfi.cvut.cz/WORK/Anketa/LS2015/67_pub/teachers/index.html" )
parser.add_argument( '-n', '--pocet_ucitelu', type = int, default = None, help = 'Kolik ucitelu se ma zpracovat (slouzi pro debug - nechat prazdne)' )
parser.add_argument( '-s', '--sleep', type = float, default = 0.1, help = 'Delay, ktery bude nastaven kvuli snizeni pozadavku na server' )
parser.add_argument( '-p', '--path', type = str, default = "anketa_{0}".format( time.strftime( "%d_%m_%Y" ) ), help = 'Nazev adresare s vystupnimi soubory' )
parser.add_argument( '-d', '--save_dicts', help = "Ulozi pomocne dictionaries (pro debug)", action = 'store_true' )
args = parser.parse_args()

class Issue():
    soup = ""
    newUrls = []
    motherUrl = ""

    vysledek = pd.DataFrame()
    ano = pd.DataFrame()
    ne = pd.DataFrame()

    ANO = defaultdict( list )
    NE = defaultdict( list )
    CHYBA = defaultdict( list )

    log = ""

    def __init__( self ):
        r = request.urlopen( args.url )
        self.soup = BeautifulSoup( r.read() )

        # sesbirej adresy ucitelu
        self.get_all_teachers_urls()

    def get_all_teachers_urls( self ):
        """Sesbira adresy ucitelu"""

        allTeac = []
        for i in self.soup.findAll( "a" ):
            try:
                if "teachers" in i["href"]:
                    allTeac.append( i["href"] )
            except:
                pass

        motherUrl = args.url[:args.url.find( "teachers" )]
        self.motherUrl = motherUrl
        newUrls = []
        for i in allTeac[4:]:  # prvni dva jsou rubish
            newUrl = motherUrl + i[3:]
            newUrls.append( newUrl )
        self.newUrls = newUrls

    def get_subject( self, predmet, url ):


        serk = {}
        predUrl = self.motherUrl + predmet["href"][6:]
        predRe = request.urlopen( predUrl )
        predSP = BeautifulSoup( predRe.read() )
        header = predSP.select_one("h1").text.split("- [")
        predmet = "[" + header[1]
        jmeno = header[0]

        prumer_celkove = float( predSP.find("div", {"class": "other-stats"}).find_all('li')[-1].text.split(":")[-1] )

        i = [x for x in predSP.findAll('div', {"class":"answers"}) if "Počet hodnotících:" in x.text][0]
        pod = i.find("li").text
        mezi = [int( s ) for s in pod.split() if s.isdigit()]
        try:
            hodn, celk = mezi[0], mezi[1]
            proc = round( hodn / celk, 2 )
            if ( proc == 1 ) or ( ( hodn >= 3 ) and ( proc >= 0.1 ) ):
                self.ANO[jmeno].append( predmet )
                prosel = "Ano"
                prosBool = True
            else:
                self.NE[jmeno].append( predmet )
                prosel = "Ne"
                prosBool = False
        except IndexError:
            hodn = mezi[0]
            celk = None
            proc = None
            self.CHYBA[jmeno].append( predmet )
            prosel = "Ne"
            prosBool = False

        serk = {"jmeno":jmeno,
                "predmet":predmet,
                "pocetHodnoticich":hodn,
                "pocetNavstevujicich":celk,
                "procentoHodnoticich":proc,
                "prosel":prosBool,
                "odkazVyucujiciho":url,
                "odkazPredmetu":predUrl,
                "celkovyPrumer":prumer_celkove}

        self.vysledek = self.vysledek.append( serk, ignore_index = True )
        vypis = "{0} - {5} - hodnotilo: {1}/{2} = {3}, prošel: {4},  celkova znamka: {6}".format(
                                        jmeno, hodn, celk, proc, prosel, predmet, prumer_celkove )
        print( vypis )
        self.log += vypis
        time.sleep( args.sleep )

    def collect_infos( self ):

        for url in self.newUrls[:args.pocet_ucitelu]:
            req = request.urlopen( url )
            sp = BeautifulSoup( req.read() )
            kurzTd = sp.select_one( "#main-content > div > aside > ul.list-unstyled.aside-links.other-courses")  # lokalizuje td s kurzama
            allCoursHref = kurzTd.findAll( "a" )

            for predmet in allCoursHref:
                self.get_subject( predmet, url )

    def polish( self ):
        limStr = 15
        limVel = 40
        # velikost = {0:"maly", 1:"stredni", 2:"velky"}

        self.vysledek["velikostPredmetu"] = 0

        for ix, val in self.vysledek.velikostPredmetu.items():
            n = self.vysledek.pocetNavstevujicich.iloc[ix]
            if n != None:
                if n >= limVel:
                    val = 2
                elif limStr <= n < limVel:
                    val = 1
                elif n < limStr:
                    val = 0
            else:
                val = None
            self.vysledek.velikostPredmetu.iloc[ix] = val

        self.vysledek = self.vysledek[["predmet", "jmeno", "velikostPredmetu", "pocetHodnoticich",
            "pocetNavstevujicich", "procentoHodnoticich", "celkovyPrumer", "odkazPredmetu", "odkazVyucujiciho", "prosel"]]

        self.ano = self.vysledek[self.vysledek.prosel == True]
        self.ne = self.vysledek[self.vysledek.prosel == False]

    def uloz( self ):
        import os

        try:
            os.mkdir( args.path )
            os.chdir( args.path )
        except FileExistsError:
            print( "Adresar existuje - vytvarim novy s nahodnym pridavkem na konci" )
            import random
            newDir = args.path + "_" + str( random.randint( 0, 1000 ) )
            os.mkdir( newDir )
            os.chdir( newDir )

        with open( "logfile.log", "w", encoding = "utf8" ) as ofile:
            ofile.write( self.log )

        self.ano.to_csv( "prosli.csv" )
        self.ne.to_csv( "neprosli.csv" )

        if args.save_dicts == True:

            self.dict_uloz()
        else:
            pass



    def dict_uloz( self ):
        for dicto, named in zip( [self.ANO, self.NE, self.CHYBA], ["ANO", "NE", "CHYBA"] ):
            with open( "{0}.csv".format( named ), "a", encoding = "utf8" ) as ofile:
                for i, j in dicto.items():
                    zap = i + ";" + str( j ) + "\n"
                    ofile.write( zap )


if __name__ == '__main__':

    issue = Issue()
    issue.collect_infos()
    issue.polish()
    issue.uloz()
