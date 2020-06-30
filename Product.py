#This file implements a class NewProduct.
class NewProduct:
	def __init__(self, Name, Cost, Temperature, LogoPath):
		self.Name = Name                   #Product's name. (Type String)
		self.Cost = Cost	           #Product's cost. (Type Integer)
		self.Temperature=Temperature       #Two valid inputs: 'R' for room and 'C' for cold.  (Type Char) 
		self.LogoPath = LogoPath           #Path to find an associated picture for the product.  (Type String) 
	
