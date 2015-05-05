import matplotlib.pyplot as plt

def legende_sources( fig, plt, liste_sources, marge_gauche=0.1, marge_droite=0.92 ):
    numSource = 0
    multX = fig.get_size_inches()[0] / 15
    plt.annotate( "Sources:",
                  (0.02 / multX, 0.03 + 0.02 * len(liste_sources)), weight='bold', xycoords='figure fraction', fontsize=8 )
    for source in reversed( liste_sources ):
        plt.annotate( source, (0.062 / multX, 0.05 + 0.02 * numSource), xycoords='figure fraction', fontsize=8 )
        numSource += 1    
    fig.subplots_adjust( left=marge_gauche, right=marge_droite, bottom = 0.15 + len( liste_sources ) * 0.02 )
    plt.annotate( "Figures sous licence LGPL\nCode : https://github.com/loindutroupeau\nloindutroupeau.blogspot.fr",
                  (0.95, 0.05), horizontalalignment='right', xycoords='figure fraction', fontsize=9 )     

def sauvegarde_figure( fig, nom_fichier ):
    print("Sauvegarde de " + nom_fichier + '.svg et .png')
    fig.savefig( '../figures/' + nom_fichier + '.svg', transparent=False, dpi=fig.dpi, edgecolor = "gray" )     
    fig.savefig( '../figures/autres_formats/' + nom_fichier + '.png', transparent=False )
#     from pylab import rcParams
#     rcParams['figure.figsize'] = 5, 10
    plt.get_current_fig_manager().resize(100,50)
    fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False, dpi=fig.dpi ) # pour les .odt   
#     fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False ) # pour les .odt   
    