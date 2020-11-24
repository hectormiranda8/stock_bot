# Dalpone's stock bot

This stock bot is used to track whether or not an item is in stock. The
items are taken from the text files which contains the links of each
corresponding item. Newegg may occasionally remove the item
and add it back to prevent bots such as this one from tracking such item.
Just keep an eye out and update the link for such item.

* src folder
    * For now it only contains the main.py which has all the source code
    for the bot to run. 
    
* urls folder
    * As you can guess.. this is the url folder and the corresponding
    text files for the items in Newegg. Notice that there are two
    different ones for Newegg, that's because the tracking method for
    an item that's sold in a single unit is different from the tracking
    method that's used for an item that's sold in a combo. As long as
    you put the _urls_ in the right place, the bot shouldn't have a
    problem.
    
Latest Python version as of 11/24/2020, Python 3.9.0, was used to compile, I recommend 
using the same version to omit any errors when trying to use it. I will
(in the near future) provide a release version of the bot which will run
in the command prompt. 

## TODOs
* Config file, to include:
    * firefox/chrome installation path
    * booleans to decide whether to open firefox, chrome or both
    * booleans for whether or not the browser should be opened when an item
    is found in stock
    * firefox/chrome user agent (just google "my user agent" and copy
    paste the result into the field)
* Make the links be looked upon concurrently for faster processing