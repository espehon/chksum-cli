#python3



#region: --------------------------------[ Notes ]--------------------------------
# √   

#endregion: Notes




#region: --------------------------------[ To-Do ]--------------------------------
# TODO: add ignore .files option

#endregion: To-Do





#region: --------------------------------[ Imports ]--------------------------------
import os
import argparse
import checksum
from colorama import Fore, init
init(autoreset=True)

#endregion: Imports





#region: --------------------------------[ Variables ]--------------------------------
parser = argparse.ArgumentParser(
    prog="CHKSUM",
    description = "Compare two checksums",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog = "If the first 2 positional arguments are checksums, the algorithm is not needed.\n\tExample 1: chksum ./file1 ./file2 md5\n\tExample 2: chksum 123456789ABCDE 123456789ABCDE",
    add_help = False # free -h from help (-? will be used as help flag)
)

parser.add_argument('-?', '--help', action='help', help="Show this help message and exit.") # make -? help
parser.add_argument('position1', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position2', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position3', type=str, nargs='?', help="Checksum, file, or algorithm")

# get args from input
args = parser.parse_args()

hashes = []
files = []
dirs = []
method = None



#endregion: Variables




#region: --------------------------------[ Functions ]--------------------------------



def trySetAlgorithm(value: str) -> bool:
    global method
    ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']
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










#endregion: Functions
