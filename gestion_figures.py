import matplotlib.pyplot as plt

def nouvelle_figure( longueur, largeur, sources ):
    fig = plt.figure( figsize=(longueur, largeur + len(sources)*0.16), dpi=80, facecolor = "white", linewidth = 20, edgecolor = "gray" )
    plt.rcParams.update({'font.size': 12})
    return fig

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
    qualite = 120
    print("Sauvegarde de " + nom_fichier + '.svg et .png')
    fig.savefig( '../figures/' + nom_fichier + '.svg', transparent=False, dpi=qualite*2, edgecolor = "gray" )     
    fig.savefig( '../figures/autres_formats/' + nom_fichier + '.png', transparent=False, dpi=qualite )
    fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False, dpi=qualite/3 )

    return

    from PIL import Image
    size = fig.get_size_inches()[0]*fig.dpi/4, fig.get_size_inches()[1]*fig.dpi/4
    im = Image.open('../figures/autres_formats/' + nom_fichier + '.png')
    im.thumbnail(size, Image.ANTIALIAS)
    im.save('../figures/autres_formats/' + nom_fichier + '_petit.png', "PNG")
#     plt.get_current_fig_manager().resize(100,50)
#     fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False, dpi=fig.dpi ) # pour les .odt   
#     fig.savefig( '../figures/autres_formats/' + nom_fichier + '_petit.png', transparent=False ) # pour les .odt   
    