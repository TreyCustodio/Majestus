from . import vec
import pygame
"""
Screen Constants
"""
RESOLUTION = vec(304,208)
SCALE = 3
UPSCALED = RESOLUTION * SCALE
EPSILON = 0.01




"""
Global boolean values that represent flags.
Used for a variety of special events.
"""
FLAGS = [False for i in range(150)]
#FLAGS[110] = True
#for i in range (1, 10):
    #FLAGS[i] = True

#FLAGS[62] = True
#1-20 -> Pop-up messages and area names
#1 -> Grand Chapel
#2 ->
#3
#4
#5
#6
#7
#8
#9
#10
#17 -> Flame shard first pickup
#18 -> Ice shard first pickup
#19 -> Bolt shard first pickup
#20 - > Gale shard first pickup

##50-59 -> Respawn/Checkpoints
#50 -> skip intro (post-death)
#51 -> respawn in Grand Chapel
#52 -> Flame_4

##60 - > flame fields flags


##88-93 -> Blessings
#88 -> Blessings are locked, way is clear
#89 -> No blessings appear
#90 -> Ice chosen
#91 -> Fire chosen
#92 -> Thunder chosen
#93 -> Wind chosen


##94-100 Completion flags
#94 -> Ice complete
#95 -> Fire complete
#96 -> Thunder complete
#97 -> Wind complete

##110-150 -> Boss Flags
#110 -> ALPHA FLAPPER DEFEATED
#111 -> LavaKnight




"""
16x16 coordinates of the screen
"""
COORD = [[(i*16, j*16) for j in range(13)] for i in range(18)]







"""
Indicates what C attack and what type of arrow is equipped
"""
EQUIPPED = {

    "C": -1,
    #0 -> fire sword, 1 -> blizzard, 2 -> clap, 3 -> slash
    "Arrow": 0,
    #0 -> regular, 1 -> bombo, 
    "room":0,
    #0 -> regular, 1 -> fire, 2 -> ice, 3- -> thunder, 4-> wind, 5-> super, 6-> hyper
    "area":0,
}

bombos = 50
"""
The Player's inventory
"""
INV = {

    ##Health, elements, arrows, currency
    "max_hp": 1,
    "shoot": True,
    "hasBombo": True,
    "fire": True,
    "clap": True,
    "slash": True,
    "cleats": True,
    "maxBombo": bombos,
    "bombo": bombos,
    "flameShard": 0,
    "frostShard": 0,
    "boltShard": 0,
    "galeShard": 0,
    
    ##Maps
    "map0":True,
    "map1":False,
    "map2":False,
    "map3":False,
    "map4":False,

    ##Consumables and key items
    "plant": 0,
    "chanceEmblem": True,
    "lavaBoots": True,
    "syringe":True,
    "potion": 5,
    "smoothie": 5,
    "beer": 0,
    "joint":0,
    "speed":0,
    "wallet": 99,
    "money": 0,
    "keys": 1,

    ##Upgrades
    "flameCost": 20,
    "frostCost": 20,
    "boltCost": 20,
    "galeCost": 20,

}


"""
Text for the intro cutscene

&& -> clear textbox before printing another line
"""
INTRO = {


0:"Before everything began,\n\
there was nothing.\n\
The elements existed in\n\
the abyss of chaos.\n\
At the moment when nothing\n\
transformed into everything,\n\
the elements split into\n\
two seperate factions:\n\
One to lay the foundation\n\
of the world itself,\n\
and another to breathe life\n\
into the infant world.\n",

1:"In order to build the world,&&\n\
The elements took on\n\
the forms of deities:\n\
Firion, of the Flame,&&\n\
Estelle, of the Frost,&&\n\
Vectros, of the Bolt,&&\n\
Gladius, of the Gale.&&\n\
Together, the four deities\n\
gave birth to nature.\n",

      
2:"As for the other elements,\n\
they birthed perspective.\n\
They fashioned energy out\n\
of Light and Darkness,\n\
illuminating and shrouding\n\
the world as they saw fit.\n\
To populate the world,&&\n\
these elements took the\n\
forms of humans and beasts.\n\
Elemental gifts flowed\n\
within all creatures.\n",

4:"As if by a divine prank,&&\n\
one tribe of humans did\n\
not receive any blessings.\n\
These people were called\n\
the Naturalites.\n\
When Light and Darkness\n\
forsook the Naturalites,\n\
they prayed...          &&\n\
    to the flames\n\
they could not quench;\n\
    to the frost\n\
they could not melt,\n\
    to the thunder\n\
they could not hush,\n\
    to the winds\n\
they could not quell.\n\
The four Gods of nature\n\
heeded their cries for help,\n\
showering them in divine\n\
gifts of power.\n",

6:"Eternally grateful for\n\
their prosperous gifts,\n\
the Naturalites constructed\n\
a city of worship.\n\
They named it [Majestus]...&&\n",

8:"...But that city\n\
now lies in ruin.\n\
And the few Naturalites\n\
alive know naught but tales.\n",

9:
"Majestus attracts the\n\
most wreckless folk today.\n\
We each seek knowledge and\n\
treasure without emotion.\n",

10:
"If you ask me...&&\n\
The secrets of our world\n\
remain just out of reach,\n\
sealed behind the lies\n\
of our ancestors.\n",


}




"""
Item info for the pause screen
"""
INFO = {


"plant":
"A vibrantly green vegetable.\n\
Geemers seem to love it.",

"shoot":
"[Old Reliable]\n\
Deal 2 damage.\n\
Press X to shoot.",

"bombo":
"[Bombofauns]\n\
Deal 5 damage.\n\
Shoot explosive plants.",

"fire":
"The blessing of fire.\n\
Equip with C.",

"cleats":
"The blessing of ice.\n\
Equip with C.",

"clap":
"The blessing of thunder.\n\
Equip with C.",

"slash":
"The blessing of wind.\n\
Equip with C.",

"chance":
"[Chance Emblem]\n\
Survive a fatal attack,\n\
if you have more than 1 HP."
}




"""
Icons from icon.png to be used in text display
"""
ICON = {
    "blank": (0,0),
    "plant":(1,0),
    "bombo":(4,0),
    "geemer0":(2,0),
    "geemer1":(3,0),
    "stomper":(5,0),
    "knight":(6,0)
}






"""
All of the text for npcs!
Follows format:

roomName_class#
"""
SPEECH = {
"alpha_flapper":
"Skreeeeeeeeee!!&&\n\
There is no treasure!&&\n\
The Gods won't choose you!\n\
This path leads to death!\n",

"lava_knight":
"O, brave human...&&\n\
.....................&&\n\
Much of my men have you\n\
chillingly slain...\n\
Thoughtlessly bleak, my view\n\
lacks knowledge to feign...\n\
This heart reacts so blue\n\
to frivolous pain...\n\
The tears pour for a few...\n\
The rage boils their rain...\n\
Take hold of my clue,\n\
you pitiful stain!\n\
This hatred you grew,\n\
shall force you to wane!\n",

"lava_knight2":
"Watch, heavenly brothers!\n\
I speak without shame!\n\
The bane of our home shall\n\
be scorched by our flame!\n",

"lava_knight3":
"In glittering glaciers,\n\
furious bells ring no more.\n\
In blazes and ashes,\n\
I've no story to tell.\n\
In wielding your blessings,\n\
pray, honor them well.\n\
",

"flame_7_bopper1":
"Y'ever just wanna blow\n\
everything up?\n\
And be like, \"the power\n\
of plant compells you!\"\n\
And then just blow up\n\
everything around you?\n",

"flame_7_bopper2":
"Y'look like a simp!&&\n\
Y'wouldn't catch me chasing\n\
a chick in these fields!\n\
I'm just sayin!&&\n\
I'm playin!&&\n",

"flameShard":"Picked up a [Flame Shard]!&&\n\
Use them in the Grand Chapel\n\
to upgrade your flame sword!\n\
Check how many you have\n\
on the pause menu.\n",

"frostShard":"Picked up a [Frost Shard]!&&\n\
Use them in the Grand Chapel\n\
to upgrade your blizzard!\n\
Check how many you have\n\
on the pause menu.\n",

"boltShard":"Picked up a [Bolt Shard]!&&\n\
Use them in the Grand Chapel\n\
to upgrade your thunderclap!\n\
Check how many you have\n\
on the pause menu.\n",

"galeShard":"Picked up a [Gale Shard]!&&\n\
Use them in the Grand Chapel\n\
to upgrade your gale slash!\n\
Check how many you have\n\
on the pause menu.\n",

"first_bombo":
"You discovered [Bombofauns]!&&\n\
Fire these explosive plants\n\
to destroy rocks and enemies.\n\
On the pause menu, equip\n\
them in the [ARR] row.\n\
See what I did there? ;)&&\n\
Keep a watchful eye on\n\
your ammo count!\n",

    "key":
"   Picked up a key.&&",
    "switch_unlocked" : "A switch was unlocked.",
    "door_unlocked" : "A door was unlocked.",
    "room_clear":
"   Room cleared!",
"intro_geemer":"You thought I was a monster,\n\
didn't you?\n\
Don't worry, man,\n\
I get that a lot.\n\
What's a dude like you\n\
doing in here anyway?\n\
Heh heh heh heh.&&\n\
You humans always gotta\n\
satisfy those desires...\n",

"intro_geemer1":
"I'm a Geemer, man.\n\
I know all kindsa stuff.\n\
My bros are around too.&&\n",

"intro_geemer2":
"My name? Oh, dude...&&\n\
Geemers don't have names,\n\
brooooo...&&\n",

"intro_geemer3":
"Dude I'm so hungry!\n\
Ya got anything to eat,\n\
mannnnnnnnnn????????????&&\n",

    "intro_sign": "/ Temple of the Naturalites\n\
   These sacred halls host\n\
 unwavering souls, who were\n\
corrupted by power and greed.\n\
  The relics sealed within\n\
    contain the blessings\n\
of the four divine guardians.\n\
      Seek their gifts...",
    
    "intro_plantgeemer":
"Mannnnn, I need energy...&&\n\
Green energy...&&\n\
.............................&&\n\
Know what I mean, dude?&&\n",

"intro_plantgeemer2":
"Is that what I think it is?&&\n\
Oh, dude, you're the best!&&\n",


"intro_plantgeemer3":
"Laaaaaaaaaterrrrr...&&",


"intro_chest":
"Picked up a strange plant.&&\n\
Someone around here\n\
might want it.\n",

"intro_entrance":
"   Divine forces prevent\n\
    you from leaving.\n",

    "intro_switches":
"Whattup, my guy?&&\n\
If ya had a block to push,\n\
I bet you could keep that\n\
red switch pressed down, man.&&\n\
Yeah, the one by my bro.&&\n\
He must be too light to\n\
weigh it down...\n\
Ha ha ha ha.&&\n",

"intro_switches2":
"Man, I've been pondering...&&\n\
The colors on these switches\n\
define their properties...\n\
Brown switches are normal,\n\
Blue ones are heavy,\n\
Reds pop back up,\n\
Green means they're timed.\n",

"intro_pushableblocks":
"Do you know about those\n\
pushable blocks?\n\
Dude.&&\n\
They were actually created\n\
by the goddess's frost.\n\
When they touch anything\n\
they don't wanna touch,\n\
They disappear!&&\n",


"intro_roomclear":
"Looks like orange switches\n\
unlock when there's no more\n\
monsters around. Nice.&&\n",

"intro_combat":
"Have you tried fighting\n\
while on the verge of death?\n\
They say that fortune\n\
favors the brave!\n",

"david":
"There seems to be some\n\
kind of note inside.\n\
\"W h e r e \' s  m y\n\
b i r t h d a y  g i f t ?\"\n\
.....................&&\n\
What?&&\n",


"menu_reminder":
"I'm sure you're quite\n\
versatile with those weapons,\n\
aren't you, baby?&&\n",

"thunder_1":
"Can ya feel the rhythm,\n\
lil guy? Check it!\n\
My name is big G,\n\
Ya can\'t move like me,\n\
can\'t sing like me,\n\
can\'t sting like me,\n\
can\'t swing like me,\n\
don\'t got bling like me...\n\
What? You said Geemers\n\
don\'t have names?\n\
Way to kill the vibe!&&\n",


"thunder_2":
"Soooooooooooo\n\
hungryyyyyyyyyyy...\n\
Foooooooooooood\n\
stolennnnnnnnnn\n\
byyyyyyyyyyyyy\n\
monstersssssssss.\n",

"thunder_fead":
"Yummmmmmmmmmmmm&&\n\
Thankssssssssssss\n\
myyyyyyy guyyyyyy!\n",


"thunder_sign":
"Ya know, game design is\n\
a lot harder than I thought,\n\
but what else would I do?\n\
Write a book?\n\
And who said anything\n\
about a fourth wall?\n",

"plant":
"Picked up another plant.\n\
Feed it to a hungry Geemer.\n",

"fire":
"Y/NFirion's fire burns\n\
furiously.\n",

"ice":
"Estelle's ice quenches\n\
your sorrows.\n",

"thunder":
"Kuwabara's thunder shocks\n\
your soul.\n",

"wind":
"The winds of Gladius flow\n\
eternally.\n",

"gale_sign":
"The creator of this game\n\
did not finish this room,\n\
but enjoy fighting a bunch\n\
of Davids instead.\n",

"chapel_geemer":
"Head west and then south\n\
to get to Scorching Fields.\n",

"skipping_text":
"Dude... You can skip\n\
text by pressing SPACE.\n\
It's pretty useful in a\n\
variety of situations.\n\
Like the one you're\n\
in right now.\n\
You see, you think\n\
I'll stop talking\n\
if you listen to me\n\
for long enough,\n\
but I'll never stop\n\
talking, and you'll\n\
never be able to escape\n\
my undying wrath,\n\
as I impose my will\n\
upon your brittle soul,\n\
thrusting your hopes and\n\
dreams into endless oblivion,\n\
never able to return to\n\
your feeble endeavors,\n\
sinking hoplelessly into\n\
a flood of sorrow.\n",


"town_1":
"Welcome to Geemer town,\n\
young traveller.\n",

"shop":
"We've got it all!&&",

"shopkeep":
"If ya see anything you want,\n\
i'll sell it to ya.\n",

"flame_entrance_geemer":
"Ya don't see too many\n\
Geemers around these parts.\n\
Not anymore that is.&&\n\
Everyone used to live in\n\
harmony and farm together...\n\
But those Stompers...&&\n\
They smash the land,\n\
they burn it all up,\n\
and they slaughter at will!&&\n\
What a shame...&&\n",

"flame_entrance_geemer2":
"You're a human!&&\n\
You guys don't eat your\n\
cheeba like we do, right?\n\
Humans have to smoke it!\n\
Ha ha ha ha ha!&&\n",

"flame_dispo":
"If you're lookin to buy,\n\
sorry man but I'm all out.\n\
Haven't been able to grow\n\
in so long, dude...\n\
But if you've got any\n\
green on you...\n\
I can roll you up something\n\
really nice, man!\n",

"flame_roll":
"Y/NLooks like you've got\n\
summa that good good!\n\
Want me to roll for ya?\n",

"bombo_expansion":
"Picked up some fertilizer\n\
for those pockets of yours!\n\
Maximum [Bombofaun] carrying\n\
capcity increased by 5!\n",

"boppers":
"Newly discovered invasive\n\
floral species: the Bopper.\n\
These dancing plants always\n\
regrow after being cut down.\n\
Additionally, they produce\n\
Bombofauns in great quantity.\n\
   [Scorching Fields\n\
     Restoration committee]\n",

"post_stomper":
"My brother's remains are\n\
splattered on the grass...\n\
Please help us slay\n\
the rest of those knights!\n",

"null":
"Nothing to see here."


}