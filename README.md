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


After running command `Estomato: Run` from command pallet selecting the above text will produce the following:
```
------------------------------------------------
Mandays required: 1.85 Days
Manhour required: 12.00 Hour
------------------------------------------------
```
at the bottom of the selected text


## Installation

 - Run `Package Control: Install Package` in command pallet
 - Select `Estomato`

## Usage
 
Run Pallet command using Shortcuts:

 - *Ctrl + Shift + p (Windows/Linux)*
 - *Cmd + Shift + p (MacOS)*

Type in:

 - *Estomato: Run*

 It will extract hour and days values from selected text and summarise at the bottom of the selection.

 It also detects currency amounts prefixed with symbols or currency labels such as `$`, `USD`, `BDT`, `RM`, `Yen`, and `Won`, and supports prefixed operators like `+`, `-`, or `*3` while summing each detected category.

## Development

Requires `make`, `git` and Python 3. Run `make` to list all targets.

 - `make test` runs the unit tests
 - `make build` builds `dist/Estomato.sublime-package` from `HEAD` (files marked `export-ignore` in `.gitattributes` are left out)

## Releasing

Package Control installs the latest semver tag (`vX.Y.Z`) and shows `messages/X.Y.Z.txt` to users who update.

1. `make bump-patch`, `make bump-minor` or `make bump-major` creates `messages/X.Y.Z.txt` and registers it in `messages.json`
2. Describe the changes in that file and merge it into `main`
3. On `main`, `make release` runs the tests and tags `vX.Y.Z` locally
4. `make push` pushes `main` and the tag, which publishes the release
