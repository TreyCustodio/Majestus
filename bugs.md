#   List of Bugs to Fix and Tasks to Complete

##  Level Design
- start with an image file
- map each 16x16 grid element to an I-block of the same size


##  Text Display
### Box 2
- closing routine not working
- characters look a bit funny



## Maps
### Wavering Grotto -> Brown or Blue
### Chapel Hall -> Red
### Scorching Fields -> Orange


##  Pausing
- press start to pause
- open up the menu
- equip your attacks
- add a fade out into the pause screen

## Shop Scripting
*Can only hold 9 of any item*

### Grotto Entrance Shop
1. Beer $50
2. Potion $10
3. Key $99
4. Chance Emblem $100

### Grotto Exit Shop
1. Beer $50
2. Smoothie $30
3. Key $99
4. Wallet $99


##  Player Movement
- Regular run ability
    - just doubles your velocity
    - lets you change directions
- Ice skates
    - triples your velocity
    - freezes enemies on contact and **knocks you back**
    - cannot change directions while running

##  Drops
- animate the drop above the player's head
- probably need to create a new object in HudManager class
    - **replica** object

##  Replica Objects
- animated sprites that do not affect anything in the world
- they just animate and add visual effect to the game
- Replica = an Animated object
    - fileName,
    - nFrames,
    - row,
    - fps,






##  Enemies
- Keep arrows attached to enemy's body
### Flapper
- movement more akin to a LTTP bat

### Alpha Flapper
- movement


