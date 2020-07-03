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
		
		#The following label implements the temperature information. 
		RoomTempMSG=("Temp: 27°C")         #Message for Room Temp products
		ColdTempMSG=("Temp: 4°C")          #Message for Room Temp products	
		if(InitVM.vm.Temp == 'C'):
			#Case when current products temperature is cold.
			MSG_To_Display_Temp = ColdTempMSG	
		else:
			#Case when current products temperature is room.
			MSG_To_Display_Temp = RoomTempMSG
		MSG_Temp = QLabel(MSG_To_Display_Temp, self)	#Label to display temperature info.



		#Code to set size and position for the button widgets.  
		X_border_W=150
		Y_border_W=200
		Y_Buttons_W= (Window_Height-2*Y_border_W)/2
		buttonBuy.setGeometry(X_border_W, Y_border_W, Window_Width-2*X_border_W, Y_Buttons_W)
		buttonAdmin.setGeometry(X_border_W, Y_border_W+Y_Buttons_W , Window_Width-2*X_border_W, Y_Buttons_W)

		#Code to set size and position for the labels. 
		#Powered by label.
		MSG_Label.move(450, 650)
		MSG_Label.adjustSize()
		#Temperature label
		InitX , InitY, Width, Height = 750, 40, 250, 100 
		MSG_Temp.setGeometry(InitX , InitY, Width, Height)		
		MSG_Temp.setFont(QFont("Times", 35))

		#Code to set the buttons style.		
		buttonAdmin.setStyleSheet("background-color: Yellow; color: Black")
		buttonAdmin.setFont(QFont("Times", 40))	
		buttonBuy.setStyleSheet("background-color:Green; color: Black")	
		buttonBuy.setFont(QFont("Times", 35))
		
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
############################
#This class implements the Buy Window. 
#This window allows the user to buy products.  
############################
class WindowBuy(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.top = Window_Top
		self.left = Window_Left 
		self.width = Window_Width
		self.height = Window_Height
		self.InitUI()
	def InitUI(self):
		self.setWindowTitle("Select the products you want to buy.")
		self.setGeometry(self.top, self.left, self.width, self.height)

		grid = QGridLayout()
		
		#Lists used to store an inventary. They should match then InventoryQuantity[x] is the amount of products of InventoryProduct[x].
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
		if (len(InventoryProduct)==0):
			#This is the case where the vending machine is empty. 
			#A label is added, stating that the vending machine is empty. 
			MSG_NoProducts_Label = QLabel("The vending machine is empty.",self)	
			InitX , InitY, Width, Height = 250, 300, 600, 100 
			MSG_NoProducts_Label.setGeometry(InitX , InitY, Width, Height)		
			MSG_NoProducts_Label.setFont(QFont("Times", 35))			

			#The following button allows the administrator to move to the main window. 	
			BackButton= QPushButton('Back', self)
			InitX , InitY, Width, Height = 50, 720, 100, 50 
			BackButton.setGeometry(InitX , InitY, Width, Height)	
 
		else:
			#This is the case where the vending machine is not empty. 
			#A label is added with the titles on the top of the window.  
			Product_Type_Column = QLabel("Product",self)	
			grid.addWidget(Product_Type_Column,0, 0) 
			Product_Type_Column.setAlignment(Qt.AlignCenter)
			
			Info_Column = QLabel("Info",self)	
			grid.addWidget(Info_Column,0, 1)
			Info_Column.setAlignment(Qt.AlignCenter)

			Info_Column = QLabel("Select the quantity to buy",self)	
			grid.addWidget(Info_Column,0, 2)
			Info_Column.setAlignment(Qt.AlignCenter)

			for i in InventoryProduct:
				#This code adds a pixmap throught the label. 
				label = QLabel(self)				
				Add_Image_As_Label(i,label)
				Pos=InventoryProduct.index(i)
				X_pos=Pos%5 +1 
				Y_pos=Pos//5  
				grid.addWidget(label,X_pos,2*Y_pos)              			
				#This code adds some useful information about each product.
				AvailableMSG= "Available: " + str(InventoryQuantity[Pos]) + "\n" + "Cost: ₡" +  str(i.Cost)
				MSGLabel = QLabel(AvailableMSG)
				MSGLabel.setAlignment(Qt.AlignCenter) #Aligns the message info at the center of the screen.
				grid.addWidget(MSGLabel,X_pos, (2*Y_pos)+1)   
				#This code adds the spin boxes to select the amount of units you want to buy.
				sp_box = QSpinBox()
				sp_box.setMinimum(0)
				sp_box.setMaximum(InventoryQuantity[Pos])
				grid.addWidget(sp_box, X_pos, (2*Y_pos)+2)
      				#sp.valueChanged.connect(self.valuechange)  				
			
				#This code sets the messages with the prices to pay				
				Price_To_Pay_Per_Product= QLabel("+ ₡0")
				grid.addWidget(Price_To_Pay_Per_Product, X_pos, (2*Y_pos)+3) 

			#This label states the total amount of money the user has to pay.				
			Price_To_Pay_Total= QLabel("Total: ₡0")
			grid.addWidget(Price_To_Pay_Total, 6, 3) 
	
			#The following button allows the user to move to the main window. 	
			BackButton= QPushButton('Back', self)	
			grid.addWidget(BackButton, 7, 0)

			#The following button allows the user to add products to a cart. 	
			BuyButton= QPushButton('Add to cart', self)	
			grid.addWidget(BuyButton, 6, 2)
			BuyButton.setStyleSheet("background-color:Yellow; color: Black")	
							
			#The following button allows the user to buy a cart. 	
			BuyButton= QPushButton('Buy cart', self)	
			grid.addWidget(BuyButton, 7, 3)
			BuyButton.setStyleSheet("background-color:Green; color: Black")	

		#Sets some information for the Back Button. 
		BackButton.clicked.connect(self.BackButton_AdminBuy_onClick)		
		BackButton.setToolTip("Back to main window.")  #Sets tooltip.
		
		#Clear lists for the following calls of this function.
		comboSelectP.clear()
		comboSelectQ.clear()
 
		self.setLayout(grid)
		self.show()
	###################
	#Widget Actions for WindowBuy:
	###################
	@pyqtSlot()
	def BackButton_AdminBuy_onClick(self):	
		self.cams = WindowMain()	
		self.cams.show()
		self.close()  



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

				#The code below is used to implement the combo box options
				#Select Product options
				comboSelectProduct = QComboBox(self)
				comboSelectProduct.addItem("Edit Product")
				for x in InitVM.InitProducts:
					comboSelectProduct.addItem(x.Name)
				comboSelectProduct.addItem("Empty")
				#Select Quantity options				
				comboSelectQuantity = QComboBox(self)
				comboSelectQuantity.addItem("Quantity")
				for y in range(1,6):				
					comboSelectQuantity.addItem(str(y))

				grid.addWidget(label,2*X_pos,2*Y_pos)           
				grid.addWidget(comboSelectProduct,(2*X_pos)+1,2*Y_pos)      	
				grid.addWidget(comboSelectQuantity,(2*X_pos)+1,(2*Y_pos)+1)
				
				#Code to include combo box widgets, and read from them as required.
				comboSelectP.append(comboSelectProduct)
				comboSelectQ.append(comboSelectQuantity)

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
		
		#The following button allows the administrator to change the product type.	
		ProductTypeSelectButton= QPushButton('Change Product Type', self)
		grid.addWidget(ProductTypeSelectButton, 12, 10)
		ProductTypeSelectButton.clicked.connect(self.ProductTypeSelect_AdminWindow_onClick)

		#Code below assigns some tooltips to the buttons
		RemoveAllButton.setToolTip("Remove all products.")				
		UpdateButton.setToolTip("Update current products.")
		CancelButton.setToolTip("Clear the current selection.")
		BackButton.setToolTip("Back to main window.")
		if(InitVM.vm.Temp == 'C'):
			Change_Temp_MSG= "Change product type to: Room [27°C]"
		else: 
			Change_Temp_MSG= "Change temperature to: Cold [4°C]"
		ProductTypeSelectButton.setToolTip(Change_Temp_MSG)
		
		
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
		#The following set of fors goes throught all the Queues of the vending machine. 
		Row= "ABCDE"
		Col= "12345"		
		for i in Row:
			for j in Col:
				Pos=VM.getListPos(i,j)		                          #Gets a [0,24] position.	
					
				SelQuantity= comboSelectQ[Pos].currentText()		  #Returns a the quantity selected in the combo box for widget at [Pos].
				SelProduct= comboSelectQ[Pos].currentText()		  #Returns a the product selected in the combo box for widget at [Pos].
				Product= FindProductMatchP(comboSelectP, Pos)		  #Returns the product instance selected in the combo box, or None				
				CurrentP= InitVM.vm.list[Pos].Product 		  	  #Reads the current product and returns it on CurrentP.		

				#Case when a queue is empty and a NewProduct is added. 
				if CurrentP == Catalog.NoProduct:
					if Product != None:
						if SelQuantity != "Quantity":	
							InitVM.vm.UpdateQueue(i, int(j), Product, int(SelQuantity))	
				#Case when the queue already has elements. 				
				else:
					if Product != None:		
						if SelQuantity!="Quantity":			
							#Modify the quantity and the Product	
							InitVM.vm.UpdateQueue(i, int(j), Product, int(SelQuantity))	
						else:   
						
							#Just modify the product, not the quantity. 
							InitVM.vm.UpdateQueue(i, int(j), Product, InitVM.vm.list[Pos].Quantity)
	
					else:   #Case when the selection is not a product. 
						if comboSelectP[Pos].currentText() == "Edit Product":
							#Just modify the quantity, not the product.
							if SelQuantity!="Quantity":				
								InitVM.vm.UpdateQueue(i, int(j), CurrentP, int(SelQuantity))
						#case when the selected product is "Empty"						
						else:
							InitVM.vm.UpdateQueue(i, int(j), Catalog.NoProduct, 0)															
		#This code clears both lists with the combo box reads. 
		comboSelectP.clear()
		comboSelectQ.clear()
		
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()   

	@pyqtSlot()
	def RemoveAllButton_AdminWindow_onClick(self):
		#This code clears both lists with the combo box reads and also the vending machine products.
		comboSelectP.clear()
		comboSelectQ.clear()
		InitVM.vm.ClearVM()
	 
		self.cams = WindowCatalog()	
		self.cams.show()
		self.close()  

	@pyqtSlot()
	def BackButton_AdminWindow_onClick(self):	
		self.cams = WindowMain()	
		self.cams.show()
		self.close()  

	@pyqtSlot()
	def ProductTypeSelect_AdminWindow_onClick(self):		
		if(InitVM.vm.Temp == 'C'):
			#Case when current products temperature is cold.
			InitVM.vm.Temp = 'R'
			InitVM.InitProducts = InitVM.InitProducts_Room
			
		else:
			#Case when current products temperature is room.
			InitVM.vm.Temp = 'C'
			InitVM.InitProducts = InitVM.InitProducts_Cold
		#This code clears both lists with the combo box reads and also the vending machine products.
		comboSelectP.clear()
		comboSelectQ.clear()
		InitVM.vm.ClearVM()
		
		self.cams = WindowAdmin()	
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
		self.setWindowTitle('Vending Machine Current Products.')
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
		#This Back button is used to get out of the catalog window, to a previous window.  
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
