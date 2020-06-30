import Catalog as Catalog
import VendingMachine as VM
import random
#This file creates an instance of the NewVendingMachine.
#Also fills the vending machine randomly.  

vm= VM.NewVendingMachine()
InitProducts= [Catalog.Coke, Catalog.FantaGrape, Catalog.FantaOrange, Catalog.FantaRed, Catalog.Powerade]
Rows= "ABCDE"
Col= "12345"
for i in Rows:
	for j in Col:
		ProductToAdd  = random.randint(0, 4)
		QuantityToAdd = random.randint(1, len(InitProducts))
		for x in range(0, QuantityToAdd):
			vm.Add_Product_To_Queue(InitProducts[ProductToAdd],str(i),int(j))



