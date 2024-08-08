v0.2
Tutorial:
- [ ] Shop + new shop controlls
- [ ] Key, set lock/key flags
- [ ] Boss room
- [ ] Text in larger rooms
- [ ] Gremlin hitboxes
- [ ] Keep updating no matter what during healthbar initialization.
- [ ] No pausing in between textboxes
- [ ] Pause screen: [-] Fullscreen, [ZR] Shortcuts -> replace top of menu with six boxes. Press A to select a box, then A on the attack/item. ZR to close.


Debug:
- [ ] Bombofaun ammo count on pause screen in rooms with camera
- [ ] enemy damage nums in camera
- [ ] Decrease keyCount in Flame_10
- [ ] No ice on enemies when respawning
- [ ] self.npcs gets set to [] during resets
- [ ] Arrow starting position (shooting with back to the wall causes arrow to instantly collide with wall)
- [ ] Health bar initialization fails if mouse off-screen event is handled as the game loads in
- [ ] Make hud transparent if you get to the left side of the screen. Set the alpha
- [ ] Rework bounce method. If inWall then don't moving in a direction that would put you further into the wall, then don't move. As opposed to setting velocity to opposite
- [ ] Stop updating during textbox if paused


Fixes:
- [ ] Fireball movement
- [ ] Make stompers bounce off each other
- [ ] placeEnemies doesn't reset position on enemyplacement 0
- [ ] Heater replaying animation every time you freeze it
- [ ] Healthbar heal
- [ ] Certain enemies get stuck in walls when damaged (rework bounce())
- [ ] NOTE THAT THE HEALTHBAR WILL GLITCH OUT AND INFINITELY DRAWHURT IF YOU CALL HEALTHBAR.DRAWHURT(0), ALTHOUGH I WILL LEAVE IT IN TO HELP DETECT ERRORS. HEALTHBAR.DRAWHURT(0) SHOULD NEVER BE CALLED.


Additions:
- [ ] Flame backstep
- [ ] Thunder hook
- [ ] Wind shield
- [ ] Boss healthbar Name
- [ ] maps
- [ ] indicators
- [ ] Make an image appear over the player's head when they swap arrows with ZR
- [ ] Also press ZR on the pause screen to edit your arrow rotation. 
- [ ] Alternate Alpha Flappers and Flappers
  - [ ] elemental Alpha Flappers
  - [ ] Shoot projectiles
  - [ ] accelerates and decelerates
  - [ ] zelda 1 type bats

  Shop Revamp:
  Move cursor on each item and give a description at the bottom
  
  Arrow Rotation Screen:
  Press a button for help:
    You can select however many arrows you want. Ideally you rotate between the 3 strongest ones available to you or the 3 best for the current enemy.

  Arrows (elemental arrows do +2 damage, are super effective to skeletal enemies, and yield their elemental effect):
  1. Ol' reliable
  2. Bombofaun
  3. Fire
  4. Ice
  5. Thunder
  6. Wind
  7. Laser/Plasma/Ring (Machine gun like cave story)
  8. Special arrow awarded from secret boss


Majestus sales pitches:
- No filler besides npcs with funny dialogue and world building
- Characters interacting with each other; Characters with personality.