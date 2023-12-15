import mechelastic as mec
import numpy as np
import MatPy.material_analytics as mp
import pandas
from scipy.stats import linregress

class calculos():
    def modYoung(epsilon, sigma):
        deriv1 = np.diff(sigma,1)
        deriv2 = np.diff(sigma,2)

        for i in range(len(deriv2)):
            puntoMax = [0,0]
            if deriv2[i]==0 and deriv1[i-1]<0:
                puntoMax = [epsilon[i],sigma[i]]
                break
        for i in range(len(deriv2)):
            puntoMin = [0,0]
            if deriv2[i]==0 and deriv1[i]>0:
                puntoMin = [epsilon[i],sigma[i]]
                break
        young = [puntoMin[0],puntoMax[0]]
        
        if puntoMin==[0,0] and puntoMax==[0,0]:
            modulo = 0
        else:
            modulo = (puntoMax[1]-puntoMin[1])/(puntoMax[0] - puntoMin[0])
        return modulo,young
    
    def fluencia(promStrain,promStress):
        strain = promStrain.clip(0,13)
        stress = np.zeros(len(strain-1))
        for i in range(len(stress)):
            stress[i] = promStress[i]
        modelo = mp.combine_data(strain,stress)
        return mp.yield_stress(modelo)        
    
    def esfuerzoMax(promStress,promStrain):
        for i in range(len(promStress)):
            if max(promStress) == promStress[i]:
                ref = i
                break
        puntoEsfMax = [promStrain[ref],max(promStress)]
        return max(promStress),puntoEsfMax