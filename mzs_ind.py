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

def populateComboTipo(ComboBoxClasse,ComboBoxTipo,LineEditTipo,rsTipo):
    # all'apertura del form e alla selezione della cmb Classe popola i valori della cmb "Tipo"
    
    #recupero il valore contenuto nella cmbClasse
    curIndex = ComboBoxClasse.currentIndex()
    #curData= ComboBoxClasse.itemData(curIndex)
    TipoIndagine = LineEditTipo.text()
    #aggiorno i valori nella cmb Tipo
    ComboBoxTipo.clear()
    ComboBoxTipo.addItem("No Data")
    
    for row in rsTipo:
        #popolo la combo tipo con tutti gli oggetti che appartengono alla classe
        # row[1] Descrizione Indagine
        # row[2] codIndagine
        if row[3]==curIndex:
            ComboBoxTipo.addItem(row[1],row[2])

def updateComboTipo(ComboBoxTipo,LineEditTipo,rsTipo):
# Aggiorna la combo Tipo Indagine in base al valore contenuti in LineEditTipo
    #try:
        #recupero il valore della casella tipoindagine        
        CodTipoIndagine = LineEditTipo.displayText()
        
        #recupero l'elenco dei cod indagini
        elCodTipo=[]
        for i in rsTipo:
            elCodTipo.append(i[2])
        
        #popolo la combo e setto l'indice al valore corrente
        if CodTipoIndagine =='NULL' or CodTipoIndagine =='':
            ComboBoxTipo.addItem("No Data")
            ComboBoxTipo.setCurrentIndex(0)
        else:
            if CodTipoIndagine in elCodTipo:
                ComboBoxTipo.setCurrentIndex(ComboBoxTipo.findData(CodTipoIndagine))
            else:
                ComboBoxTipo.addItem("No Data")
                ComboBoxTipo.setCurrentIndex(0)
        
    #except:
    #    return False
    
def updateLineEditTipo(ComboBoxTipo,LineEditTipo,rsTipo):
    #quando viene aggiornata la combo Tipo Indagine valorizza LineEditTipo
    TipoIndagine = ComboBoxTipo.currentText()
    codIndagine=''
    for row in rsTipo:
        if row[1]==TipoIndagine:
           codIndagine=str(row[2])
           
    if codIndagine:
        LineEditTipo.setText(codIndagine)