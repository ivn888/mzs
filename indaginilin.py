# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        indaginilin.py
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
import sys,mzs,mzs_ind

DEBUGMODE = True

sys.path.append(QgsProject.instance().homePath())

def formOpen(dialog,layerid,featureid):
    
    #definisco le variabili globali
    #global ComboBoxClasse, ComboBoxTipo, LineEditTipo, LedidParametro
    #global LedFilename, PbtFile, LedSpessore, LedTop, LedBottom
    #global LedQtop, LedQbottom, BtnApriFile, BtnApriParametri
    #global dicTipo, rsTipo, LayerIndagini

    rsTipo=[]
    dicTipo={}
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    # assegno gli oggetti della combo
    ComboBoxClasse= myDialog.findChild(QComboBox,"classe_ind")
    ComboBoxTipo= myDialog.findChild(QComboBox,"tipo_indcmb")
    LineEditTipo= myDialog.findChild(QLineEdit,"tipo_ind")
    LedidParametro= myDialog.findChild(QLineEdit,"pkey_indln")
    LedFilename= myDialog.findChild(QLineEdit,"doc_ind")
    BtnFile= myDialog.findChild(QPushButton,"btnFile")
    BtnApriFile= myDialog.findChild(QPushButton,"btnApriFile")
    LayerIndagini = QgsMapLayerRegistry.instance().mapLayersByName('indagini_lineari')[0]

    #collego i segnali
    ComboBoxClasse.activated.connect(lambda: mzs_ind.populateComboTipo(ComboBoxClasse,ComboBoxTipo,LineEditTipo,rsTipo))
    ComboBoxTipo.activated.connect(lambda: mzs_ind.updateLineEditTipo(ComboBoxTipo,LineEditTipo,rsTipo))
    BtnFile.clicked.connect(lambda: mzs_ind.selectFile(LedFilename))
    BtnApriFile.clicked.connect(lambda: mzs_ind.apriFile(LedFilename))
    #LayerIndagini.editingStarted.connect(lambda: mzs.chkEditState(LayerIndagini, [ComboBoxTipo]))
    #LayerIndagini.editingStopped.connect(lambda: mzs.chkEditState(LayerIndagini, [ComboBoxTipo]))

    #eseguo le funzioni alla apertura del form
    mzs.chkEditState(LayerIndagini, [ComboBoxTipo])
    LayerTipoIndagine = QgsMapLayerRegistry.instance().mapLayersByName('tab_tipoindagine_lin')[0]
    rsTipo=mzs.readTipoIndagini(LayerTipoIndagine)
    mzs_ind.populateComboTipo(ComboBoxClasse,ComboBoxTipo,LineEditTipo,rsTipo)
    mzs_ind.updateComboTipo(ComboBoxTipo,LineEditTipo,rsTipo)