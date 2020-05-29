# Better Console
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Python 3.7.5](https://img.shields.io/badge/python-3.7.5-green.svg)](https://www.python.org/downloads/release/python-375/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-green.svg)](http://perso.crans.org/besson/LICENSE.html)

![Filters](/imgs/ezgif-3-e5e15d50dcf7.gif)
![Filters](/imgs/code.png)


Provides a better console for python programs to use


# Installation:
## Prerequisites
python 3.7.5 or above (have no idea if the versions below that work)
PySimpleGuiQt (should install itself when Better Console is installing)

## install
 pip install Better-Console==0.0.6




# Features:
Filters for Debug, Info, Warning, Critical , Error and Normal messages


Text input bar to execute commands


## Usage:
```python
# Example:
import Better_Console

# Create an instance of better console . Warning: Please only create one instance of the object
c=betterConsole.BetterConsole()

# I recommend you to execute this once after creating an instance of better console
c.loop()

# Printing to console
c.print("Test","test")

# Logging
c.debug("Test","test")
c.info("Test","test")
c.warn("test","test")
c.crit("Crit TEst","test")
c.error("tset","test")



# Add commands
def func():
  c.print("Example")
c.commandHandler.addCommands({"func":func})

while True:

    #Update Better Console
    c.loop()


```

