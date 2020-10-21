# TODO

## Order!
* Generic for answers and questions (items)
* On ItemAdd: get highest postiion in item set (for q or a), new position = highest +1
* On ItemDelete: get items with position > deleted, foreach: position -1
* On ItemUp: get current position, change current position to 99, get item with position +1 and change to old current, change 99 to old +1
* On ItemDown: identical in reverse

## Users
* Get users 
* ForeignKey on Tool for owner
* Possibly manytomany for editors