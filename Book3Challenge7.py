# _____           _ _    ____
# |  ____ __ _   _(_| |_ / ___| __ _ _ __ ___   ___
# | |_ | '__| | | | | __| |  _ / _` | '_ ` _ \ / _ \
# |  _|| |  | |_| | | |_| |_| | (_| | | | | | |  __/
# |_|  |_|   \__,_|_|\__ \____|\__,_|_| |_| |_|\___|

from colored import fore
from random import randint
from time import sleep


def clearscreen():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def setup():
    print(
        fore.LIGHT_BLUE + "      ____  _       _ \n" +
        fore.LIGHT_PINK_1 + "     / ___|| | ___ | |_ ___ \n" +
        fore.WHITE + "     \___ \| |/ _ \| __/ __| \n" +
        fore.LIGHT_PINK_1 + "      ___) | | (_) | |_\__ \ \n" +
        fore.LIGHT_BLUE + "     |____/|_|\___/ \__|___/ \n")
    input(fore.LIGHT_GRAY + "    Press Any Button To Enter")
    usermoney = 100
    rollprice = 20
    symbols = ["\U0001F352", "\U0001F514", "\U0001F34B", "\U0001F34A", "\U0001F31F", "\U0001F480"]
    return usermoney, rollprice, symbols


def roll():
    crollnums = []
    croll = []
    for i in range(3):
        crollnums.append(randint(0, 5))
        croll.append(symbols[crollnums[i]])
    return crollnums, croll


def main(usermoney, rollprice, symbols):
    while usermoney >= 20:
        crollnums, croll = roll()
        skullsbells, threesame = False, False
        clearscreen()
        rollyn = input(f"You have: {fore.WHITE}{usermoney}{fore.LIGHT_GRAY} credits left.\nDo you want to roll? (y/n)")
        if rollyn.lower() == 'y' or rollyn.lower() == 'yes':
            usermoney = usermoney - rollprice
            print(fore.WHITE+"\n"+croll[0], croll[1], croll[2]+fore.LIGHT_GRAY)
            # Checking for Skulls
            if 5 in crollnums:
                if crollnums.count(5) == 2:
                    usermoney -= 100
                    skullsbells = True
                    print("\nTwo Skulls, 100 Credits Taken Away")
                elif crollnums.count(5) == 3:
                    usermoney = 0
                    skullsbells = True
                    print("\nUnlucky, Three Skulls Means Game Over")
            # Checking for Bells
            if 1 in crollnums:
                if crollnums.count(1) == 3:
                    usermoney += 500
                    skullsbells = True
                    print("\nThree Bells, Jackpot!")
            # Checking for 3 of the same
            if (crollnums[0] == crollnums[1] and crollnums[0] == crollnums[2]) and not skullsbells:
                usermoney += 100
                threesame = True
                print("\nThree Are The Same So You Get 100 Points")
            # Checking for 2 of the same
            if (crollnums[0] == crollnums[1] or crollnums[0] == crollnums[2] or crollnums[1] == crollnums[2]) and not skullsbells and not threesame:
                usermoney += 50
                print("\nTwo Are The Same So You Get 50 Points")
            sleep(1)
        elif rollyn.lower() == 'n' or rollyn.lower() == 'no':
            exit()
    if 19 > usermoney > 0:
        print("\nNot Enough Credits Left")
    print(
        fore.LIGHT_BLUE + "  ____                       ___\n" +
        fore.LIGHT_PINK_1 + " / ___| __ _ _ __ ___   ___ / _ \__   _____ _ __\n" +
        fore.WHITE + "| |  _ / _` | '_ ` _ \ / _ | | | \ \ / / _ | '__|\n" +
        fore.LIGHT_PINK_1 + "| |_| | (_| | | | | | |  __| |_| |\ V |  __| |\n" +
        fore.LIGHT_BLUE + " \____|\__,_|_| |_| |_|\___ \___/  \_/ \___|_|\n"
    )


if __name__ == "__main__":
    usermoney, rollprice, symbols = setup()
    main(usermoney, rollprice, symbols)
