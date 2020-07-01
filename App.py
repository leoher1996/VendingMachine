import sys
from PyQt5 import QtGui
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

import Catalog as Catalog
import VendingMachine as VM
import InitVendingMachine as InitVM
import Product as ProdFile
import Queue as  QueueFile


NoProduct  = Catalog.NoProduct


############################
#Below are included the Windows dimensions:
############################
Window_Top=0
Window_Left=0
Window_Width=1100
Window_Height=800

#Lists used later to store Product and Quantity from a set of 25 combo boxes.
#Their positions should match so, the product on comboSelectP[x] has a quantity of unit stored at comboSelectQ[x]. 
comboSelectP=[]
comboSelectQ=[]

###########################
#Function FindProductMatchP returns the corresponding product that matches the selection from the combo box selection.
###########################
def FindProductMatchP(comboSelectProduct, Pos):
	SelectedProduct=None
	for j in InitVM.InitProducts:
		if (comboSelectProduct[Pos].currentText() == j.Name):				
			SelectedProduct= j 
	return SelectedProduct

###########################
#Add_Image_As_Label is used to add a pixmap to a label.
#Args: i is the instance, it could be a Queue or a Product object.
#      label is the label in which the pixmap will be loaded into.
###########################
def Add_Image_As_Label(i,label):
	if isinstance(i,QueueFile.NewQueue):
		im = QPixmap(i.Product.LogoPath)
	if isinstance(i,ProdFile.NewProduct):
		im = QPixmap(i.LogoPath)
	label.setPixmap(im)
	label.setAlignment(Qt.AlignCenter)

############################
#This class implements the Main Window. 
#This window displays 2 buttons, one for the users to buy products and other for the machine administrator. 
############################
class WindowMain(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "Initial Screen"
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()   

	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.top, self.left, self.width, self.height)
		
		#Button widgets and label present on the window.
		buttonBuy = QPushButton("Buy", self)			#Button to buy a product. 
		buttonAdmin = QPushButton(" Administration ", self) 	#Admin to set up the vending machine products.
		MSG_Label = QLabel("Powered by Circuititos S.A.", self)	#Label to display an information message about the author.	

		#Code to set size and position for the button widgets.  
		X_border_W=150
		Y_border_W=200
		Y_Buttons_W= (Window_Height-2*Y_border_W)/2
		buttonBuy.setGeometry(X_border_W, Y_border_W, Window_Width-2*X_border_W, Y_Buttons_W)
		buttonAdmin.setGeometry(X_border_W, Y_border_W+Y_Buttons_W , Window_Width-2*X_border_W, Y_Buttons_W)

		#Code to set size and position for the label. 
		MSG_Label.move(450, 650)
		MSG_Label.adjustSize()
		
		#Code to set the buttons style.		
		buttonAdmin.setStyleSheet("background-color: Yellow; color: Black")
		buttonAdmin.setFont(QFont("Times", 40))	
		buttonBuy.setStyleSheet("background-color:Green; color: Black")	
		buttonBuy.setFont(QFont("Times", 40))
		
		#Code to assign the corresponding functions calls when pressing the buttons.
		buttonAdmin.clicked.connect(self.buttonAdmin_onClick)
		buttonBuy.clicked.connect(self.buttonBuy_onClick)
		
		self.show()

	@pyqtSlot()
	def buttonAdmin_onClick(self):	
		self.cams = WindowAdmin() #Calls the WindowAdmin window. 
		self.cams.show()
		self.close()                                   

	@pyqtSlot()
	def buttonBuy_onClick(self):	
		self.cams = WindowBuy()	#Calls the WindowBuy window. 
		self.cams.show()
		self.close()                                  




#TODO: This is the window that's being developed by willy. 
class WindowBuy(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle("[This is willy\'s window.] Select the products you want to buy.")
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()
		
		InventoryProduct =[]    #This is a list of products.
		InventoryQuantity=[]    #This is tha amount of each product
		
		for a in InitVM.vm.list:
			if (a.Product != None and a.Product != NoProduct):							
				if a.Product in InventoryProduct:				
					Inventory_Index = InventoryProduct.index(a.Product)
					InventoryQuantity[Inventory_Index]+=a.Quantity
				else: 	
					InventoryProduct.append(a.Product)
					InventoryQuantity.append(a.Quantity)

		
		for i in InventoryProduct:
				#This code adds a pixmap throught the label. 
				label = QLabel(self)				
				Add_Image_As_Label(i,label)


				Pos=InventoryProduct.index(i)
				X_pos=Pos%5
				Y_pos=Pos//5

				grid.addWidget(label,X_pos,2*Y_pos)              			
				AvailableMSG= "Available: " + str(InventoryQuantity[Pos]) + "\n" + "Cost: ₡" +  str(i.Cost)
				MSGLabel = QLabel(AvailableMSG)
				grid.addWidget(MSGLabel,X_pos, (2*Y_pos)+1)      
		self.setLayout(grid)
		self.show()




############################
#This class implements the Admin Window. 
#This window displays the current status of the vending machine.
#It displayes the corresponding picture, and some relevant info for the customer, as quantity and price 
#Also for each product adds a couple combo boxes to edit the product and the quantity
############################
class WindowAdmin(QDialog):
	def __init__(self):
		super().__init__()
		self.title= "[ADMIN]: Edit the Vending Machine products."
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()      #A grid is included to add all the widgets.

		for i in InitVM.vm.list:
				#This code adds a pixmap throught the label. 
				label = QLabel(self)				
				Add_Image_As_Label(i,label)

				X_pos=VM.get_X(i)
				Y_pos=VM.get_Y(i)

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

				#This code sets the message next to each product.				
				if i.Quantity==0:
					MSGLabel = QLabel("Empty")
				else:
					AvailableMSG= "Available: " + str(i.Quantity) + "\n" + "Cost: ₡" +  str(i.Product.Cost)
					MSGLabel = QLabel(AvailableMSG)
				
	
				grid.addWidget(MSGLabel,2*X_pos, (2*Y_pos)+1) 

		#The code below implements the -Remove All-, -Update-, -Cancel- and -Back- buttons.
		#Includes the QPushButton widgets, for each button.
		RemoveAllButton= QPushButton('Remove All', self)				
		UpdateButton= QPushButton('Update', self)
		CancelButton= QPushButton('Cancel', self)
		BackButton= QPushButton('Back', self)
		#Code to add the widgets on the grid, at the corresponding position.   
		grid.addWidget(RemoveAllButton, 11, 5)				
		grid.addWidget(UpdateButton,    11, 6)
		grid.addWidget(CancelButton,    11, 7)
		grid.addWidget(BackButton,      11, 8)
		##Code to assign the corresponding functions calls when pressing the buttons.
		RemoveAllButton.clicked.connect(self.RemoveAllButton_AdminWindow_onClick )				
		UpdateButton.clicked.connect(self.UpdateButton_AdminWindow_onClick)
		CancelButton.clicked.connect(self.CancelButton_AdminWindow_onClick)
		BackButton.clicked.connect(self.BackButton_AdminWindow_onClick)
		self.setLayout(grid)
		self.show()

	###################
	#Widget Actions for WindowAdmin:
	###################
	@pyqtSlot()
	def CancelButton_AdminWindow_onClick(self):
		self.cams = WindowAdmin()	
		self.cams.show()
		self.close()  
	@pyqtSlot()
	def UpdateButton_AdminWindow_onClick(self):
		Row= "ABCDE"
		Col= "12345"		
		for i in Row:
			for j in Col:
				Pos=VM.getListPos(i,j)			
				Product= FindProductMatchP(comboSelectP, Pos)			
				if Product != None:	
					InitVM.vm.UpdateQueue(i, int(j), Product, 2)				
				SelectedQuantity= comboSelectQ[Pos].currentText()
				CurrentP= InitVM.vm.list[Pos].Product 				
				if SelectedQuantity!="Quantity" and CurrentP != Catalog.NoProduct and CurrentP != None:
					InitVM.vm.list[Pos].Quantity= int(SelectedQuantity) 				
															
		#This code clears both lists with the combo box reads. 
		comboSelectP.clear()
		comboSelectQ.clear()
		
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()   

	@pyqtSlot()
	def RemoveAllButton_AdminWindow_onClick(self):
		InitVM.vm.ClearVM()
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()  

	@pyqtSlot()
	def BackButton_AdminWindow_onClick(self):	
		self.cams = WindowMain()	
		self.cams.show()
		self.close()  


############################
#This class implements the Catalog Window. 
#This window displays the current status of the vending machine.
#It displayes the corresponding picture, and some relevant info for the customer, as quantity and price 
############################
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
		
		for i in InitVM.vm.list:
				#This code adds a pixmap throught the label. 
				label = QLabel(self)				
				Add_Image_As_Label(i,label)
				X_pos=VM.get_X(i)
				Y_pos=VM.get_Y(i)
				grid.addWidget(label,X_pos,2*Y_pos)  
            			
				#This code sets the message next to each product.	
				if i.Quantity==0:
					MSGLabel = QLabel("Empty")
				else:
					AvailableMSG= "Available: " + str(i.Quantity) + "\n" + "Cost: ₡" +  str(i.Product.Cost)
					MSGLabel = QLabel(AvailableMSG)	
				grid.addWidget(MSGLabel,X_pos, (2*Y_pos)+1)      

		buttonBack = QPushButton('Back', self) 
		buttonBack.clicked.connect(self.buttonBack_FromCatalog_ToSetUpVM_onClick)	
		grid.addWidget(buttonBack,11,2)

		self.setLayout(grid)
		self.show()

	###################
	#Widget Actions for WindowCatalog:
	###################
	@pyqtSlot()
	def buttonBack_FromCatalog_ToSetUpVM_onClick(self):	
		self.cams= WindowAdmin()			
		self.cams.show()
		self.close()  




def Invoque_GUI():	  
	app=QApplication(sys.argv)
	app.setStyle('Fusion') 
	ex=WindowMain()
	sys.exit(app.exec_())
	
#If this program is run as the main, it will invoque the GUI. 
if __name__ == '__main__':         
	Invoque_GUI()
