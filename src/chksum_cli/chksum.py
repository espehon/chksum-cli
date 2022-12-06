# Copyright (c) 2022, espehon
# All rights reserved.





#region: --------------------------------[ Imports ]--------------------------------
import os
import argparse
import importlib.metadata
try:
    __version__ = f"chksum {importlib.metadata.version('chksum_cli')} from chksum_cli"
except:
    __version__ = "Package not installed..."

import checksum
from colorama import Fore, init
init(autoreset=True)

#endregion: Imports





#region: --------------------------------[ Classes ]--------------------------------

class StandaloneMode(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.exit(stand_alone(single_run=True))

#endregion: Classes





#region: --------------------------------[ Variables ]--------------------------------

CHKSUM_LICENSE = """  Copyright (c) 2022, espehon\n  All rights reserved."""

ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']

positionals = {}    # for storing positionals their type
method = 'md5'      # default algorithm

parser = argparse.ArgumentParser(
    prog="CHKSUM",
    description = f"Calculate and compare the checksums of files or directories.\nCan also compare against pasted strings. \n{ALGORITHMS = }",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog = f"If the first 2 positional arguments are strings, the algorithm is not needed. Default is {method}.\n\tExample 1: chksum ./file1 ./file2 sha512\n\tExample 2: chksum 123456789ABCDEF 123456789ABCDEF\n\tExample 3: chksum ./dir 123456789ABCDEF",
    add_help = False # free -h from help (-? will be used as help flag)
)


parser.add_argument('-?', '--help', action='help', help="Show this help message and exit.")     # make -? help
parser.add_argument('-v', '--version', action='version', version=__version__, help="Show package version and exit.")     # make -? help
parser.add_argument('-i', '--interactive', action=StandaloneMode, nargs=0, help="Run in interactive mode.")
parser.add_argument('-d', '--dots', action='store_true', help="Ignore '.' (dot) files from directories.")
parser.add_argument('position1', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position2', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position3', type=str, nargs='?', help="Checksum, file, or algorithm")

#endregion: Variables





#region: --------------------------------[ Functions ]--------------------------------
def storeDir(value: str, key: int):
    positionals[key] = {'value': value, 'type': 'dir'}


def storeFile(value: str, key: int):
    positionals[key] = {'value': value, 'type': 'file'}


def storeHash(value: str, key: int):
    positionals[key] = {'value': value, 'type': 'hash'}


def setAlgorithm(value: str):
    global method
    method = str.lower(value)


def hashFile(value: str):
    positionals.append(getHash(value))


def hashDir(value: str):
    positionals.append(getHash(value, dir=True))


def processPositional(value: str, key: int):
    """
    This function will determine what to do with positional arguments (value) that the user passed.
    It will first check if the value is an algorithm, then if it is a file, then directory.
    The value is considered a hashed value if none of the above.
    Files and directories hashed in order of positionals[iteration].
    """
    if str.lower(value) in ALGORITHMS:
        setAlgorithm(value)
    elif os.path.isfile(value):
        storeFile(value, key)
    elif os.path.exists(value):
        storeDir(value, key)
    else:
        storeHash(str.lower(value), key) # checksum returns lowercase


def getHash(path: str,  dir: bool=False) -> str:
    if dir:
        return checksum.get_for_directory(path, hash_mode=method, filter_dots=args.dots)
    else:
        return checksum.get_for_file(path, hash_mode=method)


def compareHashes(hash_1: str, hash_2: str, title: str):
    """
    Compare two strings and highlight differences on output.
    Then output True | False.
    """
    if hash_1.strip() == "" or hash_2.strip() == "":
        print(Fore.YELLOW + "One or more values were blank...")
        return "Value(s) were blank"

    outputRow_1 = ""    # first hash to print
    outputRow_2 = ""    # second hash to print
    largerRow = None    # keeps track of the larger hash
    offset = None       # difference in hash sizes
    width = 0           # for title bar formatting
    
    match [len(hash_1), len(hash_2)]:   # set logic depending on sizes of hashes for coloring (and to continue where zip stops)
        case [a, b] if a == b:
            width = a
        case [a, b] if a > b:
            offset = a - b
            largerRow = 1
            width = a
        case [a, b] if a < b:
            offset = b - a
            width = b
    
    for (a, b) in zip(hash_1, hash_2):  # color matching characters green and non matching yellow (orange)
        if a == b:
            outputRow_1 += Fore.GREEN + a
            outputRow_2 += Fore.GREEN + b
        else:
            outputRow_1 += Fore.YELLOW + a
            outputRow_2 += Fore.YELLOW + b
    
    if offset is not None:  # pickup where zip stopped. Make extra characters red
        if largerRow == 1:
            outputRow_1 += Fore.RED + hash_1[-offset:]
        else:
            outputRow_2 += Fore.RED + hash_2[-offset:]
    
    print()
    print(str.upper("[" + title + "]").center(width, '-'))  # output formatted info
    print(outputRow_1)
    print(outputRow_2)

    if hash_1 == hash_2:    # output the final result
        print(Fore.LIGHTGREEN_EX + "√ Hashes Match\n")
        return True
    else:
        print(Fore.LIGHTRED_EX + "X Hashes Do Not Match\n")
        return False


def cli():
    global method
    global args

    args = parser.parse_args()  # get args from input

    processPositional(args.position1, 1)    # store positional accordingly
    processPositional(args.position2, 2)    # store positional accordingly
    try:
            processPositional(args.position3, 3)    # store optional 3rd positional
    except:
        pass

    if len(positionals) < 2:    # must have at least 2 positionals
        print("Missing positional argument...")
        return "Missing positional"
    
    hashes = []                 # stores the final hashes for output
    iteration = 1               # tracks iteration in the while loop and doubles as a dictionary key
    hashesWerePrepared = True   # is set to False if this script runs the hash. Used to decide output title

    while len(hashes) < 2 and iteration <= 3:   # iterate through stored positionals and hash them accordingly
        if iteration in positionals:
            if positionals[iteration]['type'] == 'dir':
                hashes.append(getHash(positionals[iteration]['value'], dir=True))
                hashesWerePrepared = False
            elif positionals[iteration]['type'] == 'file':
                hashes.append(getHash(positionals[iteration]['value']))
                hashesWerePrepared = False
            elif positionals[iteration]['type'] == 'hash':
                hashes.append(positionals[iteration]['value'])
        iteration += 1
    
    if hashesWerePrepared:
        method = 'Strings'

    if compareHashes(hashes[0], hashes[1], method): # test, format, and output hashes
        return 0
    else:
        return 1
    

def stand_alone(single_run=False):
    """
    This is the standalone version.
    Logic works as follows:
        1. Get 1 of 3 options from user
        2. Determine which option was given
        3. Ask for 1 of 2 remaining options
        4. Determine which option was given
        5. Ask for final option
        6. Test, format, and output hashes
        7. Ask to rerun
    """
    title = f"""\


      _     _                        
     | |   | |                       
  ___| |__ | | _____ _   _ _ __ ___  
 / __| '_ \| |/ / __| | | | '_ ` _ \ 
| (__| | | |   <\__ \ |_| | | | | | |
 \___|_| |_|_|\_\___/\__,_|_| |_| |_|
{CHKSUM_LICENSE}

{ALGORITHMS = }
"""
    user = ""                   # for storing user input
    program_is_running = True   # for controlling the following while loop

    while program_is_running:
        try:
            print(title)

            method = None
            hash_1 = None
            hash_2 = None

            include_dots = None
            tries = 3
            hash_strings = 0

            while method is None or hash_1 is None or hash_2 is None:
                match [method, hash_1, hash_2]:
                    case [a, b, c] if a is None and (b is None or c is None):
                        user = input("Enter Algorithm or path to File or Directory > ")
                    case [a, b, c] if a is not None and (b is None or c is None):
                        user = input("Enter path to File or Directory > ")
                    case [a, b, c] if a is None and not (b is None or c is None):
                        user = input("Enter Algorithm > ")

                # if str.lower(user) in ALGORITHMS:
                #     method = str.lower(user)
                # if hash_1 is None:
                #     hash_1 = user
                # elif hash_2 is None:
                #     hash_2 = user
                # else:
                #     print("You've already supplied this requirement...")
                if user.strip() == "":
                    tries -= 1
                    print("\tNothing was entered; please try again.")
                elif str.lower(user) in ALGORITHMS:
                    method = str.lower(user)
                    print("\tAlgorithm entered.")
                else:
                    if os.path.isfile(user):
                        print("\tFile entered.")
                    elif os.path.exists(user):
                        print("\tDirectory entered.")
                    else:
                        print("\tHash string entered.")
                        if hash_1 is None or hash_2 is None:
                            hash_strings += 1
                    if hash_1 is None:
                        hash_1 = user
                    elif hash_2 is None:
                        hash_2 = user
                    else:
                        print("\tYou've already supplied two objects...")
                        tries -= 1
                if hash_strings >= 2:
                    method = "STRINGS" # no need for algorithm
                    break
                elif tries <= 0:
                    print(Fore.YELLOW + "\tNumber of tries exceeded!")
                    raise UserWarning
                

                

            # TODO: #7 user input should be validated on entry, not after all inputs.
            # the following block should be made a function so that it can be called throughout the previous block

            for index, thing in enumerate([hash_1, hash_2]):
                if os.path.isfile(thing):
                    if index == 0:
                        hash_1 = checksum.get_for_file(thing, hash_mode=method)     # calling this manually to be safe
                    else:
                        hash_2 = checksum.get_for_file(thing, hash_mode=method)     # calling this manually to be safe
                elif os.path.exists(thing):
                    if include_dots is None:
                        include_dots = not str.lower(input("Do you want to include '.' (dot) files? [Y/n] > ")).strip() == 'n'   # anything other than 'N' will set this to False
                        print(f"{include_dots = }")
                    if index == 0:
                        hash_1 = checksum.get_for_directory(thing, hash_mode=method, filter_dots= not include_dots)   # have to call this manually without argparse 
                    else:
                        hash_2 = checksum.get_for_directory(thing, hash_mode=method, filter_dots= not include_dots)   # have to call this manually without argparse
                else:
                    if index == 0:
                        hash_1 = str.lower(thing)   # checksum returns lowercase
                    else:
                        hash_2 = str.lower(thing)   # checksum returns lowercase
            
            # Finally output time!
            if compareHashes(hash_1, hash_2, method) and single_run: # test, format, and output hashes
                return 0
            elif single_run:
                return 1

        except KeyboardInterrupt:
            print(Fore.YELLOW + "Keyboard Interrupt!")
        except UserWarning:
            print("\tProgress stopped...")
        except Exception as e:
            print(Fore.LIGHTRED_EX + e)
        program_is_running = False
        if single_run is False:
            try:    # Incase the user mashes keyboard interrupt
                user = str.lower(input("\nEnter R to rerun. Anything else will exit. > "))
                if user == 'r':
                    program_is_running = True
                    print('\n' * 3)
            except KeyboardInterrupt:
                print(Fore.YELLOW + "Exiting program...")
#endregion: Functions



