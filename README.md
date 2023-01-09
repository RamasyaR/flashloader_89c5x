# Flash loader for 89c5x microcontrollers.
This software is a Python utility for write/read flash memory for 89C5x microcontroller series.

### To build and install package manually, enter this command:
```sh
$ git clone https://github.com/RamasyaR/flashloader_89c5x.git
$ cd ./flashloader_89c5x/
$ poetry build
$ pip install ./dist/flashloader-x.x.x-py3-none-any.whl
```

### How to use util:
```sh
$ flashloader
Welcome to the flashtool shell. Type help or ? to list commands.

flasher > 
```
```sh
flasher > help

Documented commands (type help <topic>):
========================================
exit  help

Undocumented commands:
======================
chip_info  disconnect  get_checksum  programmer_info  set_cursor  verify
connect    erase       get_pgm       read             status      write 

flasher > 
```