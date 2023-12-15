import numpy as np
import analisis as an
import graph
import propmec
import pandas as pd
from scipy.stats import sem

# DEFINICIÓN DE RUTAS
path_S = 'C:/Users/luism/OneDrive/Documentos/Lic. Tecnologia/Proyecto Tesis/2 Pruebas mecanicas/Resultados Pruebas Mecánicas/Tension Biomed Clear v1'

# VARIABLES DE RUTAS Y NOMENCLATURAS
experimentos = [path_S]
    
experimentos_name = ["/Muestra"]
    
experimentos_key = ["Muestra"]
    
muestras_name = ["Muestra"]
listaEsfMax = np.zeros(9)
listaModE = np.zeros(9)
listaStress = [
    np.array(1)
]
listaStrain = [
    np.array(1)
]
cont_StrainP = 0
ruidoA = 1
ruidoB = [1.0/20]*20
"""
ITERACIÓN PRINCIPAL:
En esta sección se realizan las iteraciones general sobre las rutas principales
de cada experimento realizado. Las rutas principales contienen la información
de las 5 muestras de cada experimento, ordenadas en carpetas, cada muestra se
extrae individualemente en iteraciones anidadas a la principal. 
"""
for i in range(len(experimentos)):
    """
    EXTRACCIÓN DE MUESTRAS E INFORMACIÓN:
    Se obtiene la información de cada una de las muestras almacenadas en la 
    carpeta principal, es decir, las muestras 1, 2, 3, 4 y 5. De cada una de 
    ellas se obtiene la información del esfuerzo y deformación en cada punto.
    Esta información se almacena en variables a través del comando exec(). 
    También se extraen los datos necesarios para el cálculo de las propiedades
    mecánicas.
    """
    # INICIALIZACIÓN DE VARIABLES
    muestras_paths = ""
    # ASIGNACIÓN DE RUTAS DE ARCHIVO CSV
    [rutaPrincipal,rutaEsfuerzo, rutaDeformacion, rutaDeformacionP,cont_StrainP
    ] = an.datos.rutas(experimentos[i],experimentos_name[i],cont_StrainP,ruidoA,ruidoB,
                       long1=20,long2=20,long3=20)


    """
    CÁLCULO DE N PARA LOS DATOS DE PROMEDIO:
    Se obtiene la longitud necesaria para graficar la curva promedio de las 
    5 muestras. Dicha longitud corresponde al tamaño de muestra más pequeño 
    de las listas de esfuerzo para las 5 muestras. De usarse cualquier otro
    tamaño, los datos serían insuficientes para graficar.
    """
    dataframe_len = np.zeros(5)    
    min_len = an.datos.cantidadDatos(rutaEsfuerzo,dataframe_len)

    
    """
    ITERACIÓN PARA PROMEDIAR LOS VALORES DE ESFUERZO Y DEFORMACIÓN:
    Se extraen los datos de esfuerzo y deformación de cada muestra en variables
    temporales y se promedian con sus datos correspondientes, almacenándolos 
    en una varible nueva.
    """
    [promedio_stress,promedio_strain] = an.datos.promedios(
        min_len,rutaEsfuerzo,rutaDeformacionP,b=ruidoB,a=ruidoA)
    listaStrain[i] = promedio_strain
    listaStress[i] = promedio_stress


    """
    PROPIEDADES MECÁNICAS:
    Cálculo de las propiedades mecánicas de los experimentos
    """  
    # MODULO DE YOUNG EN EL PROMEDIO
    young,region= propmec.calculos.modYoung(promedio_strain,promedio_stress)
    print("Modulo de Young: "+str(young))
    print("Región de young: "+str(region))

    # MODULO DE YOUNG ERROR
    youngMuestras = np.zeros(5)
    for j in range(5):
        youngMuestras[j],regiontemp = propmec.calculos.modYoung(
            rutaDeformacionP[j],rutaEsfuerzo[j])
    youngErrArr = youngMuestras[~np.isnan(youngMuestras)]
    youngMuestrasMedia = sum(youngMuestras)/len(youngMuestras)
    print("Young muestras:\n", youngErrArr)
    errorYoung = sem(youngErrArr)
    print("Error en el Módulo de Young: "+str(errorYoung))

    # ESFUERZO MÁXIMO
    esfuerzoMax,puntoEsfMax = propmec.calculos.esfuerzoMax(promedio_stress,
                                                           promedio_strain)
    print("Esfuerzo Máximo: ",esfuerzoMax)
    listaEsfMax[i] = esfuerzoMax

    # ESFUERZO MAXIMO ERROR
    sigmaMaxMuestras = np.zeros(5)
    for j in range(5):
        sigmaMaxMuestras[j],puntoEsfTemp = propmec.calculos.esfuerzoMax(
            rutaEsfuerzo[j],rutaDeformacionP[j])
    sigmaErrArr = sigmaMaxMuestras[~np.isnan(sigmaMaxMuestras)]
    sigmaMaxMuestrasMedia = sum(sigmaMaxMuestras)/len(sigmaMaxMuestras)
    errorSigmaMax = sem(sigmaErrArr)
    print("Error en el Esfuerzo Máximo: "+str(errorSigmaMax))


    """
    CURVAS:
    Generación y almacenamiento de los archivos de curvas esfuerzo deformación de los 
    experimentos realizados
    """
    
    path_savefig_Solida = "C:/Users/luism/OneDrive/Documentos/Lic. Tecnologia/Proyecto Tesis/2 Pruebas mecanicas/Resultados Pruebas Mecánicas/Compresion Biomed Clear v1/Python/GraficosTension/"
    graph.graficar.curvas(rutaEsfuerzo,rutaDeformacionP,promedio_stress,
                          promedio_strain,muestras_name[i],experimentos_key[i],
                          puntoEsfMax,path_savefig_Solida)  
    graph.graficar.graficarMedias(listaStress[i],listaStrain[i],muestras_name[i],
                                  regionYoung=region,valorMod=young,path_savefig=path_savefig_Solida,
                                  archivo="RegionYoung"+str(muestras_name[i]+".tiff"))
    