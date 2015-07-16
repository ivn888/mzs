from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
# from qgis.core import QgsMapLayerRegistry
from qgis.core import *

DEBUGMODE = True

myDialog = None
myfeatureid = None
curLayer = None

def formOpen(dialog,layerid,featureid):
    #definisco le variabili globali
    global myDialog, myfeatureid, curLayer
    #oggetti del form
    global ComboBoxTipo,ComboBoxInd, ComboBoxTipoPar, LineEditTipoInd 
    global LabelValore,LabelUmisura, LineEditTipoPar
    global LedSpessore, LedTop, LedBottom, LedQtop, LedQbottom
    global LedTabCurve

    #variabili
    global rsTabParametri #tab_decodifica_parametri
    global rsTipoindagine #vettore contente i tipi indagine presenti nela layer [1:int,'ERT':text]
    global dicTipo # dizionario del tipo indagine {int,string}
    
    curLayer=layerid
    myDialog =dialog
    myfeatureid=featureid
    
    # assegno gli oggetti della combo
    ComboBoxTipoPar = myDialog.findChild(QComboBox,"tipo_parpucmb")
    ComboBoxInd = myDialog.findChild(QComboBox,"pkey_indpu")
    LineEditTipoInd = myDialog.findChild(QLineEdit,"tipo_ind_txt")
    LineEditTipoPar= myDialog.findChild(QLineEdit,"tipo_parpu")
    LabelValore = dialog.findChild(QLabel,"lblValore")
    LabelUmisura = dialog.findChild(QLabel,"lblUmis")
    LedSpessore= myDialog.findChild(QLineEdit,"spessore")
    LedTop= myDialog.findChild(QLineEdit,"prof_top")
    LedBottom= myDialog.findChild(QLineEdit,"prof_bot")
    LedQtop= myDialog.findChild(QLineEdit,"quota_slm_top")
    LedQbottom= myDialog.findChild(QLineEdit,"quota_slm_bot")
    BtnFileTabella = myDialog.findChild(QPushButton,"btnFileTabella")
    LedTabCurve = myDialog.findChild(QLineEdit,"tab_curve")
    
    LedTop.editingFinished.connect(updSpessore)
    LedBottom.editingFinished.connect(updSpessore)
    LedQtop.editingFinished.connect(ctrlquota)
    LedQbottom.editingFinished.connect(ctrlquota)
    ComboBoxInd.activated.connect(updateComboInd)
    ComboBoxTipoPar.activated.connect(updateComboTipoPar)
    BtnFileTabella.clicked.connect(selectFile)
 
    if curLayer.isEditable():
        ComboBoxTipoPar.setEnabled(True)
    else:
       ComboBoxTipoPar.setEnabled(False)
    
    readTabParametri() # legge la tabella 'tab_parametri_pun'
    readIndagine() # legge i dati dal layer 'indagini_puntuali'
    updateComboInd() #popola la combo Parametri e aggiorna le relative etichette
    readComboTipoPar() # all'apertura e alla modifica del Form aggiorna la combo Tipo Parametro
    #updateComboTipoPar #popola le etichette tipoParametro
    	
def readTabParametri():
# legge i dati dalla tabella di decodifica 'tab_parametri_pun' in rsTabParametri
    global rsTabParametri   
    
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName('tab_parametri_pun')[0]
    
    # recupero gli attributi delle features
    lista=[]
    rsTabParametri=[] # vettore contenente la tabella 'tab_parametri_pun'
    
    for i in aLayer.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
        alist=[i.attributes()[3],i.attributes()[4],i.attributes()[5],i.attributes()[6],i.attributes()[7]]
        rsTabParametri.append(alist)

def readIndagine():
# legge i dati dal layer 'indagini_puntuali' e li carica in rsTipoindagine
    global rsTipoindagine
    
    aLayer = QgsMapLayerRegistry.instance().mapLayersByName('indagini_puntuali')[0]
    #recupero gli attributi delle features
    rsTipoindagine=[]
    
    for i in aLayer.getFeatures():
        alist=[i.attributes()[1],i.attributes()[3],i.attributes()[4]]
        rsTipoindagine.append(alist)

def updateComboInd():
# quando viene aggiornata la combo Indagine popola la combo Tipo Parametri 
# e mette le etichette a null

    #carico il valore id id_indpu selezionato nella combo
    id_indpu_cur = ComboBoxInd.currentText()
    tipo_ind=''
        
    # cerco il tipo indagine corrispondente a id_indpu
    for row in rsTipoindagine:
        if row[2]==id_indpu_cur:
            tipo_ind=row[1]          
            break
            
    # aggiorno i valori nella combobox Tipo
    ComboBoxTipoPar.clear()
    ComboBoxTipoPar.addItem("No Data")
    
    #popola ComboBoxTipoPar con tutti i valori validi per il tipo di indagine
    for row in rsTabParametri:
        if row[0]==tipo_ind:  # se il tipo indagine e uguale a quello contenuto in  rsTabParametri 
            ComboBoxTipoPar.addItem(row[1]) # aggiungi la voce a ComboBoxTipoPar
            LineEditTipoInd.setText(row[0]) 
    
    #azzera le etichette
    LabelValore.setText('---')
    LabelUmisura.setText('---')
          
def updateComboTipoPar():
# quando viene aggiornata la combo Tipo Parametri popola le etichette tipoParametro
    
    dicTipo={} 
    valtxt = ComboBoxTipoPar.currentText()
    
    x=1
    for row in rsTabParametri:
        if row[1]==valtxt:
            LineEditTipoPar.setText(row[3])
            dicTipo[row[3]]=x
            x=x+1
            if row[2]:
                LabelValore.setText(row[1])
            else:
                LabelValore.setText('---')
            if row[3]:
                LabelUmisura.setText('['+row[4]+']')
            else:
                LabelUmisura.setText('---')
 
def readComboTipoPar():
# all'apertura e alla modifica del Form aggiorna la combo Tipo Parametro e le etichette
    try:
        valtxt = LineEditTipoPar.displayText() # tipo_parametro
        for row in rsTabParametri:
            if row[3]==valtxt:
                val=row[1]
               
        index=ComboBoxTipoPar.findText(val)
        #print valtxt
        #print index        
        
        if valtxt =='NULL' or valtxt =='':
            ComboBoxTipoPar.setCurrentIndex(0)
        else:
            ComboBoxTipoPar.setCurrentIndex(index)
    
        for row in rsTabParametri:
            if row[3]==valtxt:
                par=row[1]
                Umis=row[4]
         
        LabelValore.setText(par)
        LabelUmisura.setText('['+Umis+']')
    
    except:
        print "Unexpected error - readComboTipoPar"

#verifica che la profondita top sia maggiore della profondita bottom e calcola il campo spessore come differenza di quote		
def updSpessore():
    try:
        if (float(str(LedTop.displayText())) > (float(str(LedBottom.displayText())))):
            LedTop.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            LedBottom.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
            #QMessageBox.about(myDialog, "Info", "La profondita' top deve essere minore della profondita' bottom")
            return none
        if (LedTop.displayText() != NULL) and (LedBottom.displayText() != NULL):
            LedSpessore.setText(str(float(str(LedBottom.displayText()))-float(str(LedTop.displayText() ))))
            LedTop.setStyleSheet("")
            LedBottom.setStyleSheet("")
    except:
        print "Unexpected error - updSpessore: dato nullo"

#verifica che la quota top sia maggiore della quota bottom 
def ctrlquota():
    try:
        if (float(str(LedQtop.displayText())) < (float(str(LedQbottom.displayText())))):
                LedQtop.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
                LedQbottom.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
                #msgBox = QMessageBox()
                #QMessageBox.about(myDialog, "Info", "La quota top deve essere maggiore della quota bottom")
        else:
                LedQtop.setStyleSheet("")
                LedQbottom.setStyleSheet("")
    except:
        print "Unexpected error -ctrlquota: dato nullo"
        
def selectFile():
    filename = QFileDialog.getOpenFileName()
    if filename:
        LedTabCurve.setText(filename)


