import sys
from PyQt5 import QtGui
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

import Catalog as Catalog
import VendingMachine as VM
import InitVendingMachine as InitVM
############################
CurrentProducts=InitVM.vm.list
############################

Window_Top=0
Window_Left=0
Window_Width=800
Window_Height=600

comboSelectP=[]
comboSelectQ=[]

NoProduct  = Catalog.NoProduct


def FindProductMatch(comboSelectProduct, comboSelectQuantity, Pos):
	SelectedProduct=None
	for j in InitVM.InitProducts:
		if (comboSelectProduct[Pos].currentText() == j.Name):
			#print(comboSelectProduct[Pos].currentText(), "Debe ser igual a ",  j.Name)				
			SelectedProduct= j 
	return SelectedProduct
				
	
	#		print(comboSelectProduct[i].currentText())
			#print(comboSelectQuantity[0].currentText())
	

class WindowMain(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "Powered by Circuititos S.A."
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()   
	        #self.setStyleSheet("QWidget {background-image: url(Pictures/snacks.jpg)}")

	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.top, self.left, self.width, self.height)

		buttonAdmin = QPushButton('Administration', self) 
		buttonAdmin.move(100, 100)
		buttonAdmin.clicked.connect(self.buttonAdmin_onClick)
		
		buttonBuy = QPushButton('Buy', self) 
		buttonBuy.move(100, 300)
		buttonBuy.clicked.connect(self.buttonBuy_onClick)

		self.show()

	@pyqtSlot()
	def buttonAdmin_onClick(self):	
		self.cams = WindowAdmin()	
		self.cams.show()
		self.close()                                   #Closes the window passed as self.

	@pyqtSlot()
	def buttonBuy_onClick(self):	
		self.cams = WindowBuy()	
		self.cams.show()
		self.close()                                   #Closes the window passed as self.

#This is the window that's being developed by willy. 
class WindowBuy(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle('This is willy\'s window.')
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()
		
		InventoryProduct =[]    #This is a list of products.
		InventoryQuantity=[]    #This is tha amount of each product
		for a in CurrentProducts:
			if (a.Product != None and a.Product != NoProduct):							
				if a.Product in InventoryProduct:
					#print("Into the IF")				
					Inventory_Index = InventoryProduct.index(a.Product)
					InventoryQuantity[Inventory_Index]+=a.Quantity
				else: 	
					print("Into the ELSE")
					InventoryProduct.append(a.Product)
					InventoryQuantity.append(a.Quantity)
					#print(Inventory)

		
		for i in InventoryProduct:
				im = QPixmap(i.LogoPath)
				label = QLabel(self)
				label.setPixmap(im)
				label.setAlignment(Qt.AlignCenter)
				Pos=InventoryProduct.index(i)
				X_pos=Pos//5
				Y_pos=Pos%5

				grid.addWidget(label,X_pos,2*Y_pos)              #Adding the product's Logo			
				AvailableMSG= "Available: " + str(InventoryQuantity[Pos]) + "\n" + "Cost: ₡" +  str(i.Cost)
				MSGLabel = QLabel(AvailableMSG)
				grid.addWidget(MSGLabel,X_pos, (2*Y_pos)+1)      #Adding product's Info 
		self.setLayout(grid)
		self.show()




class WindowCatalog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle('Vending Machine Products.')
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()
		for i in CurrentProducts:
				im = QPixmap(i.Product.LogoPath)
				label = QLabel(self)
				label.setPixmap(im)
				label.setAlignment(Qt.AlignCenter)
				X_pos=int(ord(i.Row)-65)
				Y_pos=int(i.Column)

				grid.addWidget(label,X_pos,2*Y_pos)              #Adding the product's Logo			
				AvailableMSG= "Available: " + str(i.Quantity) + "\n" + "Cost: ₡" +  str(i.Product.Cost)
					
				if i.Quantity==0:
					MSGLabel = QLabel("Empty")
				else:
					MSGLabel = QLabel(AvailableMSG)
					
				grid.addWidget(MSGLabel,X_pos, (2*Y_pos)+1)      #Adding product's Info 
		self.setLayout(grid)
		self.show()

class WindowAdmin(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle('ADMIN: Edit the Vending Machine products.')
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()
		for i in CurrentProducts:
				im = QPixmap(i.Product.LogoPath)
				label = QLabel(self)
				label.setPixmap(im)
				label.setAlignment(Qt.AlignCenter)
				X_pos=int(ord(i.Row)-65)
				Y_pos=int(i.Column)


				comboSelectProduct = QComboBox(self)
				comboSelectProduct.addItem("Edit Product")
				for x in InitVM.InitProducts:
					comboSelectProduct.addItem(x.Name)
								
				comboSelectQuantity = QComboBox(self)
				comboSelectQuantity.addItem("Quantity")
				for y in range(1,6):				
					comboSelectQuantity.addItem(str(y))

				comboSelectP.append(comboSelectProduct)
				comboSelectQ.append(comboSelectQuantity)

				grid.addWidget(label,2*X_pos,2*Y_pos)           
				grid.addWidget(comboSelectProduct,(2*X_pos)+1,2*Y_pos)      	
				grid.addWidget(comboSelectQuantity,(2*X_pos)+1,(2*Y_pos)+1)		
				AvailableMSG= "Available: " + str(i.Quantity) + "\n" + "Cost: ₡" +  str(i.Product.Cost)
					
				if i.Quantity==0:
					MSGLabel = QLabel("Empty")
				else:
					MSGLabel = QLabel(AvailableMSG)
					
				grid.addWidget(MSGLabel,2*X_pos, (2*Y_pos)+1)   
				UpdateButton= QPushButton('Update', self)
				CancelButton= QPushButton('Cancel', self)
				BackButton= QPushButton('Back', self)
				PreviewButton= QPushButton('Preview', self)   

				grid.addWidget(PreviewButton, 11, 5)				
				grid.addWidget(UpdateButton,  11, 6)
				grid.addWidget(CancelButton,  11, 7)
				grid.addWidget(BackButton,    11, 8)

				UpdateButton.clicked.connect(self.UpdateButton_UpdateWindow_onClick)
				CancelButton.clicked.connect(self.CancelButton_UpdateWindow_onClick)
				PreviewButton.clicked.connect(self.PreviewButton_UpdateWindow_onClick)
				BackButton.clicked.connect(self.BackButton_UpdateWindow_onClick)
		self.setLayout(grid)
		self.show()
	@pyqtSlot()
	def CancelButton_UpdateWindow_onClick(self):
		self.cams = WindowAdmin()	
		self.cams.show()
		self.close()  
	@pyqtSlot()
	def UpdateButton_UpdateWindow_onClick(self):
		Row= "ABCDE"
		Col= "12345"		
		for i in Row:
			for j in Col:
				Pos=VM.getListPos(i,j)			
				Product= FindProductMatch(comboSelectP, comboSelectQ, Pos)			
				if Product != None:	
					InitVM.vm.UpdateQueue(i, int(j), Product, 2)						
		CurrentProducts=InitVM.vm.list
		print("I pressed update Button")				
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()   
	@pyqtSlot()
	def PreviewButton_UpdateWindow_onClick(self):
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()  
	@pyqtSlot()
	def BackButton_UpdateWindow_onClick(self):	
		self.cams = WindowMain()	
		self.cams.show()
		self.close()             


def Invoque_GUI():	  
	app=QApplication(sys.argv)
	app.setStyle('Fusion') 
	ex=WindowMain()
	sys.exit(app.exec_())
	

if __name__ == '__main__':         #If this program is run as the main. 
	Invoque_GUI()
