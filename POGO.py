import random, csv

monList = []
userInfo = []

def makeMonList():
    '''Takes the given file of pokemon and turns it into a list that is easy to use'''
    file = open("PokeList.csv","r")
    file.readline()

    for line in file:
        mon = line.strip().split(",")
        #              Dex num,     name,    min CP,      max cp
        monList.append([int(mon[0]), mon[1], int(mon[2]), int(mon[3])])
    file.close()

def saveUserInfo(username):
    '''Saves userInfo list into a file to be opened later'''
    file = open("{}.csv".format(username), "w", newline="")
    sheet_writer = csv.writer(file, delimiter=",")
    sheet_writer.writerow([userInfo[0]])
    sheet_writer.writerow([userInfo[1]])

    for i in range(2, len(userInfo)):
        sheet_writer.writerow([userInfo[i][0],userInfo[i][1], userInfo[i][2], userInfo[i][3]])

def loadUserInfo(username):
    file = open("{}.csv".format(username), "r")
    userInfo.append(file.readline().strip())
    userInfo.append(int(file.readline()))

    for pokemonLine in file:
        mon = pokemonLine.strip().split(",")
        userInfo.append([int(mon[0]), mon[1], int(mon[2]), int(mon[3])])

def createUserInfo(username):
    """ This will create a user and give them their first pokemon."""
    file = open("{}.csv".format(username), "w", newline="")
    sheet_writer = csv.writer(file, delimiter=",")
    sheet_writer.writerow([username])
    sheet_writer.writerow([0])
    userInfo.append(username)
    userInfo.append(0)

    firstPokemon = getRandomPokemon()
    sheet_writer.writerow(firstPokemon)
    userInfo.append(firstPokemon)

    file.close()

    print("Congratulations! Your first pokemon is a {} with {} CP!".format(userInfo[2][1],userInfo[2][2] ))

def getRandomPokemon():
    '''Returns a pokemon as a list of 3 values. [Dex number, name, CP, Level]'''
    randomMon = monList[getRandomNumber(0, 149)]
    getMoreCandy()
    return [randomMon[0], randomMon[1], random.randint(randomMon[2], randomMon[3]), 1]

def genRandomPokemon():
    '''Returns a pokemon as a list of 3 values. [Dex number, name, CP, Level]'''
    randomMon = monList[getRandomNumber(0, 149)]
    return [randomMon[0], randomMon[1], random.randint(randomMon[2], randomMon[3]), 1]

def getMoreCandy():
    "Adds a random ammount of candy to the user info"
    possibleCandy = [1, 3, 5, 10]
    numrand = getRandomNumber(0,3)
    userInfo[1] = userInfo[1] + possibleCandy[numrand]
    print("Got {} candy!".format(possibleCandy[numrand]))

def getRandomNumber(min, max):
    return random.randint(min, max)

def menu_login():
    print("---------------------------   Welcome to Pokemon Go    ----------------------------")
    print("1. Login")
    print("2. Create Account")
    inp = userinput(2)
    if inp == 1:
        user = input("Input your username: ")
        try:
            loadUserInfo(user)
            print("Login Successful")
            menu_main()
        except:
            print("Login Failed. Please try again.")
            menu_login()
    elif inp == 2:
        print("If account name already exists, it will be overwritten.")
        createUserInfo(input("Choose New account name: "))
        menu_main()

def menu_main():
    while True:
        print("---------------------------          MAIN MENU         ----------------------------")
        print("1. View Current Pokemon")
        print("2. Catch a new Pokemon")
        print("3. Set new active Pokemon")
        print("4. Save")
        inp = userinput(4)
        if inp == 1:
            displayOwnedMons2()
        elif inp == 2:
            pokemonEncounter()
        elif inp == 3:
            menu_monSelect()
        elif inp == 4:
            print("Game Saved!")
            saveUserInfo(userInfo[0])

def menu_monSelect():
    print("---------------------------   Pokemon Selection Menu   ----------------------------")
    print("Selected Pokemon:", userInfo[2][1])
    print("Current CP:", userInfo[2][2])
    print("Current Level:", userInfo[2][3])
    print("Candies:", userInfo[1])
    displayOwnedMons()
    print("\n\nChoose a new pokemon as your selected pokemon.")
    inp = userinput(len(userInfo)-2)
    setCurrentMon(inp-1)
    menu_main()

def setCurrentMon(monIndex):
    temp = userInfo[monIndex+2]
    userInfo[monIndex+2] = userInfo[2]
    userInfo[2] = temp

def displayOwnedMons():
    print("-----------------------------   Current Pokemon   ---------------------------------")
    for i in range(len(userInfo)-2):
        print("{}.{:<12}| CP: {}".format(i+1, userInfo[i+2][1], userInfo[i+2][2]), end="      ")
        if((i+1) % 3 == 0):
            print()
    print()

def displayOwnedMons2():
    print("-----------------------------   Current Pokemon   ---------------------------------")
    for i in range(len(userInfo)-2):
        print("{}.{:<12}| CP: {}".format(i+1, userInfo[i+2][1], userInfo[i+2][2]), end="      ")
        if((i+1) % 3 == 0):
            print()
    print()
    menu_main()

def userinput(optoinsNumber):
    '''Takes an input as a max accepted value. If the user types a 4.8 it will floor it to 4.'''
    while(True):
        userin = -1
        try:
            userin = int(float(input("Please input a number (1-{}): ".format(optoinsNumber))))
        except ValueError:
            print("Please input a number. ", end="")

        if(userin >= 0 and userin <= optoinsNumber):
            return userin
        else:
            print("Please try again.")

def pokemonEncounter():
    print("---------------------------   Wild Pokemon Encounter   ----------------------------")
    pkm = genRandomPokemon()
    print("You found a {} CP {}".format(pkm[2],pkm[1]))
    print("1. Catch")
    print("2. Run")
    inp = userinput(2)
    if inp == 1:
        if catchMinigame():
            userInfo.append(pkm)
            print("Caught {} successfully! Added to pokemon list!".format(pkm[1]))
            getMoreCandy()
            menu_main()
        else:
            print("Failed to catch {}. Returning to menu.".format(pkm[1]))
            menu_main()
    elif inp == 2:
        print("Escaped successfully!")
        menu_main()

def catchMinigame():
    print("This game is called higher or lower. You have 7 guesses to guess a number between 1 and 100")
    randnum = getRandomNumber(1, 100)
    print("A number has been generated.")

    for i in range(6):
        guess = userinput(100)
        if(guess == randnum):
            print("Congrats! The guess was correct!")
            return True
        else:
            if guess > randnum:
                print("Incorrect. The number is lower.")
            elif guess < randnum:
                print("Incorrect. The number is higher.")
    return False

def gameInfo():
    print("Welcome to your favorite game with not enough comments, but no discernible bugs!")
    print("I hope you're ready to have a blast grading another pokemon go game!")
    print("The rules are simple, but has a prerequisite: You must know how to read!")
    print("Rules:")
    print("    - Give us a 100% :P")
    print("    - Play the game and have fun")
    print("    - The rest and user input should be self explanatory if we did a good job.")

def main():
    makeMonList()
    gameInfo()
    menu_login()

if __name__ == '__main__':
    main()