import Product as Product
import Catalog as Catalog

NoProduct  = Catalog.NoProduct

class NewQueue:	
	def __init__(self, Row, Column):
		self.Row = Row                     #Row on the vending machine. (Type Char, A->E from the left to the right)
		self.Column=Column                 #Column on the vending machine. (Type Int, 1->5 from the top to the bottom)
		self.Quantity = 0                  #Amount of products per Queue. (Type Int, Min 0, Max 5)
		self.Product = NoProduct           #Type of product on the queue. Only 1 is allowed per Queue. (Type Product) 
	
	def Add_Product(self, Product):
		if self.Product.Name != Product.Name:    
			#Case when the first product is added.
			if self.Quantity == 0:
				self.Product = Product
				self.Quantity+=1
			#Case when a product has already been added. 			
			else:  
				print("FAIL: Not possible to add a", Product.Name ,"because the queue has", self.Product.Name)
				 
		#If self.Product.Name == Product.Name		
		else:                 
			if self.Quantity<5:
				self.Quantity+=1
			else:
				print("FAIL: Not possible to add product because the queue is full") 				
		
		

	def Remove_Product(self):
		#Case when a queue has no product. 
		if self.Quantity==0:
			print("FAIL: Not possible to remove product because the queue is empty") 	
		else:
			self.Quantity-=1
			#Case when the last product is removed from a queue. 
			if self.Quantity==0:
				self.Product=NoProduct

	
	def Add_Products(self, Product, Quantity):
		if Quantity<0 or Quantity>5:
			print("FAIL: Wrong Input, Min:0 and Max: 5")
		else:
			tmp=Quantity+self.Quantity
			if tmp>5:
				print("User attempted to introduce",Quantity,"products, but only was space for",(5-self.Quantity))
				for x in range(0, 5-self.Quantity):
					self.Add_Product(Product)

			else:
				for x in range(0, tmp-self.Quantity):
					self.Add_Product(Product)

	def Remove_Products(self, Quantity):
		if Quantity<0 or Quantity>5:	
			print("FAIL: Wrong Input, Min:0 and Max: 5")
		else:		
			if Quantity > self.Quantity:
				print("User attempted to remove",Quantity,"products, but there was only ", self.Quantity)
				for x in range(0, self.Quantity):
					self.Remove_Product()
			else:	
				for x in range(0, Quantity):
					self.Remove_Product()

	def PrintQueueInfo(self):
		print("Row:", self.Row, "| Column:", self.Column, "| Quantity:", self.Quantity, "| Product:", self.Product.Name)                     



			 
						
			
			
				


		
