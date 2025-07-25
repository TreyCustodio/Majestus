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
FLAGS = [False for i in range(300)]

### Boss FLAG Control   ###

#FLAGS[10] = True
#FLAGS[100] = True #Light Cloaker
#FLAGS[200] = True #Light Cloaker Heart

#FLAGS[110] = True #Alpha Flapper
#FLAGS[210] = True #Alpha Flapper Heart

### Flag Descriptions   ###

##  0-79 -> Keys and door locks ##
#0 -> N/A
#1 -> fire shard
#2 -> ice shard
#3 -> lava shard
#4 -> gale shard
#5 -> first heart
#6 -> 
#7 -> 
#8 -> 
#9 -> 

#   Wavering Grotto
#10 -> Shop first convo
#11 -> Key in room 4
#12 -> Lock in room 3
#13 ->
#14 ->
#15 ->
#16 ->
#17 ->
#18 ->
#19 ->

#   Chapel Hall
#20 ->
#21 ->
#22 ->
#23 ->
#24 ->
#25 ->
#26 ->
#27 ->
#28 ->
#29 ->

#   Stardust Quarry
#30 ->
#31 ->
#32 ->
#33 ->
#34 ->
#35 ->
#36 ->
#37 ->
#38 ->
#39 ->

#   Scorching Fields
#40 ->
#41 -> Stomper mini boss cutscene watched
#42 -> Stomper mini boss dead
#43 ->
#44 ->
#45 ->
#46 ->
#47 ->
#48 ->
#49 ->

#   Rumbling Tower
#50 ->
#51 ->
#52 -> 
#53 -> 
#54 ->
#55 ->
#56 ->
#57 ->
#58 ->
#59 ->

#   Tempest Grove
#60 ->
#61 ->
#62 -> 
#63 -> 
#64 ->
#65 ->
#66 ->
#67 ->
#68 ->
#69 ->

#   Frigid Isles
#70 ->
#71 ->
#72 -> 
#73 -> 
#74 ->
#75 ->
#76 ->
#77 ->
#78 ->
#79 ->


##  80-99 Major Event Completion flags (sample) ##

#80 -> Wavering Grotto Complete

#81 -> Chapel Hall Complete

#82 -> Firi Section Complete #1

#83 -> Firi Section Complete #2

#84 -> Scorching Fields Complete

#85 -> Rumbling Tower Complete

#86 -> Tempest Grove Complete

#87 -> Frigid Isles Mid-game Climax complete

#88 -> 2nd Half Flag #1

#89 -> Melody Killed

#90 -> Entrance to Chamber Opened

#91 -> Ready to fight Myer

#92 -> Myer dead / Firi final fight

#93 -> End-game flag

#94 -> Extra #1

#95 -> Extra #2

#96 -> Extra #3

#97 -> Extra #4

#98 -> Extra #5

#99 -> MONSTER MOBSTER AVAILABLE


##  100-149 -> Boss Flags   ##
#100 -> Light Cloaker
#110 -> Alpha Flapper
#111 -> LavaKnight

##  200-249 -> Boss respective hearts   ##
#200 -> Light Cloaker
#210 -> Alpha Flapper
#211 -> LavaKnight


##  150-199 -> Expansions Group 1   ##
#150 -> 
#151 -> 
#152 -> 
#153 -> 
#154 -> 
#155 -> 
#156 -> 
#157 -> 
#158 -> 
#159 -> 

#160 -> 
#161 -> 
#162 -> 
#163 -> 
#164 -> 
#165 -> 
#166 -> 
#167 -> 
#168 -> 
#169 -> 

#170 ->
#171 -> 
#172 -> 
#173 -> 
#174 -> 
#175 -> 
#176 -> 
#177 -> 
#178 -> 
#179 -> 

#180 ->
#181 -> 
#182 -> 
#183 -> 
#184 -> 
#185 -> 
#186 -> 
#187 -> 
#188 -> 
#189 -> 

#190 ->
#191 -> 
#192 -> 
#193 -> 
#194 -> 
#195 -> 
#196 -> 
#197 -> 
#198 -> 
#199 -> 


##  250-299 -> Bombo Faun Expansions    ##

#250 -> 
#251 -> 
#252 -> 
#253 -> 
#254 -> 
#255 -> 
#256 -> 
#257 -> 
#258 -> 
#259 -> 

#260 -> 
#261 -> 
#262 -> 
#263 -> 
#264 -> 
#265 -> 
#266 -> 
#267 -> 
#268 -> 
#269 -> 

#270 ->
#271 -> 
#272 -> 
#273 -> 
#274 -> 
#275 -> 
#276 -> 
#277 -> 
#278 -> 
#279 -> 

#280 ->
#281 -> 
#282 -> 
#283 -> 
#284 -> 
#285 -> 
#286 -> 
#287 -> 
#288 -> 
#289 -> 

#290 ->
#291 -> 
#292 -> 
#293 -> 
#294 -> 
#295 -> 
#296 -> 
#297 -> 
#298 -> 
#299 -> 



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

    "Dodge":-1,
    #0 -> Flash step, #1 -> Ice Cleats, #2 -> Thunder Hook, #3 -> Wind Shield
    
    "room":0,
    #0 -> regular, 1 -> fire, 2 -> ice, 3- -> thunder, 4-> wind, 5-> super, 6-> hyper
    "area":0,

}

bombos = 250
"""
The Player's inventory
"""
INV = {

    ##Health, elements, arrows, currency
    "max_hp": 7,
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
    "plant": 1,
    "chanceEmblem": True,
    "lavaBoots": True,
    
    "syringe": True,
    "potion": 9,
    "smoothie": 9,
    "beer": 0,
    "joint":0,
    "speed":0,
    "wallet": 99,
    "money": 99,
    "keys": 1,

    ##Upgrades
    "flameCost": 20,
    "frostCost": 20,
    "boltCost": 20,
    "galeCost": 20,

}


#   Tuple
#   "action", integer
SHORTCUTS = {
    0:[0,0],
    1:[0,0],
    2:[0,0],
    3:[0,0],
    4:[0,0],
    5:[0,0]
}

##How come you cant change this global variable?
##Why do you need to make it a list to mutate?
ACTIVE_SHORTCUT = [0]



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
"%0O, brave human...&&\n\
.....................&&\n\
Much of my men have you\n\
chillingly slain...$$\n\
Thoughtlessly bleak, my view\n\
lacks knowledge to feign...$$\n\
This heart reacts so blue\n\
to frivolous pain...$$\n\
The tears pour for a few...&&\n\
The rage boils their rain...&&\n\
Take hold of my clue,&&\n\
you pitiful stain!$$\n\
This hatred you grew,&&\n\
shall force you to wane!~\n",

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

"darkcloak_1":
"Hmmm... A young warrior?&&\n\
Well, I know it's not much,\n\
but make yourself cozy.\n\
I'll also sell you my\n\
junk if you've got a dime.\n\
You see, I'm regrettably\n\
a big-time hoarder.\n\
So I really should get rid\n\
of all of this s**t.\n\
",

"darkcloak_2":
"Ah, before you leave...&&\n\
You see, there's another man\n\
who prowls 'round these parts\n\
He's a Luminate, a man\n\
of Light.\n\
I've chased him off\n\
several times.\n\
Imagine moving here to live\n\
in isolation, but having a\n\
douchebag neighbor that\n\
you can't get rid of.\n\
You'd be in my shoes.&&\n\
I'm usually a pacifist,\n\
but if you see this guy,\n\
do you think you\n\
could kill him?\n",

"darkcloak_3":
"Kill him???&&\n\
Good lord, is that\n\
really necessary, guy?\n",

"darkcloak_4":"Hoo boy. You don't\n\
quite understand.\n\
He's f***ing egregious.&&\n\
I don't think I've ever\n\
used that word in my life.\n\
Look, you don't have to\n\
kill him if you want to,\n\
but if you run into him...&&\n\
I think he might just\n\
convince you otherwise.\n",

"darkcloak_5":
"Huh. Well, I guess\n\
I'll see what happens.\n",

"intro_0":
"Journal of %fKyro Phoenix%~,.\n\
30th Day of Winter,.\n\
Year 160,.$$\n\
I'd like to begin documenting\n\
my experience here in %pVerea%~.$$\n\
Wavering moons glisten above\n\
this %ptroubled continent%~,\n\
illuminating roads paved by\n\
the %pendless stream of dreams%~.$$\n\
%pDreams%~ that egg on\n\
the %rtides of war%~,\n\
which have washed upon\n\
this %pmystic land%~ for ages.$$\n\
As one war ends...$$\n\
Another is always\n\
sure to follow...\n",

# A wavering, moon glistens\n\
# above the troubled continent,\n\
# illuminating roads paved by\n\
# the endless stream of dreams.\n",

"intro_1":
"Four flavors of man\n\
exist in %pVerea%~.\n",

"intro_1l":
"%w(1)%~ The %wLuminates%~ are sophisticated\n\
bringers of %wLight%~. They roam\n\
%pVerea%~ with vibrant dignity.\n",

"intro_1d":
"%d(2)%~ The %dDarklings%~ seek to spread\n\
their %dDarkness%~ with a brutal,\n\
savage disposition.\n",

"intro_1f":
"%f(3)%~ The %fNaturalites%~ produce\n\
miracles with %pnature's blessings%~.\n\
They are proud warriors\n\
who live in isolation.\n",

"intro_1n":
"%b(4)%~ Finally, the %bNonnies%~ make up\n\
those of us who lack elemental\n\
affinity.\n",

"intro_2":
"During the last %rGreat War%~,\n\
the %wLuminates%~ and the %dDarklings%~\n\
joined forces, forming the\n\
%rUnified World Powers%~.$$\n\
Upon emerging victorious,\n\
they declared %wtheir%~ %dkind%~\n\
as the %rsuperior human race%~.\n",

"intro_3":
"Come to find out,\n\
the %rsuperior human\n\
race%~ dreads their own demise.$$\n\
So much so, that the %rPowers%~ have\n\
chosen to quell their fears by\n\
eradicating the four tribes which\n\
compose the %fNaturalite race%~,&&\n\
thus eliminating the threat\n\
of rebellion before the idea\n\
could even manifest in our minds.$$\n\
$aAhhh, Yes!&&\n\
Because the only way\n\
to prevent war is to\n\
start another one!$$\n\
Like clockwork!$~\n",


"intro_4":
"Anyway, the %tThunder%~ and %gWind%~ tribes\n\
were quickly decimated thanks to the\n\
element of surprise.$$\n\
The nomadic %iIce%~ tribe remains\n\
safe, concealed by raging\n\
blizzards.$$\n\
Now we, the %fFire%~ tribe, have\n\
put up a great fight against\n\
the %wsun%~ and %dmoon%~ thus far...$$\n\
%r$sBut we've begun to ignite\n\
our final flames.%~$~$$\n\
My older brother, %fFiri%~,\n\
and I were ordered to take refuge.&&\n\
We've escaped the chaos of the\n\
most recent battle,$$\n\
but not without an army\n\
of %wLight%~ and %dShadow%~\n\
hot on our tails.&&\n\
 $_\n\
 \n\
 \n\
$~%fKyro Phoenix%~$_   $~\n",

"tutorial_1":
"Press Y to shoot arrows.",

"tutorial_2":
"Gleemers will shoot you\n\
unless you stare at them.\n\
Hold the target button\n\
to stare into their eyes.\n",

"tutorial_4":
"Many rooms will reward you\n\
for slaying every enemy.\n\
It's never a bad idea\n\
to bash some heads in.\n",

"null":
"Nothing to see here."


}