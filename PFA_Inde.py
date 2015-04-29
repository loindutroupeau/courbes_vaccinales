#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt
import xlrd
import numpy

import annotations

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


fichier = u"../Données_recueillies/PFA_Inde.xls"
classeur = xlrd.open_workbook( fichier )
nom_des_feuilles = classeur.sheet_names()
numFeuille = 0
feuillePays = classeur.sheet_by_name( nom_des_feuilles[numFeuille] )

Lignes = enum( 'ANNEE', 'PAYS', 'PFA', 'TAUX_NON_POLIO', 'TAUX_SELLES_ADEQUATES',
               'EN_COURS', 'POLIO_SAUVAGE', 'ISSUE_DU_VACCIN', 'COMPATIBLES' )

# parcourt la feuille tant qu'il y a des pays
numCol = 1
cell = feuillePays.cell_value
annee = int( cell( numCol, Lignes.ANNEE ) )
annees = []
pfa = []
taux_pfa_non_polio = []
polio_sauvage = []
polio_vaccinale = []
while annee != 2015: # on saute l'année en cours car les données ne sont pas complètes
    annees.append( annee )
    pfa.append( int( cell( numCol, Lignes.PFA) ) )
    taux_pfa_non_polio.append( float( cell( numCol, Lignes.TAUX_NON_POLIO) ) )
    if cell( numCol, Lignes.POLIO_SAUVAGE ) == '':
        polio_sauvage.append( numpy.NaN )
    else:
        polio_sauvage.append( int( cell( numCol, Lignes.POLIO_SAUVAGE) ) )
    polio_vaccinale.append( int( cell( numCol, Lignes.ISSUE_DU_VACCIN) ) )
    numCol += 1
    annee = int( cell( numCol, Lignes.ANNEE ) )

# crée et prépare la figure
sources = [u"Base de données OMS, https://extranet.who.int/polis/public/CaseCount.aspx"]
fig = plt.figure( 0, figsize=(12, 6.4 + len(sources)*0.16), dpi=80, facecolor = "white", linewidth = 20, edgecolor = "gray" )
plt.xlabel( u"Année" )
plt.ylabel( u"Nombre annuel" )
plt.annotate( u"Cas de paralysies et de poliomyélites en Inde", (0.5, 0.94), xycoords='figure fraction', ha='center', fontsize=14 )

# trace les courbes et les légendes
epaisseur=3
graphe_pfa, = plt.plot( annees, pfa, linewidth=epaisseur, label=u"Paralysies flasques aiguës" )
graphe_sauvage, = plt.plot( annees, polio_sauvage, linewidth=epaisseur, label=u"Poliomyélites sauvages" )
graphe_vaccinal, = plt.plot( annees, polio_vaccinale, linewidth=epaisseur, label=u"Poliomyélites issues du vaccin" )

plt.legend(bbox_to_anchor=(0.1, 0.9), loc=2, borderaxespad=1)
annotations.legende_sources( fig, plt, sources, 0.1, 0.93 )
plt.show()

print "Sauvegarde de PFA_Inde en .svg, .jpeg et .png"
fig.savefig( '../figures/PFA_Inde.svg', transparent=False, dpi=fig.dpi )     
fig.savefig( '../figures/autres_formats/PFA_Inde.png', transparent=False, dpi=fig.dpi )     
fig.savefig( '../figures/autres_formats/PFA_Inde.jpeg', transparent=False, dpi=fig.dpi )        
