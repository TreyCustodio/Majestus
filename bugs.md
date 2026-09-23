#   List of Bugs to Fix and Tasks to Complete


##  Player Movement
- Regular run ability
    - just doubles your velocity
    - lets you change directions
- Ice skates
    - triples your velocity
    - freezes enemies on contact and **knocks you back**
    - cannot change directions while running

##  Interacting with Npcs
- shouldn't be able to speak while holding interact
- once you enter the interaction zone, the engine should check for the next time you press down the interact button before displaying text



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








##  Enemies
- Keep arrows attached to enemy's body
### Flapper
- movement more akin to a LTTP bat

### Alpha Flapper
- movement








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

