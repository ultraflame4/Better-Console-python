# Better Console
Provides a better console for python programs to use

# Installation:
 pip install Better-Console==0.0.2

## Features:
Filters for Debug, Info, Warning, Critical , Error and Normal messages


Text input bar to execute commands


## Usage:
```python
# Example:
import betterConsole
c=betterConsole.BetterConsole()
c.loop()
c.print("Test","test")
c.debug("Test","test")
c.info("Test","test")
c.warn("test","test")
c.crit("Crit TEst","test")
c.error("tset","test")
while True:
    c.loop()


```


# Dependencies:

PySimpleGuiQt
