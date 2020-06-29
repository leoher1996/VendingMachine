import Catalog as Catalog
import VendingMachine as VM

vm= VM.NewVendingMachine()
InitProducts= [Catalog.Coke, Catalog.FantaGrape, Catalog.FantaOrange, Catalog.FantaRed, Catalog.Powerade]
Rows= "ABCDE"
Col= "12345"
for i in range(0,3):
	for i in Rows:
		for j in Col:
			vm.Add_Product_To_Queue(InitProducts[int(j)-1],str(i),int(j))




