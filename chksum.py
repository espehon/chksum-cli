#python3





#region: --------------------------------[ Imports ]--------------------------------
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
    epilog = "If the first 2 positional arguments are checksums, the algorithm is not needed.\nExample 1: chksum ./file1 ./file2 md5\nExample 2: chksum 123456789ABCDE 123456789ABCDE",
    add_help = False # free -h from help (-? will be used as help flag)
)

parser.add_argument('-?', '--help', action='help', help="Show this help message and exit.") # make -? help
parser.add_argument('position1', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position2', type=str, help="Checksum, file, or algorithm")
parser.add_argument('position3', type=str, nargs='?', help="Checksum, file, or algorithm")

# get args from input
args = parser.parse_args()



#endregion: Variables