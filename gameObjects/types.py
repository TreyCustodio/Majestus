"""
This file contains all type  and status data.
"""

#   -----   Status Effects  -----   #
#   Poison: Deal 1 damage per second
#
#   Freeze: Get trapped in a block of ice for 5 seconds
#
#   Burn: Deal 2 damage per second for 5 seconds
#
#   Stun: Stop moving for 2 seconds, then move slow for 5 seconds
#
#   Knock: Get pushed back until you hit a wall
#   or until 5 seconds is up
#
#   Blind (Light and Dark variation): Only see yourself for 5 seconds
# 
#   Blight: Become slow and can't attack for 5 seconds
#   
#   Wither: Get Poisoned and can't be healed for 5 seconds
#   
#   Drunk (player only): Deal 1.5x damage but become 1.5x slower and vision gets blurry.
#
#   High (player only): Receive 1.5x less damage and see secrets but become 2x slower
#
#
#   *Light and Dark sorcery techniques can inflict all of the above.
#   Each of these effects have particle effects.*
#
#   
#   ------------------------------   #
#
#
#
#   -----   Types   -----  #
#   --- Type Statistics --- #
#
#   Resistance: receive multiple times less damage
#   Weakness:   receive multiple times more damage
#   Immunity:   receive 0 damage and not affected by certain status effects
#   Absorption: receive 0 damage and heal as much health as the attack deals
#
#
#   --- Non-Elemental ---   #
#   Not severely affected by any other type.
#   True neutral type.
#
#   Resistance: None
#   Weakness:   None
#   Immunity:   None
#   Absorption: None
#
#
#   --- Skeletal ---    #
#   Undead skeletons that resist everything except
#   Non-elemental attacks.
#   
#   Resistance: All except Non-elemental (1/2x)
#   Weakness:   Non-elemental (2x)
#   Immunity:   Poison, Freeze, Burn, Stun, Knockback
#   Absorption: None
#
#
#   --- Reptillian ---    #
#   Strong, durable, cold-blooded creatures that are easily frozen.
#   They boast high strength, defense, and speed.
#
#   Resistance: Thunder (1/2x)
#   Weakness:   Ice (2x)
#   Immunity:   Poison, Burn, Stun, Fire
#   Absorption: None
#
#
#   --- Avian ---    #
#   Swift, powerful, warm-blooded creatures that are easily burned.
#   They boast high strength, defense, and speed.
#
#   Resistance: Wind (1/2x)
#   Weakness:   Fire (2x)
#   Immunity:   Freeze, Stun, Ice
#   Absorption: None
#
#
#   --- Soulbender ---    #
#   Mysterious beings who play with death and reanimation.
#   They are masters at hunting Luminates and Darklings.
#
#   Resistance: Light, Dark (1/2x)
#   Weakness:   None
#   Immunity:   All statuses
#   Absorption: None
#
#
#   --- Phantom ---    #
#   Apparitions that break the laws of reality.
#
#   Resistance: None
#   Weakness:   None
#   Immunity:   All status effects, Non-elemental
#   Absorption: None
#
#
#   --- Stone ---    #
#   Stalwart creatures that block access to certain areas.
#   Can only be damaged by Non-elemental attacks.
#
#   Resistance: None
#   Weakness: None
#   Immunity: All status effects, All elements except Non-elemental
#   Absorption: None
#
#
#   --- Fire ---    #
#   Beings that carry the blessing of Fire.
#
#   Resistance: Non-elemental (1/2x)
#   Weakness:   Ice (2x)
#   Immunity: Burn
#   Absorption: Fire
#
#
#   --- Ice ---     #
#   Beings that carry the blessing of Ice.
#
#   Resistance: Non-elemental (1/2x)
#   Weakness:   Fire (2x)
#   Immunity:   Freeze
#   Absorption: Ice
#
#
#   --- Thunder ---     #
#   Beings that carry the blessing of Thunder.

#   Resistance: Non-elemental (1/2x)
#   Weakness:   Wind (2x)
#   Immunity:   Stun
#   Absorption: Thunder
#
#
#   --- Wind ---     #
#   Beings that carry the blessing of Wind.

#   Resistance: Non-elemental (1/2x)
#   Weakness:   Thunder (2x)
#   Immunity:   Knockback
#   Absorption: Wind
#
#
#   --- Light ---     #
#   Luminates or creatures blessed by Light.

#   Resistance: Non-elemental (1/2x)
#   Weakness:   Fire, Ice, Thunder, Wind (1.5x)
#   Immunity:   Blind, Blight
#   Absorption: None
#
#
#   --- Dark ---     #
#   Darklings or creatures blessed by Darkness.
#
#   Resistance: Non-elemental (1/2x)
#   Weakness:   Fire, Ice, Thunder, Wind (1.5x)
#   Immunity:   Blind, Wither
#   Absorption: None
#   ---------------------  #
#
#  
#   --- Multi-Types --- #
#   Resistances, Weaknesses, and Immunities stack up
#   Absorption is handled by case


class Non:
    """Non-Elemental"""
    NAME = "Non"

    RESISTANCE = []
    WEAKNESS = []
    IMMUNITY = []
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Skeletal:
    """Skeletal Enemies"""
    NAME = "Skel"

    RESISTANCE = ["Fire", "Ice", "Thunder", "Wind", "Light", "Dark"]
    WEAKNESS = ["Non"]
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Skeletal_Fire:
    """Skeletal Fire-based Enemies"""
    NAME = "Skel_Fire"

    RESISTANCE = ["Thunder", "Wind", "Light", "Dark"]
    WEAKNESS = ["Non", "Ice"]
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock"]
    ABSORPTION = ["Fire"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Skeletal_Ice:
    """Skeletal Ice-based Enemies"""
    NAME = "Skel_Ice"

    RESISTANCE = ["Thunder", "Wind", "Light", "Dark"]
    WEAKNESS = ["Non", "Fire"]
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock"]
    ABSORPTION = ["Ice"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Skeletal_Thunder:
    """Skeletal Thunder-Based Enemies"""
    NAME = "Skel_Thunder"

    RESISTANCE = ["Fire", "Ice", "Light", "Dark"]
    WEAKNESS = ["Non", "Wind"]
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock"]
    ABSORPTION = ["Thunder"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Skeletal_Wind:
    """Skeletal Wind-Based Enemies"""
    NAME = "Skel_Wind"

    RESISTANCE = ["Fire", "Ice", "Light", "Dark"]
    WEAKNESS = ["Non", "Thunder"]
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock"]
    ABSORPTION = ["Wind"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Skeletal_Light:
    """Skeletal Light-Based Enemies. Non-Elemental and Natural Elements
    damage them normally. Immune to Blind and Blight"""

    NAME = "Skel_Light"

    RESISTANCE = ["Light", "Dark"]
    WEAKNESS = []
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock", "Blind", "Blight"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 1

class Skeletal_Dark:
    """Skeletal Dark-Based Enemies. Non-Elemental and Natural Elements
    damage them normally. Immune to Blind and Wither"""

    NAME = "Skel_Dark"

    RESISTANCE = ["Light", "Dark"]
    WEAKNESS = []
    IMMUNITY = ["Poison", "Freeze", "Burn", "Stun", "Knock", "Blind", "Wither"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 1





class Avian:
    """Versatile flyers who fear the heat"""
    NAME = "Avian"

    RESISTANCE = ["Wind"]
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Freeze", "Stun", "Ice"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Avian_Ice:
    """Doubly weak to their natural weakness to fire"""
    NAME = "Avian_Ice"

    RESISTANCE = ["Non", "Wind"]
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Freeze", "Stun", "Ice"]
    ABSORPTION = ["Ice"]

    RES_FACTOR = 2
    WEAK_FACTOR = 3 # Take triple fire damage

class Avian_Thunder:
    """Cancels out their wind resistance"""
    NAME = "Avian_Thunder"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Freeze", "Stun", "Ice"]
    ABSORPTION = ["Thunder"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Avian_Wind:
    """Versatile flyers who fear the heat"""
    NAME = "Avian_Wind"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Fire", "Thunder"]
    IMMUNITY = ["Freeze", "Stun", "Ice"]
    ABSORPTION = ["Wind"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Avian_Fire:
    """The most powerful flyers who absorb their natural weakness"""
    NAME = "Avian_Fire"

    RESISTANCE = ["Non", "Wind"]
    WEAKNESS = ["Ice"]

    IMMUNITY = ["Freeze", "Stun", "Ice", "Burn"]
    ABSORPTION = ["Fire"]

    RES_FACTOR = 2
    WEAK_FACTOR = 1.5




class Reptillian:
    """Venomous Reptiles who fear the cold"""
    NAME = "Rept"

    RESISTANCE = ["Thunder"]
    WEAKNESS = ["Ice"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Fire"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Reptillian_Wind:
    """Cancels out their Thunder Resistance"""
    NAME = "Rept_Wind"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Ice"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Fire"]
    ABSORPTION = ["Wind"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Reptillian_Thunder:
    """Dangerous Reptiles charged by Thunder"""
    NAME = "Rept_Thunder"
    
    RESISTANCE = ["Non"]
    WEAKNESS = ["Ice", "Wind"]
    IMMUNITY = ["Poison, Burn", "Stun", "Fire"]
    ABSORPTION = ["Thunder"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Reptillian_Ice:
    """Reptiles who can channel their cold blood into frosty attacks"""
    NAME = "Rept_Ice"
    
    RESISTANCE = ["Non", "Thunder"]
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Poison, Burn", "Stun", "Fire", "Freeze"]
    ABSORPTION = ["Ice"]

    RES_FACTOR = 2
    WEAK_FACTOR = 1.5 # Technically, their cold blood will still resist heat just a bit

class Reptillian_Fire:
    """Doubly weak to their natural weakness to ice"""
    NAME = "Rept_Fire"
    
    RESISTANCE = ["Non"]
    WEAKNESS = ["Ice"]
    IMMUNITY = ["Poison, Burn", "Stun", "Fire"]
    ABSORPTION = ["Fire"]

    RES_FACTOR = 2
    WEAK_FACTOR = 3



class Soulbender:
    """Protected against Light and Dark.
    Immune to all status effects."""
    NAME = "Soul"

    RESISTANCE = ["Light", "Dark"]
    WEAKNESS = []
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Phantom:
    """Must be damaged with an element.
    Immune to all status effects."""
    NAME = "Phant"

    RESISTANCE = []
    WEAKNESS = []
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                  "Non"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Stone:
    """Must be damaged by a Non-Elemental attack"""
    NAME = "Stone"

    RESISTANCE = []
    WEAKNESS = []
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                "Fire", "Ice", "Thunder", "Wind", "Light", "Dark"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 2

class Stone_Fire:
    """Must be damaged by Ice"""
    NAME = "Stone_Fire"

    RESISTANCE = []
    WEAKNESS = ["Ice"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                "Non", "Fire", "Thunder", "Wind", "Light", "Dark"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 4

class Stone_Ice:
    """Must be damaged by Fire"""
    NAME = "Stone_Ice"

    RESISTANCE = []
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                "Non", "Ice", "Thunder", "Wind", "Light", "Dark"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 4

class Stone_Thunder:
    """Must be damaged by Wind"""
    NAME = "Stone_Thunder"

    RESISTANCE = []
    WEAKNESS = ["Wind"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                "Non", "Fire", "Ice", "Thunder", "Light", "Dark"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 4

class Stone_Wind:
    """Must be damaged by Thunder"""
    NAME = "Stone_Wind"

    RESISTANCE = []
    WEAKNESS = ["Thunder"]
    IMMUNITY = ["Poison", "Burn", "Stun", "Freeze", "Knock", "Blind", "Blight", "Wither",
                "Non", "Fire", "Wind", "Light", "Dark"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 4


class Fire:
    NAME = "Fire"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Ice"]
    IMMUNITY = ["Burn"]
    ABSORPTION = ["Fire"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Ice:
    NAME = "Ice"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Fire"]
    IMMUNITY = ["Freeze"]
    ABSORPTION = ["Ice"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Thunder:
    NAME = "Thunder"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Wind"]
    IMMUNITY = ["Stun"]
    ABSORPTION = ["Thunder"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Wind:
    NAME = "Wind"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Thuder"]
    IMMUNITY = ["Knock"]
    ABSORPTION = ["Wind"]

    RES_FACTOR = 2
    WEAK_FACTOR = 2


class Light:
    NAME = "Light"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Fire", "Ice", "Thunder", "Wind"]
    IMMUNITY = ["Blind", "Blight"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 1.5


class Dark:
    NAME = "Dark"

    RESISTANCE = ["Non"]
    WEAKNESS = ["Fire", "Ice", "Thunder", "Wind"]
    IMMUNITY = ["Blind", "Wither"]
    ABSORPTION = []

    RES_FACTOR = 2
    WEAK_FACTOR = 1.5

