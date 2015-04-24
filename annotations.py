def legende_sources( fig, plt, liste_sources ):
    numSource = 0
    multX = fig.get_size_inches()[0] / 15
    plt.annotate( "Sources:",
                  (0.02 / multX, 0.03 + 0.02 * len(liste_sources)), weight='bold', xycoords='figure fraction', fontsize=8 )
    for source in reversed( liste_sources ):
        plt.annotate( source, (0.062 / multX, 0.05 + 0.02 * numSource), xycoords='figure fraction', fontsize=8 )
        numSource += 1    
    fig.subplots_adjust( left=0.07, right=0.88, bottom = 0.15 + len( liste_sources ) * 0.02 )
    plt.annotate( "Figures sous licence LGPL\nCode : https://github.com/loindutroupeau\nloindutroupeau.blogspot.fr",
                  (0.95, 0.05), horizontalalignment='right', xycoords='figure fraction', fontsize=9 )     
