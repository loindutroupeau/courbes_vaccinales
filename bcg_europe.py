#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt
import xlrd
import numpy
import math

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


fichier = u"../Données_calculées/BCG_Europe.xls"
classeur = xlrd.open_workbook( fichier )
nom_des_feuilles = classeur.sheet_names()
numFeuille = 0
feuillePays = classeur.sheet_by_name( nom_des_feuilles[numFeuille] )

Lignes = enum( 'PAYS', 'PAYS_TRADUCTION', 'TAUX_INCIDENCE', 'TAUX_INCIDENCE_ENFANTS', 'RATIO_ADULTES_ENFANTS',
               'COUVERTURE_MIN', 'COUVERTURE_MAX', 'ANNEE', 'PROGRAMME_A_SUIVRE' )

def getCouv( couvStr ):
    if couvStr == "n/a":
        couv = numpy.nan
    elif couvStr == "-":
        couv = 0
    else:
        couv = float(couvStr[0:-1])
    return couv

# parcourt la feuille tant qu'il y a des pays
nomPays = 'vide'
numCol = 2
cell = feuillePays.cell_value
nomPays = cell( numCol, Lignes.PAYS )
nom_pays = []
incidence = []
incidence_enfants = []
min_couverture = []
max_couverture = []
bcg = {}
while nomPays != 'FIN':
    nom_pays.append( nomPays )
    _incidence = float(cell(numCol,Lignes.TAUX_INCIDENCE))
    incidence.append( _incidence )
    min_couv = getCouv( cell( numCol,Lignes.COUVERTURE_MIN) )
    max_couv = getCouv( cell( numCol,Lignes.COUVERTURE_MAX) ) 
    min_couverture.append( min_couv )
    max_couverture.append( max_couv )
    bcg[nomPays] = [_incidence, min_couv, max_couv]    
    numCol += 1
    nomPays = cell( numCol, Lignes.PAYS_TRADUCTION )

# crée et prépare la figure
fig = plt.figure( 0, facecolor = "white", linewidth = 20, edgecolor = "gray" )
plt.xlabel( u"Couverture du vaccin BCG (%) [intervalle si incertitude]" )
plt.ylabel( u'Incidence (taux pour 100.000)' )
plt.annotate( u"Couverture BCG en 2003 et incidence selon les pays d'Europe", 
                           (0.5, 0.94), xycoords='figure fraction', ha='center', fontsize=14 )
fig.subplots_adjust(bottom=0.2)
plt.annotate( u"Sources : Euro Surveill 2006;11(3): 6-11 (http://opac.invs.sante.fr/doc_num.php?explnum_id=4827)", 
                           (0.05, 0.05), xycoords='figure fraction', fontsize=9 )

# trace des flèches pour indiquer certains pays
decalage_fleches = {}
decalage_fleches[u"Allemagne"] = [10,+10]
decalage_fleches[u"France"] = [-12,+10]
decalage_fleches[u"Grèce"] = [-0,+15]
decalage_fleches[u"Lituanie"] = [-20,+10]
decalage_fleches[u"Portugal"] = [-20,+10]
decalage_fleches[u"Roumanie"] = [-20,-10]
decalage_fleches[u"Royaume-Uni"] = [-25,+15]
decalage_fleches[u"Espagne"] = [10,10]
for pays in bcg:
    if decalage_fleches.has_key(pays):
        _incidence, min_couv, max_couv = bcg[pays]
        decX, decY = decalage_fleches[pays]
        normeDec = math.sqrt( decX*decX + decY*decY )
        plt.annotate( pays, color='gray', xy=(min_couv + decX * 2/normeDec, _incidence + decY * 2/normeDec), 
                      xytext=(min_couv + decX, _incidence + decY ),
                      arrowprops=dict(color='gray',shrink=0.01, width=0.8, headwidth = 8, frac=3/normeDec ) )

# trace les points
plt.scatter( min_couverture,incidence, c='b', s=30, marker='<' )
plt.scatter( max_couverture, incidence, c='b', s=30, marker='>' )
plt.hlines( incidence, min_couverture, max_couverture, colors='b' )

# ajuste les axes
plt.xlim(0, 100)
plt.ylim(0, plt.ylim()[1])

plt.show()

