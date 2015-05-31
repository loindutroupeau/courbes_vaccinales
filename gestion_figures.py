#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt

class FigureVaccination(): 
    def get( self ):
        return self.fig
    
    def __init__( self, longueur, hauteur, sources, pourLivre ):
        self.estPourLivre = pourLivre
        self.longueur = longueur
        self.hauteur = hauteur
        if pourLivre:
            self.incrementSources = 0.08
            self.margeBas = 0.1
            self.police = 22
        else:
            self.margeBas = 0
            self.incrementSources = 0.16
            self.police = 12
    
        self.fig = plt.figure( figsize=(longueur, hauteur + self.margeBas + len(sources)*self.incrementSources), dpi=80, facecolor = "white", linewidth = 20, edgecolor = "gray" )
        plt.rcParams.update({'font.size': self.police})

    def legende_sources( self, plt, liste_sources, marge_gauche=0.1, marge_droite=0.92 ):
        numSource = 0
        multX = self.fig.get_size_inches()[0] / 15
        if self.estPourLivre:
            grossissementPolice = 1.35
            incrementSources = 0.02
            margeSources = 0.02
            if liste_sources != []:
                margeBas = 0.1
            else:
                margeBas = 0.1
            margeX = 0.02
            positionSource = margeSources + incrementSources * len(liste_sources)
        else:
            grossissementPolice = 1
            incrementSources = 0.02
            margeSources = 0.05
            margeBas = 0.15
            margeX = 0.062
            positionSource = margeSources - incrementSources + incrementSources * len(liste_sources)
            
        if liste_sources != []:
            plt.annotate( "Sources:",
                          (0.02 / multX, positionSource ), 
                          weight='bold', xycoords='figure fraction', fontsize=8*grossissementPolice )
        for source in reversed( liste_sources ):
            plt.annotate( source, (margeX / multX, margeSources + incrementSources * numSource), xycoords='figure fraction', fontsize=8*grossissementPolice )
            numSource += 1
        marge_bas_total = margeBas + len( liste_sources ) * incrementSources
        print("avant",self.fig.get_size_inches())
        self.fig.subplots_adjust( left=marge_gauche, right=marge_droite, bottom=marge_bas_total )
        print("apres", self.fig.get_size_inches())
        if not self.estPourLivre:
            plt.annotate( "Figures sous licence LGPL\nCode : https://github.com/loindutroupeau\nloindutroupeau.blogspot.fr",
                          (0.95, 0.05), horizontalalignment='right', xycoords='figure fraction', fontsize=9*grossissementPolice )     
    
    def taille( self ):
        return (self.fig.get_size_inches()) 
        
    def sauvegarde_figure( self, nom_fichier ):
        nom_fichier = nom_fichier.replace(u"é","e").replace(u"è","e") # LaTeX traite mal les accents dans includegraphics...
        qualite = 120
        if self.estPourLivre:
            self.fig.savefig( '../figures/autres_formats/' + nom_fichier + '.png', transparent=False, dpi=qualite )
        else:
            print("Sauvegarde de " + nom_fichier + '.svg et .png')
            self.fig.savefig( '../figures/' + nom_fichier + '.svg', transparent=False, dpi=qualite*2, edgecolor = "gray" )     
            self.fig.savefig( '../figures/autres_formats/' + nom_fichier + '.png', transparent=False, dpi=qualite )
        print(nom_fichier, self.taille())
        return
    
        from PIL import Image
        size = self.fig.get_size_inches()[0]*self.fig.dpi/4, self.fig.get_size_inches()[1]*self.fig.dpi/4
        im = Image.open('../figures/autres_formats/' + nom_fichier + '.png')
        im.thumbnail(size, Image.ANTIALIAS)
        im.save('../figures/autres_formats/' + nom_fichier + '_petit.png', "PNG")
    #     plt.get_current_fig_manager().resize(100,50)
    #     self.fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False, dpi=self.fig.dpi ) # pour les .odt   
    #     self.fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False ) # pour les .odt   
        