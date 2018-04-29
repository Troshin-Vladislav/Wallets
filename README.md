Wallets
=======

Convert walluts difference country

Project was wrote on python3 and OS Linux

START
-----

	$ chmod +x wallets.py (unix)
	$ python3 wallets.py
	$ ./wallets.py

OPTIONS
-------

**-ow <str>, --out-wallets <str>:** 
set output wallet (USD, JPY, ...)
**-iw <str>, --in-wallets <str>:** 
set input wallet (USD, JPY, ...)
**-v <float>,--value <float>:** 
set value ( type: float )
**-i <str>,--interface <str>:** 
select interface, have only 2 options (gui, console)
**-d,--debug:** 
information for debug
**-l,--list:** 
print list wallutes and they description on russian language
**-V,--version:** 
print version program and last updates and exit
**-h, --help:** 
print help page
> Note: some options use association, to ( tty | cmd | console; x | gui )


EXAMPLES
--------

***Start in console***

    $ ./wallets.py --interface=console
    
***set in wallute USD, out wallute JPY, and value 2.5***

    ./wallets.py --in-wallets USD --out-wallets JPY --value 2.5
   