#!/usr/bin/python2.7
# coding: utf-8

import xlrd
import os, glob
import re # exoressions régulières
# import numpy
import matplotlib.pyplot as plt
# from samba import strcasecmp_m
from operator import itemgetter # pour trier les années

CODE = 0; ANNEE = 1; SEXE = 2; AGE = 3; NB_MORTS = 4

def ajouterDonneesFichier( nbMorts, typesDeMort, maladies, diagnosticsPossibles, fichier ):	
	# Réouverture du classeur
	classeur = xlrd.open_workbook( fichier )
	
	# Récupération du nom de toutes les feuilles sous forme de liste
	nom_des_feuilles = classeur.sheet_names()
	
	# Récupération de la première feuille
	feuilleDescription = classeur.sheet_by_name( nom_des_feuilles[1] )
		
	codesMaladie = {}
	maladieParCodes = {}
	codesRetenus = []
	
	for maladie in maladies:
		ligne = 0
		maladieTest = feuilleDescription.cell_value( ligne, 1 )
		codesMaladie[maladie] = []
		maladieTrouvee = False
		finDuFichier = False
		while not finDuFichier:
			ligne = ligne + 1
			try:
				maladieTest = feuilleDescription.cell_value( ligne, 1 )
				if re.compile( diagnosticsPossibles[maladie] ).match( maladieTest ) != None: # la maladie correspond aux descriptions possibles
					maladieTrouvee = True
					if not maladieTest in typesDeMort:
						typesDeMort.append( maladieTest )
					codeMaladie = ( feuilleDescription.cell_value( ligne, 0 ) )
					if type( codeMaladie ) == float or type( codeMaladie ) == int:
						codeMaladie = str( int( codeMaladie ) )
					codesMaladie[maladie].append( codeMaladie )
					maladieParCodes[codeMaladie] = maladie
					codesRetenus.append( codeMaladie )					
			except:
				finDuFichier = True
				if not maladieTrouvee:
					print("Maladie non trouvée", maladie, fichier )
	
	print( "codesMaladie", codesMaladie )
	print( "typesDeMort", typesDeMort )
	print( "codeRetenus", codesRetenus )
	print( "maladieParCodes", maladieParCodes )

	for numFeuille in range( 2, len( nom_des_feuilles ) ):
		feuilleValeurs = classeur.sheet_by_name(nom_des_feuilles[numFeuille])
		ligne = 1
		ligneCorrecte = True
		while ligneCorrecte:
			try:
# 				print( ligne )
				codesMaladie = (feuilleValeurs.cell_value( ligne, CODE ))
# 				if( ligne > -5100 and ligne < 25 ):
# 					print( codesMaladie, ligne, str( int( codesMaladie ) ) )
				maladieTrouveeDansLesCodesRetenus = ( codesMaladie in codesRetenus )
				if not maladieTrouveeDansLesCodesRetenus:
					try: 
						if str( int( codesMaladie ) ) in codesRetenus: # on peut trouver des codes 0010 pour 10, donc il faut convertir
							maladieTrouveeDansLesCodesRetenus = True
							codesMaladie = str( int( codesMaladie ) )
					except: ()
				if maladieTrouveeDansLesCodesRetenus:
#  					print("oui")
					annee = int( feuilleValeurs.cell_value( ligne, ANNEE ) )
# 					if( ligne > -5100 and ligne < 25 ):
# 			 			print(type( annee ))
# 				 		print(annee)
					nbMortsCategorie = feuilleValeurs.cell_value( ligne, NB_MORTS )
# 					print(nbMortsCategorie, maladieParCodes[codesMaladie])
					nomMaladie = maladieParCodes[codesMaladie]
					if nbMorts[nomMaladie].has_key( annee ):
# 	 					print("has key")
						nbMorts[nomMaladie][annee] = nbMorts[nomMaladie][annee] + nbMortsCategorie
					else:
# 	 					print("!has key")
						nbMorts[nomMaladie][annee] = nbMortsCategorie
				ligne = ligne + 1	
			except:
				ligneCorrecte = False
		
	print( "nb morts", nbMorts )
# 	return nbMorts

repertoire = "/home/pierrejean/Perso/Dropbox/vacc-notsaved/Statistiques"
print(os.getcwd())
os.chdir( repertoire )
# fichiers = glob.glob( "*9_c.xls" )
# fichiers = glob.glob( "*_*.xls" )
# fichiers = glob.glob( "*1.xls" )

fichiers = glob.glob( "*.xls" )
print(fichiers)
nbMorts = {}

# maladies = [u"Coqueluche"]
# maladies = [u"Diphtérie"]
# maladies = [u"Hépatites"]
# maladies = [u"Poliomyélite"]
# maladies = [u"Scarlatine"]
# maladies = [u"Tétanos"]
maladies = [u"Tuberculose"]
# maladies = [u"Vaccin"]

diagnosticsPossibles={}
diagnosticsPossibles[u"Coqueluche"] = "^.*([p,P]ertussis|[W,w]hooping cough).*$"
diagnosticsPossibles[u"Diphtérie"] = "^.*([d,D]iphtheria).*$"
diagnosticsPossibles[u"Hépatites"] = "^.*([H,h]epatitis).*$"
diagnosticsPossibles[u"Poliomyélite"] = "^.*([p,P]oliomyelitis).*$"
diagnosticsPossibles[u"Rougeole"] = '^.*([M|m]easles).*$'
diagnosticsPossibles[u"Scarlatine"] = "^.*([S,s]carl[atina,et]).*$"
diagnosticsPossibles[u"Tétanos"] = "^.*([T,t]etanus).*$"
# Apparemment, pour être en accord avec gov.uk après 1988-2013, il faut enlever "Late effects of tuberculosis". Pas très juste mais pour la cohérence du graphe
diagnosticsPossibles[u"Tuberculose"] = '(?!Late*)^.*([t,T](\.)*b\.|[t,T]ubercul|[P,p]hthisis|Tabes mesenterica|Lupus|Tubercle|Scrofula).*$' # Tb, t.b., tb., etc.
diagnosticsPossibles[u"Vaccin"] = '^.*(accination|accinal|accines|immunization|inoculation).*$' # Tb, t.b., tb., etc.

for maladie in maladies:
	nbMorts[maladie] = {}

typesDeMort = []
for fichier in fichiers:
	print( "path", fichier ) 
	ajouterDonneesFichier( nbMorts, typesDeMort, maladies, diagnosticsPossibles, fichier ) 
	
numFigure = 1	
for maladie in nbMorts:
	x = []
	y = []
	print("maldie", maladie)
	for annee in range( min( nbMorts[maladie] ), max( ( nbMorts[maladie] ) ) + 1 ):
		x.append( -int( annee ))
		if annee in nbMorts[maladie]:
			y.append( nbMorts[maladie][annee] )
#  			print("nan", annee, nbMorts[maladie][annee])
		else:
			y.append( 0 )

	(anneeinv, nb) = [list(z) for z in zip(*sorted(zip(x, y), key=itemgetter(0)))]
	annee = []
	for a in anneeinv:
# 		print ("a, ", a, -a )
		annee.append( -a )
	plt.figure( numFigure )
	numFigure = numFigure + 1
	plt.plot( annee, nb )
	print ("x", annee )
	print ("y", nb )
	plt.title( maladie )
	plt.xlabel( u'Années' )
	plt.ylabel( u'Décès' )
	plt.axis([min(annee), max(annee), 0, max(nb)])
	
# rev = []
# for i in reversed(nb):
# 	rev.append(i)
# 	
# print "tableau"	
print typesDeMort
plt.show()


if __name__ == '__main__':
	print("oui")