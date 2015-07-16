#verifica che la profondita top sia maggiore della profondita bottom e calcola il campo spessore come differenza di quote		
def updSpessore():
# controlla i valori dei campi quota
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

#verifica che nel campo quota vengano inseriti valori numerici
def validaQuota():
    quota=unicode(LblQuota.displayText())
    if not isfloat(quota):
        LblQuota.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
        msgBox = QMessageBox()
    else:
        LblQuota.setStyleSheet("")

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

