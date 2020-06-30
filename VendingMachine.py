import Queue as Queue
import Product as Product
import Catalog as Catalog

def getListPos(Row, Col):
	Pos= (int(Col)-1)
	Pos+= (5*(ord(Row)-65))   #ord() returns unicode characted represented by an integer. ('A' -> 65)
	return Pos


class NewVendingMachine:
	def __init__(self):
		self.list = []
		#Create an empty vending machine.
		Rows= "ABCDE"
		Col= "12345"		
		for i in Rows:
			for j in Col:
				self.list.append(Queue.NewQueue(i,j))
		
	def Print_Queues_Info(self):
		for x in range(0,25):		
			self.list[x].PrintQueueInfo();
			print("\n")
	
	def Add_Product_To_Queue(self,Product,Row,Col):
		Pos= getListPos(Row,Col)            #This line converts X,Y to a position 'Pos' in [0,24] range. 
		self.list[Pos].Add_Product(Product) #This line adds a product object to the queue object into list[Pos].
		#TODO: Add some flags to check if there is any issue adding the product to the queue.	


	def Remove_Product_From_Queue(self, Row, Col):
		Pos= getListPos(Row,Col)            #This line converts X,Y to a position 'Pos' in [0,24] range.
		self.list[Pos].Remove_Product()     #This line removes a product object from the queue object in list[Pos]. 
		#TODO: Add some flags to check if there is any issue removing the product to the queue.

	def Check_Availability(self, Product):
		Product_Units = 0
		for Pos in range(0,25):
			if (Product.Name == self.list[Pos].Product):
				Product_Units+= self.list[Pos].Quantity
		return Product_Units    	   #This function returns the amount of a product on the vending machine. 

	def UpdateQueue(self, Row, Col, Product, Quantity):
		Pos= getListPos(Row,Col)            #This line converts X,Y to a position 'Pos' in [0,24] range.
		#Clear Queue
		for w in range (0, self.list[Pos].Quantity): 
			self.list[Pos].Remove_Product()
		#Add selectedProduct
		self.list[Pos].Add_Products(Product,Quantity)


	#def Product_Inventory(self):
	#Function to create an inventory of the available products
		

	
	#def Extract_Product(self, Product):
	#This function will extract a unit of the product from the queue with the lower amount.

	def ClearVM(self):
		Row= "ABCDE"
		Col= "12345"		
		for i in Row:
			for j in Col:
				Pos=getListPos(i,j)
				self.list[Pos].Product = Catalog.NoProduct
				self.list[Pos].Quantity = 0 
		
	








