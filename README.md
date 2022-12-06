<p align="center">
<a href="https://pypi.org/project/chksum-cli/">
<img align="center" src=""/>
</a>
</p>

# chksum
CLI for comparing two checksums

# Usage
```
CHKSUM [-?] [-i] [-d] position1 position2 [position3]

Calculate and compare the checksums of files or directories.
Can also compare against pasted strings.
ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']

positional arguments:
  position1          Checksum, file, or algorithm
  position2          Checksum, file, or algorithm
  position3          Checksum, file, or algorithm

options:
  -?, --help         Show this help message and exit.
  -i, --interactive  Run in interactive mode.
  -d, --dots         Ignore '.' (dot) files from directories.

If the first 2 positional arguments are checksums, the algorithm is not needed. Default is md5.
```


## Interactive mode




## Authors

- [@espehon](https://www.github.com/espehon)


