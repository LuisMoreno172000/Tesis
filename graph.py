import matplotlib.pyplot as plt
import numpy as np

class graficar():
    def curvas(esfuerzo,deformacion,esfuerzoProm,deformacionProm,
               nombreMuestra,claveExp,maximo,path_savefig):
        line_color = ["#3f5f2f","#aab78d","#637a30","#9cb269","#687661"]
        for p in range(5):
            plt.plot(deformacion[p],esfuerzo[p],color = line_color[p],label="Sample "
                    +str(p+1), linestyle=":")

        plt.plot(deformacionProm,esfuerzoProm,label="Mean",color="#004258")
        plt.scatter(maximo[0],maximo[1],color="#004258",label="Maximum Stress")
        # ETIQUETAS DE GRÁFICO
        plt.xlabel('Strain (%)')
        plt.ylabel('Stress (MPa)')
        #plt.title("Ensayos de Compresión \n" + "Muestra: " + 
                #nombreMuestra + "\n Resina: Biomed Clear v1")
        
        # PERZONALIZACIÓN
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.minorticks_on()
        plt.grid(which='major',linestyle='-',linewidth=0.5)
        plt.grid(which='minor',linestyle=':',linewidth=0.5)
        #plt.ylim(ymin=0,ymax=10)
        #plt.xlim(xmin=0,xmax=30)
        plt.savefig(path_savefig+claveExp+"Grafico.png",bbox_inches="tight", dpi=600)
        plt.show()

    def graficarMedias(mediaEsf,mediaDef,experimento,regionYoung,valorMod,path_savefig,archivo):
        plt.plot(mediaDef,mediaEsf,label=experimento+"\nMagnitud: "+'{:.{prec}f}'.format(valorMod, prec=2))
        # ETIQUETAS DE GRÁFICO
        plt.xlabel('Deformación (%)')
        plt.ylabel('Esfuerzo (MPa)')
        #plt.title("Region de Young en la Muestra "+str(experimento)+"\n")
        
        # PERZONALIZACIÓN
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.minorticks_on()
        plt.grid(which='major',linestyle='-',linewidth=0.5)
        plt.grid(which='minor',linestyle=':',linewidth=0.5)
        plt.axvline(regionYoung[1],0,1,linestyle=":",color="grey")
        plt.axvline(regionYoung[0],0,1,linestyle=":",color="grey")
        plt.xlim(xmin=regionYoung[0],xmax=regionYoung[1])
        plt.savefig(path_savefig+archivo,bbox_inches="tight",dpi=600)
        plt.show()