import random
import time
import os

if (os.name == 'nt'):
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

# Storytelling device for the Legend of Nico (>W<) #
def nicoPrint(message):
    print(message)
    input()
    clear()

# an actor is character that can "ACT" in the game, e.g. the player an enemy, etc...
class actor:

    # str, int, int, int
    def __init__(self, n, h, a, d):
        self.name = n
        self.health = h
        self.maxHealth = h
        self.attack = a
        self.weapon = item("hands", "not much of note, there's a left one and a right one...very common", "weapon", 0)
        self.defense = d
        self.inventory = inventory()

    # returns int representing damage done
    def performAttack(self):
        nicoPrint(self.name + " attacks!")
        return random.randint(0, self.attack) + self.weapon.getEffect()

    # take damage, OUCH!
    def hit(self, incomingAttack):

        # at the moment defense acts as immediate dampening, simple subtraction
        if incomingAttack > self.defense:
            self.health -= (incomingAttack - self.defense)
            nicoPrint(self.name + " took " + str(incomingAttack - self.defense) + " damage!")
        else:
            nicoPrint(self.name + " dexterously dodged the attack!")
        
        # RIP
        if self.health < 0:
            self.health = 0

    def getStatus(self):
        return (self.health > 0)

    # healu!
    def heal(self, addedHealth):

        self.health += addedHealth
        if (self.health > self.maxHealth):
            self.health = self.maxHealth
        print(self.name + " gained +" + str(addedHealth) + "HP!")

    def equipWeapon(self, newWeapon):

        if newWeapon.getType() == "weapon":
            oldWeapon = self.weapon
            self.weapon = newWeapon
            return oldWeapon

    # transfers ownership of item to inventory!
    def addItemToInventory(self, item, num):
        self.inventory.addItem(item, num)

    # transfers ownership of item to calling function!
    def getItemFromInventory(self, itemName):
        return self.inventory.getItem(itemName)

    # given item name, performs respective action return True if action taken
    def useItemFromInventory(self, itemName):
        item = self.getItemFromInventory(itemName)

        if (item == None):
            nicoPrint("That's illegal! item not found")
            return False

        if item.getType() == "heal":
            self.heal(item.getEffect())
            nicoPrint(item.getDescription())
            return True
        else:
            # if item isn't something we can use, put it back
            self.addItemToInventory(item, 1)
            return False
    
    def searchInventory(self):
        self.inventory.traverse()

class item:

    # str, str, str, int
    def __init__(self, name, description, itemType, effect):
        self.name = name
        self.description = description
        self.type = itemType
        self.effect = effect

    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getType(self):
        return self.type
    
    def getEffect(self):
        return self.effect

class inventory:

    # 2d map where [key1][key2] is [name of item][item itself or number in inventory]
    # example: "rock" maps to an array with 2 items, index 0 is the item itself
    # and index 1 is the number of items of "rock" we have in inventory
    def __init__(self):
        self.items = dict()
    
    # inventory now has ownsership of item
    def addItem(self, item, num):
        if item.getName() in self.items:
            self.items[item.getName()][1] += num
        else:
            initItem = [item, 1]
            self.items[item.getName()] = initItem

    # inventory passes ownership of item to calling function (i.e. its not here anymore, your problem now)
    def getItem(self, itemName):
        requestedItem = None
        if itemName in self.items:
            requestedItem = self.items[itemName][0]
            if self.items[itemName][1] <= 1:
                self.items.pop(itemName)
            else:
                self.items[itemName][1] -= 1
        return requestedItem

    def traverse(self):
        for item in self.items:
            print(item + ": " + str(self.items[item][1]))
        if len(self.items) < 1:
            print("No items in inventory")
        input()
        clear()

    # TODO: make a getInfo() function to print out stats


# nico has health of 25 HP, atack of 5, and def of 1
player = actor("nico", 25, 5, 1)

# lesser sword, +1 attack modifier
lesserSword = item("lesser sword", "An unimpresive sword hardly sharper than a butter knife...but a certian spark in it wispers to you about long forgotten heroes", "weapon", 1)

# rock
rock = item("rock", "The gritty taste is embracing!", "heal", 5)

# equip nico with a lesser sword OwO
player.equipWeapon(lesserSword)

# give nico a rock
player.addItemToInventory(rock, 1)

# slime-san has health of 15 HP, atack of 3, and def of 0 ... but he's not a BAD slime!
# 俺は悪いスライムじゃない！
slime = actor("slime", 15, 5, 1)

battleTalk = ["the slime tries to wiggle menacingly.  you suddenly have a desire to eat jello",
"the slime opens its mouth to say something, but blushes and looks away. social anxiety +3 baka!",
"you wonder how slimes take showers without getting washed down the drain...maybe thats why they're slimey?",
"the slime suddenly becomes nervous...on its lips you read: 'were taxes due last week?'",
"you briefly consider wiggling to the slime, but then think it'd look stupid if you did it",
"the slime jiggles to the music"]

clear()
print("The Legend Of Nico")
print("C 2019 Rudaitis Industries")
nicoPrint("press any button to begin...")

nicoPrint("Chapter 2: Rocky Plains")

nicoPrint("a wild slime approaches!")

nicoPrint("uptempo music beings playing out of thin air!")

while slime.getStatus() and player.getStatus():

    actionPerformed = False

    while not actionPerformed:
        
        print("Perform action! (say \"help\" if you're lost)")

        action = input()

        clear()

        if action == "attack":
            atk = player.performAttack()
            slime.hit(atk)
            actionPerformed = True
        elif action == "search":
            player.searchInventory()
        elif action == "use":
            print("sepecify item name:")
            itemName = input()
            clear()
            actionPerformed = player.useItemFromInventory(itemName)
        elif action == "stats":
            print(player.name + ": " + str(player.health) + "/" + str(player.maxHealth) + " HP")
            print(slime.name + ": " + str(slime.health) + "/" + str(slime.maxHealth) + " HP")
        elif action == "help":
            print("You can perfrom actions by loudly screaming out your intentions to your opponent...you wont look stupid, promise!")
            print("You can shout things such as \"attack\", \"search\", \"use\" and \"stats\"")
        else:
            nicoPrint("you mutter strange words to yourself but nothing happens")
    
    if (slime.getStatus()):
        enemyAtk = slime.performAttack()
        player.hit(enemyAtk)
        print(battleTalk[random.randint(0, len(battleTalk)-1)])

if (player.getStatus()):
    nicoPrint("The slime decides to rethink its life choices and hops away to buy some motivational tapes")
    nicoPrint("5 EXP gained....oh...")
    nicoPrint("...this is awkward...")
    nicoPrint("...there isn't an EXP system yet...")
    nicoPrint("Well thanks for playing bye now!")
else:
    nicoPrint("Congrats you...oh...")
    nicoPrint("Your lifeless body lies on the floor as the slime realizes it commited murder...")
    nicoPrint("Good job, now what is this little slime gonna say to its slimely?...")
    nicoPrint("Try again :(")
