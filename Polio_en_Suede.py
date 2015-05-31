#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt
import xlrd
import numpy

import gestion_figures

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


fichier = u"../Données_recueillies/Polio_Suède.xls"
classeur = xlrd.open_workbook( fichier )
nom_des_feuilles = classeur.sheet_names()
numFeuille = 0
feuillePays = classeur.sheet_by_name( nom_des_feuilles[numFeuille] )

Lignes = enum( 'ANNEE', 'POLIO_PARA', 'POLIO_NON_PARA', 'TYPE_DE_VIRUS', 'AGES_CIBLE', 'NB_VACCINS' )


# parcourt la feuille tant qu'il y a des pays
numCol = 1
cell = feuillePays.cell_value
annee = int( cell( numCol, Lignes.ANNEE ) )
annees = []
polio_para = []
polio_non_para = []
nb_vaccins = []
total_nb_vaccins = 0
while annee != 1965: # on saute l'année en cours car les données ne sont pas complètes
    annees.append( annee )
    polio_para.append( int( cell( numCol, Lignes.POLIO_PARA) ) )
    polio_non_para.append( int( cell( numCol, Lignes.POLIO_NON_PARA) ) )
    if cell( numCol, Lignes.NB_VACCINS ) == '':
        nb_vaccins.append( numpy.NaN )
    else:
        total_nb_vaccins += int( cell( numCol, Lignes.NB_VACCINS) ) / 1000
        nb_vaccins.append( total_nb_vaccins )
    numCol += 1
    annee = int( cell( numCol, Lignes.ANNEE ) )

# crée et prépare la figure
sources = [u"The Cutter incident and the development of a Swedish polio vaccine, 1952-1957, http://scielo.isciii.es/pdf/dyn/v32n2/03.pdf"]
fig = gestion_figures.FigureVaccination( 12, 6.4, sources, False )
plt.xlabel( u"Année" )
plt.ylabel( u"Poliomyélites par an" )
plt.annotate( u"Poliomyélites et vaccination en Suède", (0.5, 0.94), xycoords='figure fraction', ha='center', fontsize=14 )

# trace les courbes et les légendes
epaisseur=3
graphe_pfa, = plt.plot( annees, polio_para, linewidth=epaisseur, label=u"Paralysies flasques aiguës", color='red' )
graphe_sauvage, = plt.plot( annees, polio_non_para, linewidth=epaisseur, label=u"Poliomyélites sauvages", color='blue' )

ax = plt.twinx()
graphe_vaccinal, = plt.plot( annees, nb_vaccins, linewidth=epaisseur, label=u"Poliomyélites issus du vaccin", color='green' )

plt.legend([graphe_pfa, graphe_sauvage, graphe_vaccinal], [u"Polios paralytiques", u"Polios non paralytiques", 
           u"Vaccins"], bbox_to_anchor=(0.3, 0.9), loc=2, borderaxespad=1)
fig.legende_sources( plt, sources, 0.1, 0.9 )
plt.ylabel( u"Nombre de vaccins cumulés (milliers)" )
plt.show()

fig.sauvegarde_figure( "Polio_en_Suède" )
