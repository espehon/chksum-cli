#python3



#region: --------------------------------[ Notes ]--------------------------------
# √   

#endregion: Notes




#region: --------------------------------[ To-Do ]--------------------------------
# TODO: add ignore .files option
# TODO: add defaults to description and directory support to description

#endregion: To-Do





#region: --------------------------------[ Imports ]--------------------------------
import os
import argparse
import checksum
from colorama import Fore, init
init(autoreset=True)

#endregion: Imports





#region: --------------------------------[ Variables ]--------------------------------
ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']

dirs = []
files = []
hashes = []
method = 'md5'

parser = argparse.ArgumentParser(
    prog="CHKSUM",
    description = f"Compare two checksums\nAlgorithms:{ALGORITHMS}",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog = "If the first 2 positional arguments are checksums, the algorithm is not needed.\n\tExample 1: chksum ./file1 ./file2 sha512\n\tExample 2: chksum 123456789ABCDEF 123456789ABCDEF",
    add_help = False # free -h from help (-? will be used as help flag)
)

parser.add_argument('-?', '--help', action='help', help="Show this help message and exit.") # make -? help
parser.add_argument('-d', '--dots', action='store_true', help="Ignore '.' (dot) files from directories")
parser.add_argument('position1', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position2', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position3', type=str, nargs='?', help="Checksum, file, or algorithm")

# get args from input

args = parser.parse_args()



#endregion: Variables




#region: --------------------------------[ Functions ]--------------------------------



def trySetAlgorithm(value: str) -> bool:
    global method
    if str.upper(value) in ALGORITHMS:
        method = value
        return True
    return False


def trySetFile(value: str) -> bool:
    if os.path.isfile(value):
        files.append(value)
        return True
    return False


def trySetDir(value: str) -> bool:
    if os.path.exists(value):
        dirs.append(value)
        return True
    return False


def processPositional(value: str):
    """This function will determine what to do with positional arguments (value) that the user passed.
    It will first check if the value is an algorithm, then if it is a file, then directory.
    The value is considered a hashed value if none of the above."""
    
    if not trySetAlgorithm(value):
        if not trySetFile(value):
            if not trySetDir(value):
                hashes.append(str.lower(value)) # checksum returns lowercase


def getHash(path: str,  dir: bool=False) -> str:
    if dir:
        return checksum.get_for_directory(path, hash_mode=method, filter_dots=args.dots)
    else:
        return checksum.get_for_file(path, hash_mode=method)


def compareHashes(hash_1: str, hash_2: str, title: str):
    # compare two strings and highlight differences on output
    # then output True | False


    print(str.upper("[" + title + "]").center(64, '-'))

    outputRow_1 = ""
    outputRow_2 = ""
    largerRow = None
    offset = None
    
    match [len(hash_1), len(hash_2)]:
        case [a, b] if a == b:
            pass
        case [a, b] if a > b:
            offset = len(hash_1) - len(hash_2)
            largerRow = 1
        case [a, b] if a < b:
            offset = len(hash_2) - len(hash_1)
    
    for (a, b) in zip(hash_1, hash_2):
        if a == b:
            outputRow_1 += Fore.GREEN + a
            outputRow_2 += Fore.GREEN + b
        else:
            outputRow_1 += Fore.YELLOW + a
            outputRow_2 += Fore.YELLOW + b
    
    if offset is not None:
        if largerRow == 1:
            outputRow_1 += Fore.RED + hash_1[-offset:]
        else:
            outputRow_2 += Fore.RED + hash_2[-offset:]
    
    print(outputRow_1)
    print(outputRow_2)

    if hash_1 == hash_2:
        print(Fore.LIGHTGREEN_EX + "√ Hashes Match")
    else:
        print(Fore.LIGHTRED_EX + "X Hashes Do Not Match")







#endregion: Functions

#region: --------------------------------[ Testing ]--------------------------------



#endregion: Testing
