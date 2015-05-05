#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt
import xlrd
import numpy
import math
import operator
import re # exoressions régulières
import copy
from scipy import stats

import gestion_figures

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def listeVaccins( cell ):
    col = Colonnes.VACCINS
    vaccin, type_vaccin  = cell( 0, col ).split(",")
    vaccins = []
    while vaccin != 'FIN':
        vaccins.append( ( vaccin, type_vaccin.replace( " ", "" ) ) )
        col += 1
        vaccin, type_vaccin  = cell( 0, col ).split(",")
    return vaccins

def combinaisonVaccins( vaccins ):
    combinaisons_vaccins = [[]]
    def ajouteVaccinAListeCombinaison( listeCombinaison, vaccin ):
        for combinaison in listeCombinaison:
            combinaison.append( vaccin )
    for vaccin in vaccins:
        combinaisons_sans_ce_vaccin = copy.deepcopy( combinaisons_vaccins )
        ajouteVaccinAListeCombinaison( combinaisons_vaccins, vaccin )
        for i in range(0,len(combinaisons_sans_ce_vaccin)):
            combinaisons_vaccins.append( combinaisons_sans_ce_vaccin[i] ) #combinaisons_avec_ce_vaccin )
    return combinaisons_vaccins
    
def nbDosesAvant( text, nbMoisMax ):
    text = text.replace( 'months', '' )
    text = text.replace( 'month', '' )
    text = text.replace( 'birth', '0' )
    text = text.replace( ' ', '' )
    text = text.replace( ';', ',' )
    doses = text.split(',')
    nbDoses = 0
    for dose in doses:
        if dose == '':
            continue
        intervalle = dose.split('-')
        if len(intervalle) > 1:
            debut, fin = intervalle
        else:
            debut = intervalle[0]
            fin = debut
        mois_retenu = int( debut )  # si on choisit le premier mois de l'intervalle comme date référence
#         mois_retenu = ( int( debut ) + int( fin ) ) / 2    # si on prend la moyenne
        if mois_retenu <= nbMoisMax:
            nbDoses += 1
    return nbDoses

def dosesAffichees( pays, vaccins_retenus=".*", types_retenus=".*" ):
    nbDoses = 0
    for doses_vaccin in nb_doses[pays]:
        vaccin, type_vaccin = doses_vaccin[0]
        if re.compile( vaccins_retenus ).match( vaccin ) != None and \
            re.compile( types_retenus ).match( type_vaccin ) != None: 
            nbDoses += doses_vaccin[1]
    return nbDoses

def tracerFleches( nb_doses, mortalite_tracee ):
    for pays in nb_doses:
        if pays in decalage_fleches:
            xx = dosesAffichees( pays )
            yy = mortalite_tracee[pays]
            print(pays + " " + str(xx) + " " + str(yy))
            decX, decY = decalage_fleches[pays]
            decY *= plt.ylim()[1] / 6
            normeDec = math.sqrt( decX*decX + decY*decY )
            plt.annotate( pays, color='gray', xy=(xx + decX * 0.2/normeDec, yy + decY * 0.2/normeDec), 
                          xytext=(xx + decX, yy + decY ),
                          arrowprops=dict(color='gray',shrink=0.05, width=0.8, headwidth = 3, frac=0.2/normeDec ) )
    

def tracerPoints( mortalite_tracee, titreY, numGraphe, combinaisonVaccins, nePasTracer=False, restrictionVaccin="" ):    
    # par exemple vaccins_retenus = u"^.*(BCG|Diphtérie|Tétanos|ROR).*$"
    if combinaisonVaccins == []:
        return 0,1
    vaccins_retenus = u"^.*("
    for vaccin in combinaisonVaccins[:-1]:
        vaccins_retenus += vaccin[0] + "|"
    if len(combinaisonVaccins) > 0:
        vaccins_retenus += combinaisonVaccins[-1][0]
    vaccins_retenus += ").*$"
    x = []
    y = []
    for pays in nb_doses:
        nbDoses = dosesAffichees( pays, vaccins_retenus, types_retenus )
        if nb_doses[pays] != []:
            x.append( nbDoses )
            y.append( mortalite_tracee[pays] )
          
    # calcule et trace la corrélation
    a, b, r, valeur_p, _ = stats.linregress(x,y)

    if not nePasTracer:    
        plt.subplot(1, 2, numGraphe) 
        plt.xlabel( u"Nombre de doses du calendrier avant 12 mois" + restrictionVaccin )        
        plt.ylabel( titreY )
        plt.annotate( u"Calendrier vaccinal et mortalité selon les pays d'Europe", 
                               (0.5, 0.94), xycoords='figure fraction', ha='center', fontsize=14 )
        plt.scatter( x, y, c='b', s=30, marker='o' )
        tracerFleches( nb_doses, mortalite_tracee )        
        x_max = plt.xlim()[1]
        marge = x_max / 20       
        plt.plot([marge, x_max-marge],[b+a,b+a*(x_max-marge)],linewidth=2,c='r',ls='--')
        r_texte = "r = " + "%0.2f" % r
        p_texte = "p = " + "%0.4f" % valeur_p
        plt.annotate( r_texte + "\n" + p_texte, color='red', xy=(0,0), xytext=(marge,b+marge*a + 0.5) )
     
        # ajuste les axes
        plt.xlim( 0, plt.xlim()[1] )
        plt.ylim( 0, plt.ylim()[1] )    
    return r, valeur_p
    
def listeVaccinTexte( vaccins ):
    texte = "["
    for vaccin, _ in vaccins[:-1]:
        texte += vaccin + ";"
    texte += vaccins[len(vaccins)-1][0]
    texte += "]"
    return texte
    
def tracerPireCombinaison( mortalite, titre, vaccins, numGraphe ):
    combinaisons_vaccins = combinaisonVaccins( vaccins )
    max_r = 0
    for combi in combinaisons_vaccins:
        r, _ = tracerPoints( mortalite, "", 0, combi, True )
        if r > max_r:
            max_r = r
            print("Nouveau meilleur r = " + combi + " " + r )
            combi_pire_r = combi
    
    tracerPoints( mortalite, titre, numGraphe, combi_pire_r, False, "\n" + listeVaccinTexte(combi_pire_r) )
    
    
fichier = u"../Données_recueillies/Vaccins_et_mortalité_infantile.xls"
classeur = xlrd.open_workbook( fichier )
nom_des_feuilles = classeur.sheet_names()
numFeuille = 0
feuillePays = classeur.sheet_by_name( nom_des_feuilles[numFeuille] )
Colonnes = enum( 'PAYS', 'COUNTRY', 'TAUX_MORTALITE_INFANTILE', 'TAUX_MORTALITE', 'VACCINS' )


# vaccins_retenus = u"^.*(BCG|Diphtérie|Tétanos|ROR).*$"
# vaccins_retenus = ".*"
types_retenus = "^.*(I|V).*$"

# parcourt la feuille tant qu'il y a des pays
nomPays = 'vide'
NB_MOIS_MAX = 11
cell = feuillePays.cell_value
nom_pays = []
vaccins = listeVaccins( cell )
mortalite_infantile = {}
mortalite_totale = {}
nb_doses = {}
ligne = 2
nomPays = cell( ligne, Colonnes.PAYS )
while nomPays != 'FIN': # and ligne <= 57:
    nom_pays.append( nomPays )
    texte = cell(ligne, Colonnes.TAUX_MORTALITE_INFANTILE)
    if texte == '':
        mortalite_infantile[nomPays]= numpy.NaN
    else:
        mortalite_infantile[nomPays]= float( texte )
    texte = cell(ligne, Colonnes.TAUX_MORTALITE)
    if texte == '':
        mortalite_totale[nomPays]= numpy.NaN
    else:
        mortalite_totale[nomPays]= float( texte )
    nb_doses[nomPays] = []
    col = Colonnes.VACCINS
    ligne_vide = True
    for vaccin in vaccins:
        texte = str( cell(ligne, col) )
        if ligne_vide and nbDosesAvant( texte, 24 ) > 0:
            ligne_vide = False
        nb_doses[nomPays].append((vaccin, nbDosesAvant( texte, NB_MOIS_MAX )))
        col += 1
    if ligne_vide:
        nb_doses[nomPays] = []  # on efface les zéros pour les vaccins, c'est juste que rien n'a été rempli
    ligne += 1
    nomPays = cell( ligne, Colonnes.PAYS )

print(nb_doses)

# crée et prépare la figure
sources = [u"Immunization Summary, Edition 2014, http://www.who.int/immunization/monitoring_surveillance/Immunization_Summary_2013.pdf (Calendrier vaccinal 2013)",
           u"https://www.cia.gov/library/publications/the-world-factbook/rankorder/2091rank.html (Mortalité infantile 2014)",
           u"https://www.cia.gov/library/publications/the-world-factbook/rankorder/2066rank.html (Mortalité 2014)"]
fig = plt.figure( 0, figsize=(16, 6.4 + len(sources)*0.16), dpi=80, facecolor = "white", linewidth = 20, edgecolor = "gray" )
 
fig.subplots_adjust(bottom=0.2)
 
# trace des flèches pour indiquer certains pays
decalage_fleches = {}
decalage_fleches[u"Allemagne"] = [-0.2,+0.4]
decalage_fleches[u"Australie"] = [2.5,-0.1]
# decalage_fleches[u"Corée du Sud"] = [1,1]
decalage_fleches[u"Danemark"] = [-6,0.4]
# decalage_fleches[u"Espagne"] = [-3,0.3]
# decalage_fleches[u"Finlande"] = [-4,-0.4]
decalage_fleches[u"France"] = [-6,0.4]
decalage_fleches[u"États-Unis"] = [1.8,-0.1]
# decalage_fleches[u"Italie"] = [-2,-0.1]
decalage_fleches[u"Japon"] = [1.5,-0.1]
decalage_fleches[u"Monaco"] = [-5,-0.3]
decalage_fleches[u"Royaume-Uni"] = [0.5,+0.5]
decalage_fleches[u"Suisse"] = [0,-0.5]


mortalite_triee = sorted(mortalite_infantile.items(), key=operator.itemgetter(1))
# nbPaysMax = 50
# numPays = 0
# for pays in mortalite_triee:
#     if numPays == nbPaysMax:
#         break;
#     numPays += 1
#     nbDoses = dosesAffichees( pays[0] )
#     if nbDoses > 0:
#         print pays[0] + u" : mortalité de " + str(pays[1]) + " avec " + str(nbDoses) + u" doses jusqu'à " + str(NB_MOIS_MAX) + " mois"
#     else:
#         print "Pas de donnees pour", pays[0]
       
tracerPoints( mortalite_infantile, u'Taux de mortalité infantile (pour 1000 naissances)', 1, vaccins )
tracerPoints( mortalite_totale, u'Taux de mortalité général (pour 100.000)', 2, vaccins )
   
calculPireCombinaison = False # prend du temps       
if calculPireCombinaison:       
    tracerPireCombinaison( mortalite_infantile, u'Taux de mortalité infantile', vaccins, 1 )       
    tracerPireCombinaison( mortalite_totale, u'Taux de mortalité', vaccins, 2 )
    
gestion_figures.legende_sources( fig, plt, sources, 0.05, 0.95 )
plt.show()

gestion_figures.sauvegarde_figure(fig, "Doses_infantiles_et_mortalité")
