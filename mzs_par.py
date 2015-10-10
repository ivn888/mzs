# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        mzs.py
# Purpose:
#
# Author:      Luca Lanteri Arpa Piemonte
#
# Created:     05-10-2015
# Copyright:   (c) Luca Lanteri 2015
# Licence:     <GPL>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis.core import QgsMapLayerRegistry
from qgis.core import *
import sys, os

DEBUGMODE = True

#__all__=["validaQuota"]

def readIndagini(tabella):
# legge i dati dal layer 'indagini_puntuali' e li carica in rsTipoindagine
    
    rsTipoindagine=[]    
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName(tabella)[0]
    #recupero gli attributi delle features
    #[1] pkindpu - int
    #[3] tipoindagine - str (ERT)
    #[4] ID_INDPU - str 
       
    for i in aLayer.getFeatures():
        alist=[i.attributes()[1],i.attributes()[3],i.attributes()[4]]
        rsTipoindagine.append(alist)
    return rsTipoindagine
    
def readTabParametri(tabella):
# legge i dati dalla tabella di decodifica 'tab_parametri_pun' in rsTabParametri
    
    rsTabParametri=[]   
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName(tabella)[0]
    
    # recupero gli attributi delle features
    #[3] Tipo ind - str (SPT)
    #[4] descPar - str (prova penetrometrica)
    #[5] Par - str (cu)
    #[6] TipoPar - str (CU) 
    #[7] Umisura - stre (Mpa)
      
    alist=[]
    for i in aLayer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
        alist=[i.attributes()[3],i.attributes()[4],i.attributes()[5],i.attributes()[6],i.attributes()[7]]
        rsTabParametri.append(alist)
    return rsTabParametri
    
def populateComboPar(ComboBoxInd,ComboBoxTipoPar,LabelValore,LabelUmisura,LineEditTipoInd,rsTipoindagine,rsTabParametri):
# quando viene aggiornata la combo Indagine popola la combo Tipo Parametri 
# e mette le etichette a null
    
    #leggo codice e tipo della indagine puntuale selezionata 
    #carico il valore di id_indpu selezionato nella combo
    Indagine = ComboBoxInd.currentText()
    
    tipo_ind=''
    # cerco il tipo indagine corrispondente a id_indpu
    for row in rsTipoindagine:
        if row[2]==Indagine:
            tipo_ind=row[1]
            break
        
    # aggiorno i valori nella combobox Tipo
    ComboBoxTipoPar.clear()
    ComboBoxTipoPar.addItem("No Data")
    #popola ComboBoxTipoPar con tutti i valori validi per il tipo di indagine
    for row in rsTabParametri:
        if row[0]==tipo_ind:  # se il tipo indagine e uguale a quello contenuto in rsTabParametri 
            ComboBoxTipoPar.addItem(row[1],row[2]) # aggiungi la voce a ComboBoxTipoPar
            LineEditTipoInd.setText(row[0]) 
    
    #azzera le etichette
    LabelValore.setText('---')
    LabelUmisura.setText('---')
    
def updateLineEditParametro(ComboBoxTipoPar,LabelValore,LineEditTipoPar,LabelUmisura,rsTabParametri):
# quando viene aggiornata la combo Tipo Parametri popola le etichette tipoParametro
    
    nomePar = ComboBoxTipoPar.currentText()
   
    for row in rsTabParametri:
        if row[1]==nomePar:
            LineEditTipoPar.setText(row[3])
            if row[2]:
                LabelValore.setText(row[1])
            else:
                LabelValore.setText('---')
            if row[3]:
                LabelUmisura.setText('['+row[4]+']')
            else:
                LabelUmisura.setText('---')    


def updateComboTipoPar(LineEditTipoPar,LineEditTipoInd,ComboBoxTipoPar,rsTabParametri,LabelValore,LabelUmisura):
# all'apertura e alla modifica del Form aggiorna la combo Tipo Parametro e le etichette
    #try:
        val=None
        codParametro = LineEditTipoPar.displayText() # tipo_parametro
        codIndagine = LineEditTipoInd.displayText() # tipo_parametro
        for row in rsTabParametri:
            if (row[3]==codParametro and row[0]==codIndagine):
                val=row[1]
                break
            else:
                val='No Data'

        if val:
            index=ComboBoxTipoPar.findText(val)
        #print valtxt
        #print index

        if codParametro =='NULL' or codParametro =='':
            ComboBoxTipoPar.setCurrentIndex(0)
        else:
            ComboBoxTipoPar.setCurrentIndex(index)

        for row in rsTabParametri:
            if row[3]==codParametro:
                par=row[1]
                Umis=row[4]
            else:
                par='--'
                Umis='--'

        LabelValore.setText(par)
        LabelUmisura.setText('['+Umis+']')

    #except:
        #print "Unexpected error - updateComboTipoPar"