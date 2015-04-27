#!/usr/bin/python2.7
# coding: utf-8

import matplotlib.pyplot as plt
import xlrd
import numpy
import pylab

import annotations

fichier = u"../Données_recueillies/Incidence.xls"
classeur = xlrd.open_workbook( fichier )

# Récupération du nom de toutes les feuilles sous forme de liste
nom_des_feuilles = classeur.sheet_names()

numFeuille = 0

# Récupération de la première feuille
feuillePays = classeur.sheet_by_name( nom_des_feuilles[numFeuille] )
 
annees = []
finDeLigne = False
ligne_annee = 2
col = 2
while not finDeLigne:
    try:
        annee = int( feuillePays.cell_value( 1, col ) )
        annees.append( annee ) 
        col = col + 1        
    except: 
        finDeLigne = True
 
tableau = {}
colonneSource = 1
colonnePremiereDonnee = 2
numCourbe = 2
premiereAnnee = 2014
while True:
    nomCourbe = feuillePays.cell_value( numCourbe, 0 )
    if nomCourbe == "FIN":
        break
    if nomCourbe == '':
        numCourbe += 1
        continue
    nomCourbeTaux = "taux " + nomCourbe
    nomMaladie = nomCourbe.split()[0]
    nomSources = "sources " + nomMaladie
    tableau[nomCourbe] = numpy.zeros( len( annees ) ) * pylab.nan
    tableau[nomCourbeTaux] = numpy.zeros( len( annees ) ) * pylab.nan
    if not tableau.has_key( nomSources ):
        tableau[nomSources] = []
    source = feuillePays.cell_value( numCourbe, colonneSource )
#    print "ll", source in tableau[nomSources], source, tableau[nomSources]
    fin = -1
    for col in range( 0, len( annees ) ):
        try:
            val = int( float( feuillePays.cell_value( numCourbe, col + colonnePremiereDonnee ) ) )
            tableau[ nomCourbe ][ col ] = int( val )
            if numCourbe > 2:
                tableau[ nomCourbeTaux ][ col ] = float( val ) / ( tableau['Population'][col] / 1000000 )
            else:
                tableau[ nomCourbeTaux ][ col ] = val
            if fin == -1:
                fin = premiereAnnee - col
            debut = premiereAnnee - col 
        except: ()
    numCourbe = numCourbe + 1
    precisions = nomCourbe.split( '(' )

    if len( precisions ) > 1:
        indiceCourbe = int( precisions[1][1] )
        if indiceCourbe <= 3:
            typeDeCourbe = ' ('
            premiereLettre = precisions[1][0]
            if premiereLettre == 'D':
                typeDeCourbe = ' (Mort. '
            elif premiereLettre == 'I':
                typeDeCourbe = ' (Inc. '
            elif premiereLettre == 'C':
                typeDeCourbe = ' (Couv. '        
            if not source in tableau[nomSources]:
                tableau[nomSources].append( source + typeDeCourbe + str(debut) + '-' + str(fin) + ')' )
 
print( tableau.keys() )

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)

def add_subplot_axes(ax,rect,axisbg='w'):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)    
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]
    subax = fig.add_axes([x,y,width,height],axisbg=axisbg)
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax, x_labelsize, y_labelsize

x = annees
y2 = []

#http://webarchive.nationalarchives.gov.uk/20140629102627/https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/246403/Vaccination_timeline_1796_to_2013.pdf
creation_vaccin = {}
immunisation_de_masse = {}
creation_vaccin[u'Tuberculose'] = 1921
immunisation_de_masse[u'Tuberculose'] = 1953 # UK immunization program (sinon 1950) ; BCG créé en 1909
creation_vaccin[u'Coqueluche'] = 1926
immunisation_de_masse[u'Coqueluche'] = 1957
creation_vaccin[u'Poliomyélite'] = 1956 # 1956 pour le public, 1962 pour le vaccin oral
immunisation_de_masse[u'Poliomyélite'] = 1956 # 1956 pour le public, 1962 pour le vaccin oral
creation_vaccin[u'Tétanos'] = 1926 # routine...
immunisation_de_masse[u'Tétanos'] = 1961 # routine...
creation_vaccin[u'Diphtérie'] = 1923
immunisation_de_masse[u'Diphtérie'] = 1942 # https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/416108/Diphtheria_Guidelines_Final.pdf
creation_vaccin[u'Rougeole'] = 1968 # trouvé 1963 ailleurs, à vérifier ; MMR 1988
immunisation_de_masse[u'Rougeole'] = 1968 # trouvé 1963 ailleurs, à vérifier ; MMR 1988
creation_vaccin[u'Hépatite B'] = 1981
immunisation_de_masse[u'Hépatite B'] = 1982

fleches = {}
fleches[u'Coqueluche'] = [[1926,u'Création du vaccin',0b11],[1957,u'Immunisation de masse']];
fleches[u'Diphtérie'] = [[1923,u'Création du vaccin'],[1942,u'Immunisation de masse']];
fleches[u'Hépatite B'] = [[1981,u'Création du vaccin'],[1982,u'Immunisation de masse']];
fleches[u'Poliomyélite'] = [[1956,u'Création du vaccin inactivé'],[1962,u'Création du vaccin vivant oral']];
fleches[u'Rougeole'] = [[1968,u'Création et immunisation\nde masse'], [1988,u'ROR',0b1000], [1996,u'2e dose ROR',0b1000]];
fleches[u'Scarlatine'] = [];
fleches[u'Tétanos'] = [[1926,u'Création du vaccin',0b10],[1961,u'Immunisation de masse']];
fleches[u'Tuberculose'] = [[1921,u'Création du vaccin',0b10],[1953,u'Immunisation de masse']];

couleur_deces0 = '#000066'
couleur_deces = '#0000aa'
couleur_deces2 = '#0000ff'
couleur_incidence = '#bb4444'
couleur_couverture = "g"
epaisseur_trait = 1.7

def tracer_courbes( nom_maladie, rect_gros_plan, rect_couverture, date_gros_plan, date_couverture ):
    numFigure = 0
    sources = tableau['sources ' + nom_maladie ]
    fig = plt.figure( numFigure, figsize=(15, 6.4 + len(sources)*0.16), dpi=80, facecolor = "white", linewidth = 20, edgecolor = "gray" )
    numFigure = numFigure + 1
    ax = plt.subplot(1,2,1)
    fig.get_axes()[0].annotate(nom_maladie + ' (Angleterre et Pays de Galles)', 
                               (0.5, 0.94), xycoords='figure fraction', ha='center', fontsize=16 )
        
    y_taux = tableau['taux ' + nom_maladie + ' (D1)']
    plt.plot( x, y_taux, couleur_deces, linewidth=epaisseur_trait )
    if tableau.has_key(nom_maladie + ' (D0)'):
        y0 = tableau[nom_maladie + ' (D0)']
        y0_taux = tableau['taux ' + nom_maladie + ' (D0)']
        plt.plot( x, y0_taux, couleur_deces0, linewidth=epaisseur_trait )
    else:
        print( nom_maladie + u" : pas de données avant 1900" )
        y0 = [] 
        y0_taux= []   
    if tableau.has_key(nom_maladie + ' (D2)'):
        y2 = tableau[nom_maladie + ' (D2)']
        y2_taux = tableau['taux ' + nom_maladie + ' (D2)']
        plt.plot( x, y2_taux, couleur_deces2, linewidth=epaisseur_trait )
    else:
        print(nom_maladie + u" : pas de données après 2000" )
        y2 = []
        y2_taux = []

    ymax = numpy.nanmax( y_taux )
    if y0 != []:
        ymax = numpy.nanmax( [y0_taux, y_taux] )
    plt.axis([x[premiere_donnee_valide( y0_taux, y_taux )], max(x), min(0, numpy.nanmin(y_taux)), ymax])
   
    plt.xlabel( u'Année' )
    plt.ylabel( u'Décès (par million)', color= couleur_deces )
    for fleche in fleches[nom_maladie]:
        angle = 0
        if len(fleche) > 2 and fleche[2] / 2 == 1:
            angle = 90       
        if len(fleche) <= 2 or fleche[2] / 4 == 0:    
            tracer_fleche( y_taux, fleche[0], fleche[1], angle, premiere_donnee_valide( y0_taux, y_taux ), ymax )
      
    # gros-plan 1e graphique, avec l'incidence
    nb_annees_gros_plan = premiereAnnee - date_gros_plan
    multY = 6 / fig.get_size_inches()[1] # mise à jour avec nouvelle taille de fenêtre, et tenant compte de la légende
    rect_dont_legende = [rect_gros_plan[0], (1-multY) + rect_gros_plan[1] * multY,
                         rect_gros_plan[2], rect_gros_plan[3] * multY]
    ax1, _, y_labelsize = add_subplot_axes( ax, rect_dont_legende )
    ax1.yaxis.set_tick_params(labelsize=y_labelsize)
    plt.plot( x[1:nb_annees_gros_plan], y_taux[1:nb_annees_gros_plan], couleur_deces, linewidth=epaisseur_trait )

    if y2_taux != []: 
        plt.plot( x[1:nb_annees_gros_plan], y2_taux[1:nb_annees_gros_plan], couleur_deces2, linewidth=epaisseur_trait)
   
    if tableau.has_key(nom_maladie + ' (I1)'):
        cas = tableau[nom_maladie + ' (I1)']
        cas_taux = tableau['taux ' + nom_maladie + ' (I1)']
        ax2 = ax1.twinx()
        ax2.plot(x[1:nb_annees_gros_plan], cas_taux[1:nb_annees_gros_plan], couleur_incidence, linewidth=epaisseur_trait)
        ax2.set_ylim( [0, ax2.get_ylim()[1]] )
        ax2.yaxis.set_tick_params(labelsize=y_labelsize, labelcolor=couleur_incidence)
        ax2.set_ylabel('Incidence (par million)', color=couleur_incidence)

    if tableau.has_key(nom_maladie + ' (I2)'):
        cas2_taux = tableau['taux ' + nom_maladie + ' (I2)']
        ax2.plot(x[1:nb_annees_gros_plan], cas2_taux[1:nb_annees_gros_plan], couleur_incidence, linewidth=epaisseur_trait)
    ax2.set_xlim( ax2.get_xlim()[0], annees[0] )

    # 2e graphique : couverture contre maladie
    nb_annees_couverture = premiereAnnee - date_couverture
    ax = plt.subplot(1,2,2)
    plt.xlabel( u'Année' )
    plt.ylabel( u'Décès', color=couleur_deces)
    y = tableau[nom_maladie + ' (D1)']
    ymax = numpy.nanmax( y[0:nb_annees_couverture] )
    plt.plot( x[1:nb_annees_couverture], y[1:nb_annees_couverture], couleur_deces, linewidth=epaisseur_trait )
    ax.set_ylim( [0, ax.get_ylim()[1]] )
    
    for fleche in fleches[nom_maladie]:
        angle = 0
        if len(fleche) > 2 and fleche[2] % 2 == 1:
            angle = 90
        if len(fleche) <= 2 or fleche[2] % 4 == 0:
            tracer_fleche( y, fleche[0], fleche[1], angle, nb_annees_couverture, ymax )

    if y2 != []:
        plt.plot( x[1:nb_annees_couverture], y[1:nb_annees_couverture], couleur_deces, x[1:nb_annees_couverture], y2[1:nb_annees_couverture], couleur_deces2, linewidth=epaisseur_trait )    
    
    # Incidence sur l'axe de droite
    ax2 = ax.twinx()
    ax2.yaxis.set_tick_params(labelsize=y_labelsize)
    ax2.set_ylabel( "Nombre de cas", color=couleur_incidence)
    plt.plot( x[1:nb_annees_couverture], cas[1:nb_annees_couverture], couleur_incidence, linewidth=epaisseur_trait )
    
    # Couverture vaccinale sur l'axe de droite
    ax_couv = ax.twinx()
    ax_couv.yaxis.set_tick_params(labelsize=y_labelsize)    
    ax_couv.spines["right"].set_position(("axes", 1.17)) # échelle décalée vers la droite
    make_patch_spines_invisible(ax_couv)
    ax_couv.spines["right"].set_visible(True)
    
    couv1 = []
    couv2 = []
    couv3 = []
    if tableau.has_key(nom_maladie + ' (C1)'):
        couv1 = tableau[nom_maladie + ' (C1)']
    if tableau.has_key(nom_maladie + ' (C2)'):
        couv2 = tableau[nom_maladie + ' (C2)']
    if tableau.has_key(nom_maladie + ' (C3)'):
        couv3 = tableau[nom_maladie + ' (C3)']
    legende = ''
    if couv1 != []:
        ax_couv.plot( x[1:nb_annees_couverture], couv1[1:nb_annees_couverture], "g." )
        legende = legende + u'• Couverture (%)\n'
    if couv2 != []:            
        ax_couv.plot( x[1:nb_annees_couverture], couv2[1:nb_annees_couverture], "g*")
        legende = legende + u'* Couverture 2e dose (%)\n'
    if couv3 != []:
        ax_couv.plot( x[1:nb_annees_couverture], couv3[1:nb_annees_couverture], "g-")
        legende = legende + u'- Couverture 3e dose (%)'
    
    ax_couv.set_ylabel( legende, color='g')
    plt.axis([max( 1900, min(x[1:nb_annees_couverture]) ), max(x[1:nb_annees_couverture]), 0, 100])
    annotations.legende_sources( fig, plt, sources, 0.07, 0.88 )
    plt.show()
    print "Sauvegarde de " + nom_maladie + '.svg, .jpeg et .png'
    fig.savefig( '../figures/' + nom_maladie + '.svg', transparent=False, dpi=fig.dpi )     
    fig.savefig( '../figures/autres_formats/' + nom_maladie + '.png', transparent=False, dpi=fig.dpi )     
    fig.savefig( '../figures/autres_formats/' + nom_maladie + '.jpeg', transparent=False, dpi=fig.dpi )     

def tracer_fleche( courbe, date, annotation, angle, nb_annees, ymax = -1 ):
    if ymax == -1:
        ymax = numpy.nanmax(courbe)     
    y_fleche_pointe = courbe[premiereAnnee - date] + ymax / 40 
    y_fleche_bout = courbe[premiereAnnee - date] + 3 * ymax / 40 
    if angle == 90:
        texte_x = date - 220 / nb_annees
        texte_y = y_fleche_bout + ymax / 60
    else:  
        texte_x = date
        texte_y= y_fleche_bout
    plt.annotate( "", xy=(date, y_fleche_pointe), xytext=(date, y_fleche_bout ),
                arrowprops=dict(facecolor='black', shrink=0.01, width=0.8, headwidth = 4, frac=0.3 ) )
    plt.annotate( annotation, xy=(texte_x, texte_y), rotation=angle, va="bottom" )

def premiere_donnee_valide( y0, y ):   # en quelle année (son indice) on trouve la première donnée valide pour ce graphe
    y_test = y
    if y0 != []:
        y_test = y0
    i = 0
    for val in y_test:
        if not numpy.isnan( val ):
            last_non_nan = i
        i = i + 1
    return last_non_nan
    
tracer_coqueluche = False
tracer_diphterie = False
# tracer_hepatiteB = False    # pas de données de décès
tracer_polio = False
tracer_rougeole = False
tracer_scarlatine = False   
tracer_tetanos = False  #: incidence avant 1970 ? très différent de la France
tracer_tuberculose = True #: incidence avant 1965 ? couverture ?

if( tracer_coqueluche ):
    tracer_courbes( u'Coqueluche', [0.25,0.35,0.57,0.6], [0.49,0.47,0.30,0.45], 1930, 1940 )

if( tracer_diphterie ):
    tracer_courbes( u'Diphtérie', [0.32,0.39,0.5,0.57], [0.49,0.47,0.30,0.45], 1927, 1948 )

# if( tracer_hepatiteB ):
#     tracer_courbes( u'Hépatite B', [0.37,0.39,0.5,0.57], [0.49,0.47,0.30,0.45], 1950, 1937 )

if( tracer_polio ):
    tracer_courbes( u'Poliomyélite', [0.37,0.39,0.5,0.57], [0.49,0.47,0.30,0.45], 1940, 1958 )

if( tracer_rougeole ):
    tracer_courbes( 'Rougeole', [0.37,0.29,0.45,0.67], [0.49,0.47,0.30,0.45], 1940, 1955 )

if( tracer_scarlatine ):
    tracer_courbes( u'Scarlatine', [0.2,0.29,0.57,0.67], [0.49,0.47,0.30,0.45], 1910, 1940 )

if( tracer_tetanos ):
    tracer_courbes( u'Tétanos', [0.3,0.36,0.53,0.6], [0.49,0.47,0.30,0.45], 1950, 1940 )

if( tracer_tuberculose ):
    tracer_courbes( u'Tuberculose', [0.42,0.39,0.4,0.57], [0.49,0.47,0.30,0.45], 1910, 1940 )
