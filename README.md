# estomato
A sublime package to quickly calculate man days and man hour needed for a feature development straight from the selection from text editor
The package will aggregate text which has numeric values representing hour values or day values required to finish a feature i.e.:

```
init 2h
api integration 3h
response preparation 2h
documentation 2h
internal sync 3h
```


After running command `estomato` selecting the above text will produce the following:
```
------------------------------------------------
Mandays required: 1.85 Days
Manhour required: 12.00 Hour
------------------------------------------------
```
at the bottom of the selected text


## Installation

 - Install Package Control - https://packagecontrol.io
 - Run `Add Repository` command
 - Paste `https://github.com/rakibulhaq/estomato`
 - Run `Install Package` command
 - Select `Estomato`

## Usage

Available commands in the Selection Menu:

 - *Estomato* – extracts hour and days values from selected text and summarise at the bottom of the selection

Available commands in the Context Menu (Right click on selected text):

 - *Estomato*
 
Also Available commands using Shortcuts:

 - *Ctrl + Alt + e (Windows/Linux)*
 - *Cmd + Alt + e (MacOS)*
