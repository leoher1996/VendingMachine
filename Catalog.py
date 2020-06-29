import Product as Product
#This file includes a set of available products. 

#Cold products:
Coke        = Product.NewProduct("Coke" , 700, 'C', "Pictures/CokeLogo.jpg")
FantaGrape  = Product.NewProduct("Fanta Grape", 650, 'C', "Pictures/FantaGrape.jpg")
FantaOrange = Product.NewProduct("Fanta Orange", 600, 'C', "Pictures/FantaOrange.jpg")
FantaRed    = Product.NewProduct("Fanta Red", 600, 'C', "Pictures/FantaRed.jpg")
Powerade    = Product.NewProduct("Powerade", 800, 'C', "Pictures/Powerade.jpg")

#Room Temperature: 
ChocolateBar = Product.NewProduct("Chocolate Bar" , 500, 'R', "Introduce Path")

#Empty Field:
NoProduct   = Product.NewProduct("None",  0, 'C', "Pictures/empty.jpg")







