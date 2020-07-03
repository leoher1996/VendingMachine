import Product as Product
#This file includes a set of available products. 

#Cold products:
Coke        = Product.NewProduct("Coke"         , 700 , 'C', "Pictures/Cold/CokeLogo.jpg")
FantaGrape  = Product.NewProduct("Fanta Grape"  , 650 , 'C', "Pictures/Cold/FantaGrape.jpg")
FantaOrange = Product.NewProduct("Fanta Orange" , 600 , 'C', "Pictures/Cold/FantaOrange.jpg")
FantaRed    = Product.NewProduct("Fanta Red"    , 650 , 'C', "Pictures/Cold/FantaRed.jpg")
Powerade    = Product.NewProduct("Powerade"     , 800 , 'C', "Pictures/Cold/Powerade.jpg")

#Room Temperature: 
Lays        = Product.NewProduct("Lays"         , 700 , 'R', "Pictures/Room/Lays.jpg")
Pringles    = Product.NewProduct("Pringles"     , 1200, 'R', "Pictures/Room/Pringles.jpg")
Ritz        = Product.NewProduct("Ritz"         , 450 , 'R', "Pictures/Room/Ritz.jpg")
Snickers    = Product.NewProduct("Snickers"     , 600 , 'R', "Pictures/Room/Snickers.jpg")
Tosh        = Product.NewProduct("Tosh"         , 400 , 'R', "Pictures/Room/Tosh.jpg")

#Empty Field:
NoProduct   = Product.NewProduct("None"         , 0   , 'C', "Pictures/empty.jpg")







