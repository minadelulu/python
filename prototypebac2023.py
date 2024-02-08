from PyQt5.QtWidgets import *
from PyQt5.uic import *
from pickle import dump,load

def verif(ch):
    i=0
    while i<len(ch) and (('A'<=ch[i].upper()<='Z') or ('0'<=ch[i]<='9')):
        i=i+1
    return (i==len(ch)) and (len(ch)<10)


def ajouter():
    if w.id.text()=='' or w.tel.text()=='':
        QMessageBox.information(w,'information','veuillez saisir toutes les informations')
    elif not(verif(w.id.text())):
        QMessageBox.critical(w,'Erreur','Identifiant invalide')
    elif not(len(w.tel.text())==8 and w.tel.text().isdecimal()):
        QMessageBox.critical(w,'Erreur','numéro de téléphone invalide')
    else:
        f=open('clients.dat','ab')
        e={}
        e['id']=w.id.text()
        e['tel']=w.tel.text()
        e['ville']=w.ville.currentText()
        if w.M.isChecked():
            e['genre']='Masculin'
        else:
            e['genre']='Feminin'
        if w.etat.isChecked():
            e['etat']='Inscrit'
        else:
            e['etat']='Non Inscrit'
        dump(e,f)
        f.close()
        QMessageBox.information(w,'information','le client est ajouté(e)')
        w.id.setText('')
        w.tel.setText('')
        

def affclient():
    f=open('clients.dat','rb')
    w.t.setRowCount(0)
    fin=False
    l=0
    while not (fin):
        try:
            e=load(f)
            w.t.insertRow(l)
            w.t.setItem(l,0,QTableWidgetItem(e['id']))
            w.t.setItem(l,1,QTableWidgetItem(e['tel']))
            w.t.setItem(l,2,QTableWidgetItem(e['ville']))
            w.t.setItem(l,3,QTableWidgetItem(e['genre']))
            w.t.setItem(l,4,QTableWidgetItem(e['etat']))
            l=l+1
        except:
            fin=True
    f.close()

def afficherchance():
    w.lchance.clear()
    ft=open("chance.txt","r")
    ch=ft.readline()
    while ch!="":
        w.lchance.addItem(ch)
        ch=ft.readline()
    
    ft.close()
    


def affichergagnant():
    w.lgagnant.clear()
    f=open("clients.dat","rb")
    fin=False
    w.lgagnant.addItem("les clients gagnants sont: ")
    while not(fin):
        try:
            e=load(f)
            x=somme(e['tel'])
            if recherche(x):
                w.lgagnant.addItem("identifiant:"+e['id']+"-N° Téléphone: "+e['tel'])
        except:
            fin=True
    f.close()


def somme(ch):
    while (len(ch)!=1):
        s=0
        for i in range(len(ch)):
            s=s+int(ch[i])
        ch=str(s)
    return s


def recherche(x):
    ft=open("chance.txt","r")
    ch=ft.readline()[:-1]
    trouve=False
    while ch!="" and trouve==False:
        trouve=(x==int(ch))
        ch=ft.readline()[:-1]
    ft.close()
    return trouve


#-----------------------Exploitation de l'interface graphique-------------
app=QApplication([])
w=loadUi("prototype2023.ui")
w.show()
w.ajouter.clicked.connect(ajouter)
w.afficher_client.clicked.connect(affclient)
w.afficher_chance.clicked.connect(afficherchance)
w.afficher_gagnant.clicked.connect(affichergagnant)
app.exec_()