import pandas as pd
import numpy as np
from scipy.signal import lfilter
from scipy.stats import f_oneway
from statistics import stdev

class datos:
    def rutas(rutaExperimento,nombreExperimento,flag,a,b,long1,long2,long3):
        # LISTAS PARA ALMACENAR MUESTRAS POR EXPERIMENTO
        muestrasRutas = ["","","","",""]
        muestrasEsfuerzos = ["","","","",""]
        muestrasDeformacion = ["","","","",""]
        muestrasDeformacionP = ["","","","",""]
        # EXTRACCIÓN DE DATOS
        for j in range (5):
            # ASIGNACIÓN DE RUTAS
            muestraEspecif = rutaExperimento+nombreExperimento+\
                "-"+str(j+1)+'.csv'
            muestrasRutas[j] = pd.read_csv(muestraEspecif)
            # ASIGNACIÓN DE ESFUERZOS
            muestrasEsfuerzos[j] = lfilter(b,a,
                                           pd.read_csv(muestraEspecif).
                                           loc[:,'Standard force'])
            muestrasEsfuerzos[j] = muestrasEsfuerzos[j][
                ~np.isnan(muestrasEsfuerzos[j])]
            # ASIGNACIÓN DE DEFORMACIONES
            muestrasDeformacion[j] = lfilter(b,a,
                                             pd.read_csv(muestraEspecif).
                                             loc[:, 'Nominal strain'])
            muestrasDeformacion[j] = muestrasDeformacion[j][
                ~np.isnan(muestrasDeformacion[j])]
            # CÁLCULO DE DEFORMACIONES PORCENTUALES 
            # (FLAG ES PARA TOMAR EN CUENTA LA ALTURA)
            # DE LA PROBETA DEL EXPERIMENTO
            if flag == 0:
                muestrasDeformacionP[j] = lfilter(b,a,
                                                  pd.read_csv(muestraEspecif).
                                                  loc[:,'Nominal strain']/long1*100)
                muestrasDeformacionP[j] = muestrasDeformacionP[j][
                    ~np.isnan(muestrasDeformacionP[j])]
            elif flag == 1:
                muestrasDeformacionP[j] = lfilter(b,a,
                                                  pd.read_csv(muestraEspecif).
                                                  loc[:, 'Nominal strain']/long2*100)
                muestrasDeformacionP[j] = muestrasDeformacionP[j][
                    ~np.isnan(muestrasDeformacionP[j])]
            elif flag == 2:
                muestrasDeformacionP[j] = lfilter(b,a,
                                                  pd.read_csv(muestraEspecif).
                                                  loc[:, 'Nominal strain']/long3*100)
                muestrasDeformacionP[j] = muestrasDeformacionP[j][
                    ~np.isnan(muestrasDeformacionP[j])]
        # ACTUALIZACIÓN DE BANDERA DE LONGITUD
        flag += 1
        if flag == 3:
            flag = 0
        return[muestrasRutas,muestrasEsfuerzos,muestrasDeformacion,
               muestrasDeformacionP,flag]
    
    def cantidadDatos(muestrasEsfuerzo,longitud):
        for k in range(5):
            temp = muestrasEsfuerzo[k]
            longitud[k] = len(temp)
        return min(longitud)
    
    def promedios(nDatos,esfuerzo,deformacion,b,a):
        promedio_stress = np.zeros(nDatos.astype(dtype=np.int64))
        promedio_strain = np.zeros(nDatos.astype(dtype=np.int64))

        for l in range(nDatos.astype(dtype=np.int64)):
            # VARIABLES TEMPORALES PARA CADA MUESTRA
            temp_prom_val_stress_1 = esfuerzo[0][l]
            temp_prom_val_strain_1 = deformacion[0][l]
            
            temp_prom_val_stress_2 = esfuerzo[1][l]
            temp_prom_val_strain_2 = deformacion[1][l]
            
            temp_prom_val_stress_3 = esfuerzo[2][l]
            temp_prom_val_strain_3 = deformacion[2][l]
            
            temp_prom_val_stress_4 = esfuerzo[3][l]
            temp_prom_val_strain_4 = deformacion[3][l]
            
            temp_prom_val_stress_5 = esfuerzo[4][l]
            temp_prom_val_strain_5 = deformacion[4][l]
            
            # GENERACIÓN DE LAS LISTAS PROMEDIADAS
            promedio_stress[l] += (temp_prom_val_stress_1+temp_prom_val_stress_2+
                                temp_prom_val_stress_3+temp_prom_val_stress_4+
                                temp_prom_val_stress_5)/5
            
            promedio_strain[l] += (temp_prom_val_strain_1+temp_prom_val_strain_2+
                                temp_prom_val_strain_3+temp_prom_val_strain_4+
                                temp_prom_val_strain_5)/5
            
            promedio_stressFilter = lfilter(b,a,promedio_stress)
            promedio_strainFilter = lfilter(b,a,promedio_strain)

        promedio_strain = promedio_strain[~np.isnan(promedio_strain)]
        promedio_stressFilter = promedio_stressFilter[~np.isnan(promedio_stressFilter)]

        dev = stdev(promedio_stress)
        print("Desviación std: ", dev)

        return[promedio_stressFilter,promedio_strainFilter]
    
    def linealidadDatos(epsilon,sigma):
        x = np.concatenate((epsilon[0],epsilon[1],epsilon[2],epsilon[3],epsilon[4]))
        y = np.concatenate((sigma[0],sigma[1],sigma[2],sigma[3],sigma[4]))

        smooth_width = 59
        x1 = np.linspace(-3,3,smooth_width)
        norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0]) 
        y1 = (4*x1**2 - 2) * np.exp(-x1**2) / smooth_width 

        return x