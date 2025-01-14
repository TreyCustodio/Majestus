# Majestus To-Do List
This file contains information relevant to version history,
as well as ideas and everything on my to-do list.
~Trey Custodio~


## v0.1
Scorching Fields first version. Lava Knight Boss.

## v0.2 - Tutorial
### Primary Objectives
- [ ] Connect the tutorial area to the chapel
- [ ] Textbox + font design
- [ ] Icon manager for buttons
- [ ] Shop / Dark Cloaker
- [ ] Light Cloaker
  - [ ] I Wonder boss theme
  - [ ] Introduce health concept
- [ ] Shortcuts
  - [ ] Next/Prev shortcuts
  - [ ] Icons
- [ ] Replace Quit with an Options menu
  - [ ] Text Speed
  - [ ] Child Mode
  - [ ] Controls
  - [ ] Quit
- [ ] Slowdown in Camera room
- [ ] Animated Title Screen Buttons


### Reminders and fixes:
- [ ] set lock/key flags
- [ ] Gremlin/Larger enemy hitboxes
- [ ] Keep updating no matter what during healthbar initialization.
- [ ] No pausing (event handling) in between textboxes
- [ ] Boners need to throw bone to the side they get hit
- [ ] Fix slowdown in (Tut_2 and Tut_3)
  - Reset the singleton rooms. Completely reinstantiate the room upon reintry. 
- [ ] Fix fadeout and screen wipe
- [ ] Outline white characters
- [ ] Redrawing Grotto
  - [ ] Finish Tut_2
    - [ ] Place each tile used on a tilemap (delete old tilemap)
    - [ ] Recdraw Tut_3 and Tut_1 using the new tiles only

## v0.25 - Saving
### Primary Objectives
- [ ] Read in flags and load data from a text file
- [ ] Write flag, save room, inventory, equipped, and shortcut values to a file
- [ ] Nicodemus boss fight
- [ ] Nicodemus saving dialogue
- [ ] New game gives warning that progress will be lost
- [ ] Censoring. Child mode censoring. Use symbol to replace words in drawchars.
      Fuck -> Duck, Bitch -> Witch, Shit -> Dump, 
      Also change entire dialogue if in child mode. When Myer graphically describes how
      his brothers were killed, make it less graphic.
      Also change bloody/death sprites.
      
- [ ] Title Screen lets you choose New Game, Continue, or Firi Mode
  - [ ] Firi Mode lets you play as Firi starting from the beginning

## v0.3 - Intro Cutscene (lots of art and spritework)

## v0.4 Firi Segment in Stardust Quarry + Firi Mode on title screen
### Primary Objectives
- [ ] Firi Mode gives you a timed challenge to complete

## v0.5 Scorching Fields, Some of Frigid Isles

## v0.6 Thunder Tower

## v0.7 Gale Grove

## v0.8 Myer Segment
### Primary Objectives
- [ ] Myer Mode lets you play as Myer in the same segment.
- [ ] Talk to your brother to restart the segment like New Game +
- [ ] Keeps track of a percentage
- [ ] In the future, I might make another campaign mode where you play as Myer. Replace his boss fights with new ones.

## v0.9 - Mid-game Climax + Frigid Isles

## v0.10 - Connecting Routes, Maintaining Flags

## v0.11 - Post Frigid Isles Segment

## v0.12 - Final level + final boss

## v0.13-20 - Extra Content, Monster Mobster, Stardust Quarry, Item Placement, Side quests, secret bosses, boss gauntlet


## Universal To-do List
### To Debug:
- [ ] Decrease keyCount in Flame_10
- [ ] No ice on enemies when respawning
- [ ] Arrow starting position (shooting with back to the wall causes arrow to instantly collide with wall)
- [ ] Health bar initialization fails if mouse off-screen event is handled as the game loads in
- [ ] Make hud transparent if you get to the left side of the screen. Set the alpha
- [ ] Rework bounce method. If inWall then don't moving in a direction that would put you further into the wall, then don't move. As opposed to setting velocity to opposite
- [ ] Stop updating during textbox if paused
- [ ] Heater replaying animation every time you freeze it


### To add:
- [ ] Monster Mobster
- [ ] Boss Gauntlet in stardust quarry. You can choose between Kylo, Firi (after his segment), or Myer (after his segment)
- [ ] Fireball movement
- [ ] Make stompers bounce off each other
- [ ] Healthbar heal
- [ ] Alternate weapons
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
  - [ ] A shield that increases the number of iframes -> Wouild have to allow you to attack during i frames
  - [ ] Something with the commandments
- [ ] Move 


## Miscellaneous Data and Definitions
### On New Game
- Child Mode On/Off
- Controler Options
- Toggle Fullscreen

### Settings Menu
- Controls
  - Controller name and image in top-left
  - Display controls for each action
    - Interact
    - Arrow
    - Element Attack
    - Element Movement
    - Shortcut
    - Previous Shortcut
    - Next Shortcut
- Text Speed Slow, Med, Fast
- Child Mode Off/On
- Fullscreen Off/On
[space]
- Quit to Title


### Input Options
1. Nintendo Switch Pro
2. Dualshock 5
3. Xbox One / Series X
4. Keyboard + Mouse
   1. Right/Left hand mode
      1. Move Kylo with WASD or Arrow keys
   2. Move target with mouse
   3. Kylo snaps to the closest direction that corresponds to the mouse position.
      1. if the mouse is best described as to his left, then he'll face left.
      2. Once it gets above/below a certain y/x coordinate (based on his sprite size), he'll snap to the corresponding direction
5. Keyboard no mouse
   1. WASD
      1. Shortcut shifting -> LSHIFT / RSHIFT
      2. Shortcut -> ENTER
      3. Arrow -> ;
      4. Element -> '
      5. Interact -> SPACE
      6. Pause -> ESC
   2. Arrow Keys
      1. Shortcut shifting -> A / S
      1. Shortcut -> SPACE
      2. Arrow -> X
      3. Element -> C
      4. Interact -> Z
      5. Pause -> ENTER

### Equipment

  #### Key Items
  1. Plant
  2. Chance Emblem
  3. Map
  4. Fake id
  5. Magic Conch
  6. Defense ring
  7. Alpha key
  8. ???

  #### Arrows (elemental arrows do +2 damage. All arrows are super effective to skeletal enemies):
  1. Ol' reliable
  2. Bombofaun
  3. Fire
  4. Ice
  5. Thunder
  6. Wind
  7. Laser/Plasma/Ring (Machine gun like cave story)
  8. Special arrow awarded from secret boss

  #### Elements
  1. Flame Sword
  2. Flare Step
  3. Blizzard
  4. Ice Cleats
  5. Thunder Clap
  6. Thunder Grapple
  7. Gale Slash
  8. Air Shield

  #### Items
  1. Syringe
  2. Cherry Potion
  3. Smoothie
  4. Beer
  5. Joint
  6. Speed
  7. ???
  8. ???




## Ideas
  ### Arrow Rotation Screen:
  - Hold Arrow button to open up an arrow selection screen. 
  - Hover over an arrow to select it. 
  - Release to exit the screen.

  ### Boss idea:
  - He spams shooting you. 
  - If you try to shoot him, he dodges to the right or left 
  - after 3 dodges, he runs at you, and you can hit him.
  
  ### Create seperate list for static obstacles/enemies.
  - That way you dont have to loop thru enemies
  to bounce an enemy off another enemy



## Majestus sales pitches:
- No filler besides npcs with funny dialogue and world building
- Characters interacting with each other; Characters with personality.

