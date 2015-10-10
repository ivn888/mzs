# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        indaginipun.py
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
import sys,mzs, mzs_ind

DEBUGMODE = True

sys.path.append(QgsProject.instance().homePath())

def formOpen(dialog,layerid,featureid):
    
    #definisco le variabili globali
    #global ComboBoxClasse
    #global ComboBoxTipo, LineEditTipo, LedidParametro
    #global LedFilename, PbtFile,LedSpessore, LedTop, LedBottom
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
    LedFilename= myDialog.findChild(QLineEdit,"doc_ind")
    LedSpessore= myDialog.findChild(QLineEdit,"spessore")
    LedTop= myDialog.findChild(QLineEdit,"prof_top")
    LedBottom= myDialog.findChild(QLineEdit,"prof_bot")
    LedQtop= myDialog.findChild(QLineEdit,"quota_slm_top")
    LedQbottom= myDialog.findChild(QLineEdit,"quota_slm_bot")
    BtnFile= myDialog.findChild(QPushButton,"btnFile")
    BtnApriFile= myDialog.findChild(QPushButton,"btnApriFile")
    LedIdIndagine= myDialog.findChild(QLineEdit,"pkey_indpu")
    TblParametri=myDialog.findChild(QTableWidget,"tableParametri")
    LineEditTipo= myDialog.findChild(QLineEdit,"tipo_ind")
    LayerIndagini = QgsMapLayerRegistry.instance().mapLayersByName('indagini_puntuali')[0]

    #collego i segnali
    ComboBoxClasse.activated.connect(lambda: mzs_ind.populateComboTipo(ComboBoxClasse,ComboBoxTipo,LineEditTipo,rsTipo))
    ComboBoxTipo.activated.connect(lambda: mzs_ind.updateLineEditTipo(ComboBoxTipo,LineEditTipo,rsTipo))
    LedTop.editingFinished.connect(lambda: mzs.updSpessore(LedTop,LedBottom,LedSpessore))
    LedBottom.editingFinished.connect(lambda: mzs.updSpessore(LedTop,LedBottom,LedSpessore))
    LedQtop.textChanged.connect(lambda: mzs.validaQuota(LedQtop))
    LedQbottom.textChanged.connect(lambda: mzs.validaQuota(LedQbottom))
    LedQtop.editingFinished.connect(lambda: mzs.ctrlquota(LedQtop,LedQbottom))
    LedQbottom.editingFinished.connect(lambda: mzs.ctrlquota(LedQtop,LedQbottom))
    BtnFile.clicked.connect(lambda: mzs.selectFile(LedFilename))
    BtnApriFile.clicked.connect(lambda: mzs.apriFile(LedFilename))
    #LayerIndagini.editingStarted.connect(lambda: mzs.chkEditState(LayerIndagini, [ComboBoxTipo]))
    #LayerIndagini.editingStopped.connect(lambda: mzs.chkEditState(LayerIndagini, [ComboBoxTipo]))
    
    #eseguo le funzioni alla apertura del form
    mzs.chkEditState(LayerIndagini, [ComboBoxTipo])
    LayerTipoIndagine = QgsMapLayerRegistry.instance().mapLayersByName('tab_tipoindagine_pun')[0]
    rsTipo=mzs.readTipoIndagini(LayerTipoIndagine)
    mzs_ind.populateComboTipo(ComboBoxClasse,ComboBoxTipo,LineEditTipo,rsTipo)
    mzs_ind.updateComboTipo(ComboBoxTipo,LineEditTipo,rsTipo)
  