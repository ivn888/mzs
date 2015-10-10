# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        parametrilin.py
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
from qgis.core import *
import sys, os, mzs, mzs_par

DEBUGMODE = True

sys.path.append(QgsProject.instance().homePath())

def formOpen(dialog,layerid,featureid):
    #definisco le variabili globali
    #global myDialog, myfeatureid, curLayer
    
    #oggetti del form
    #global ComboBoxTipo,ComboBoxInd, ComboBoxTipoPar, LineEditTipoInd 
    #global LabelValore,LabelUmisura, LineEditTipoPar
    #global LedSpessore, LedTop, LedBottom, LedQtop, LedQbottom
    #global LedTabCurve, rsTipoindagine, LayerParametri

    #variabili
    #global rsTabParametri #tab_decodifica_parametri
    #global rsTipoindagine #vettore contente i tipi indagine presenti nela layer [1:int,'ERT':text]
    #global dicTipo # dizionario del tipo indagine {int,string}
    #global rsTabParametri
    
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    rsTipoindagine=[] #vettore che contiene l'elenco dei tipi indagine
    rsTabParametri=[] #vettore che contiene l'elenco dei tipi parametri
    
    # assegno gli oggetti della combo
    ComboBoxTipoPar = myDialog.findChild(QComboBox,"tipo_parpucmb")
    ComboBoxInd = myDialog.findChild(QComboBox,"pkey_indln")
    LineEditTipoInd = myDialog.findChild(QLineEdit,"tipo_ind_txt")
    LineEditTipoPar= myDialog.findChild(QLineEdit,"tipo_parln")
    LabelValore = dialog.findChild(QLabel,"lblValore")
    LabelUmisura = dialog.findChild(QLabel,"lblUmis")
    LedSpessore= myDialog.findChild(QLineEdit,"spessore")
    LedTop= myDialog.findChild(QLineEdit,"prof_top")
    LedBottom= myDialog.findChild(QLineEdit,"prof_bot")
    LedQtop= myDialog.findChild(QLineEdit,"quota_slm_top")
    LedQbottom= myDialog.findChild(QLineEdit,"quota_slm_bot")
    LedTabCurve = myDialog.findChild(QLineEdit,"tab_curve")
    LayerParametri = QgsMapLayerRegistry.instance().mapLayersByName('parametri_lineari')[0]

    #connetto i segnali	
    LedTop.editingFinished.connect(lambda: mzs.updSpessore(LedTop,LedBottom,LedSpessore))
    LedBottom.editingFinished.connect(lambda: mzs.updSpessore(LedTop,LedBottom,LedSpessore))
    LedQtop.textChanged.connect(lambda: mzs.validaQuota(LedQtop))
    LedQbottom.textChanged.connect(lambda: mzs.validaQuota(LedQbottom))
    LedQtop.editingFinished.connect(lambda: mzs.ctrlquota(LedQtop,LedQbottom))
    LedQbottom.editingFinished.connect(lambda: mzs.ctrlquota(LedQtop,LedQbottom))
    ComboBoxInd.activated.connect(lambda: mzs_par.populateComboPar(ComboBoxInd,ComboBoxTipoPar,LabelValore,LabelUmisura,LineEditTipoInd,rsTipoindagine,rsTabParametri))
    ComboBoxTipoPar.activated.connect(lambda: mzs_par.updateLineEditParametro(ComboBoxTipoPar,LabelValore,LineEditTipoPar,LabelUmisura,rsTabParametri))
    
    #LayerParametri.editingStarted.connect(lambda: mzs.chkEditState(LayerParametri, [ComboBoxTipo]))
    #LayerParametri.editingStopped.connect(lambda: mzs.chkEditState(LayerParametri, [ComboBoxTipo]))
  
    mzs.chkEditState(LayerParametri, [ComboBoxTipoPar])
    rsTipoindagine= mzs_par.readIndagini('indagini_lineari') # legge i dati dal layer 'indagini_puntuali'
    rsTabParametri= mzs_par.readTabParametri('tab_parametri_lin') # legge la tabella 'tab_parametri_pun' 
    mzs_par.populateComboPar(ComboBoxInd,ComboBoxTipoPar,LabelValore,LabelUmisura,LineEditTipoInd,rsTipoindagine,rsTabParametri) #popola la combo Parametri e aggiorna le relative etichette
    mzs_par.updateComboTipoPar(LineEditTipoPar,LineEditTipoInd,ComboBoxTipoPar,rsTabParametri,LabelValore,LabelUmisura) # all'apertura e alla modifica del Form aggiorna la combo Tipo Parametro 
