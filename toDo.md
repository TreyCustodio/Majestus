This file contains information relevant to version history,
as well as ideas and everything on my to-do list.
~Trey Custodio~

v0.1
Scorching Fields first version. Lava Knight Boss.

v0.2
Tutorial:
- [ ] Tutorial Shop
  - [ ] Convo
  - [ ] Shopkeeper npc
- [ ] Key, set lock/key flags
  - [ ] One flag for the door,
  - [ ] One flag for the puzzle to get key
- [ ] Boss Light Cloaker
- [ ] Gremlin/Larger enemy hitboxes
- [ ] Keep updating no matter what during healthbar initialization.
- [ ] No pausing in between textboxes
- [ ] Shortcut screen
- [ ] Show next and previous shortcuts
- [ ] New textboxes + tutorial text signs

v0.25
Saving:
- [ ] Read in flags and load data from a text file
- [ ] Write flag, save room, inventory, equipped, and shortcut values to a file
- [ ] Nicodemus boss fight
- [ ] Nicodemus saving dialogue
- [ ] New game gives warning that progress will be lost
- [ ] Title Screen lets you choose New Game, Continue, or Firi Mode
  - [ ] Firi Mode lets you play as Firi starting from the beginning

v0.3
Intro

v0.4
Firi Segment + Stardust Quarry
- [ ] Firi Mode gives you a timed challenge to complete

v0.5
Scorching Fields, Some of Frigid Isles

v0.6
Thunder Tower

v0.7
Gale Grove

v0.8
Myer Segment
- [ ] Myer Mode lets you play as Myer in the same segment.
- [ ] Talk to your brother to restart the segment like New Game +
- [ ] Keeps track of a percentage
- [ ] In the future, I might make another campaign mode where you play as Myer. Replace his boss fights with new ones.

v0.9
Mid-game Climax + Frigid Isles

v0.10
Connecting Routes, Maintaining Flags

v0.11
Post Frigid Isles Segment

v0.12
Final level + final boss

v0.13-20
Extra Content, Monster Mobster, Stardust Quarry, Item Placement, Side quests, secret bosses, boss gauntlet



To Debug:
- [ ] Decrease keyCount in Flame_10
- [ ] No ice on enemies when respawning
- [ ] Arrow starting position (shooting with back to the wall causes arrow to instantly collide with wall)
- [ ] Health bar initialization fails if mouse off-screen event is handled as the game loads in
- [ ] Make hud transparent if you get to the left side of the screen. Set the alpha
- [ ] Rework bounce method. If inWall then don't moving in a direction that would put you further into the wall, then don't move. As opposed to setting velocity to opposite
- [ ] Stop updating during textbox if paused
- [ ] Heater replaying animation every time you freeze it


To add:
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




    

Equipment:

  Key Items
  1. Plant
  2. Chance Emblem
  3. Map
  4. Fake id
  5. Magic Conch
  6. Defense ring
  7. Alpha key
  8. ???

  Arrows (elemental arrows do +2 damage. All arrows are super effective to skeletal enemies):
  1. Ol' reliable
  2. Bombofaun
  3. Fire
  4. Ice
  5. Thunder
  6. Wind
  7. Laser/Plasma/Ring (Machine gun like cave story)
  8. Special arrow awarded from secret boss

  Elements
  1. Flame Sword
  2. Flare Step
  3. Blizzard
  4. Ice Cleats
  5. Thunder Clap
  6. Thunder Grapple
  7. Gale Slash
  8. Air Shield

  Items
  1. Syringe
  2. Cherry Potion
  3. Smoothie
  4. Beer
  5. Joint
  6. Speed
  7. ???
  8. ???




Ideas:
  Arrow Rotation Screen:
  - Hold Arrow button to open up an arrow selection screen. 
  - Hover over an arrow to select it. 
  - Release to exit the screen.

  Boss idea:
  - He spams shooting you. 
  - If you try to shoot him, he dodges to the right or left 
  - after 3 dodges, he runs at you, and you can hit him.
  
  Create seperate list for static obstacles/enemies.
  - That way you dont have to loop thru enemies
  to bounce an enemy off another enemy



Majestus sales pitches:
- No filler besides npcs with funny dialogue and world building
- Characters interacting with each other; Characters with personality.

