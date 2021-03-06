#This file implements a class NewVendingMachine.
import Queue as Queue
import Product as Product
import Catalog as Catalog

############################
#Function getListPos is a useful function to get a position [0,24] from the row and column on a vending machine. 
#Arg: Row corresponds to the row in a vending machine, refered as {A,B,C,D,E}
#     Col corresponds to the column in a vending machine, refered as {1,2,3,4,5}
############################
def getListPos(Row, Col):
	Pos= (int(Col)-1)
	Pos+= (5*(ord(Row)-65))   #ord() returns unicode characted represented by an integer. ('A' -> 65)
	return Pos

############################
#Function get_X and get_Y are a useful functions to convert row and column on a vending machine to a position X and Y on a [1,5] range. 
#Arg: Row corresponds to the row in a vending machine, refered as {A,B,C,D,E}
#     Col corresponds to the column in a vending machine, refered as {1,2,3,4,5}
############################
def get_X(Queue):
	X_pos=int(ord(Queue.Row)-65)
	return X_pos	

def get_Y(Queue):
	Y_pos=int(Queue.Column)
	return Y_pos



class NewVendingMachine:
	def __init__(self):
		self.list = []    #list[] allows to store the 25 queues that conforms the vending machine. a
		self.Temp= None
		Rows= "ABCDE"
		Col= "12345"		
		for i in Rows:
			for j in Col:
				self.list.append(Queue.NewQueue(i,j))
		
	############################
	#Method Print_Queue_Info displays some relevant info about the NewQueue objects, included in list[].
	############################
	def Print_Queues_Info(self):
		for x in range(0,25):		
			self.list[x].PrintQueueInfo();
			print("\n")
	

	############################
	#Method Add_Product_To_Queue sets the corresponding parameters to simulate the inclusion of a product to a queue
	#given by a column and a row.
 	#Arg: Row corresponds to the row in a vending machine, refered as {A,B,C,D,E}
	#     Col corresponds to the column in a vending machine, refered as {1,2,3,4,5}
	############################
	def Add_Product_To_Queue(self,Product,Row,Col):
		Pos= getListPos(Row,Col)            
		self.list[Pos].Add_Product(Product)  #This line adds a product object to the queue object into list[Pos].
		#TODO: Add some flags to check if there is any issue adding the product to the queue.	



	############################
	#Method Remove_Product_From_Queue sets the corresponding parameters to simulate the remotion of a product from a queue
	#given by a column and a row.
 	#Arg: Row corresponds to the row in a vending machine, refered as {A,B,C,D,E}
	#     Col corresponds to the column in a vending machine, refered as {1,2,3,4,5}
	############################
	def Remove_Product_From_Queue(self, Row, Col):
		Pos= getListPos(Row,Col)            
		self.list[Pos].Remove_Product()     #This line removes a product object from the queue object in list[Pos]. 
		#TODO: Add some flags to check if there is any issue removing the product to the queue.



	############################
	#Method Check_Availability  returns the amount of products of type Product present on the vending machine.
	#Args: Product selects the product that the function will search for.
	############################
	def Check_Availability(self, Product):
		Product_Units = 0
		for Pos in range(0,25):
			if (Product.Name == self.list[Pos].Product):
				Product_Units+= self.list[Pos].Quantity
		return Product_Units    	   #Returns the amount of a products found. 


	############################
	#Method UpdateQueue sets the corresponding parameters to simulate the remotion of the current products on the queue
	#and includes 'Quantity' objects of type Product. 
	#given by a column and a row.
 	#Arg: Row corresponds to the row in a vending machine, refered as {A,B,C,D,E}.
	#     Col corresponds to the column in a vending machine, refered as {1,2,3,4,5}.
	#     Product selects the product that the function will include.
	#     Quantity selects the amount of Product objets to be included. 
	############################
	def UpdateQueue(self, Row, Col, Product, Quantity):
		Pos= getListPos(Row,Col)           
		#Clear Queue:
		for w in range (0, self.list[Pos].Quantity): 
			self.list[Pos].Remove_Product()
		#Add selectedProduct:
		self.list[Pos].Add_Products(Product,Quantity)


	############################
	#Method ClearVM sets all the corresponding parameters simulating to clear all the queues on the vending machine  
	############################
	def ClearVM(self):
		Row= "ABCDE"
		Col= "12345"		
		for i in Row:
			for j in Col:
				Pos=getListPos(i,j)
				self.list[Pos].Product = Catalog.NoProduct
				self.list[Pos].Quantity = 0 

	

	############################
	#Method Extract_Products will extract a unit of the product from the queue with the lower amount.	
	#This function should be called after making sure the product is available.
	#Args: The Product object we are looking for.
	############################	
	def Extract_Product(self, Product):
		MinQuantity=5
		for x in self.list: 
			if (x.Product == Product):
				if x.Quantity<=MinQuantity :
					#Updates the information for the Queue with the lower amount of product.
					MinQuantity=x.Quantity
					Column= x.Column
					Row= x.Row
		#Remove one product from the queue with the lower amount. 
		Pos= getListPos(Row, Column)
		self.list[Pos].Remove_Products(1)
	
	############################
	#Method Extrac_A_Quantity_Of_Products will extract a quantity of a product from the queues with the lower amount.	
	#This function calls Extract_Product Quantity times. 
	#Args: The Product object we are looking for.
	############################	
	def Extrac_A_Quantity_Of_Products(self, Product, Quantity):
		for i in range(0,Quantity):
			self.Extract_Product(Product)
		





