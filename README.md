# GABC Editor 0.1.1 (alpha)

_(C) 2023 Paolo Turrini_

## Description

Graphical interface and text editor for GABC language and typesetting of gregorian chant using `LuaLaTeX + Gregorio`.

## Prerequisites: LaTeX distribution

GABC Editor is being developed on Windows 10. It has not yet been tested on other OSes.
A previously installed LaTeX distribution and the Gregorio library are required. The two most common LaTeX distributions are **TexLive** and **MikTeX**. MikTeX is recommended for its easier and faster setup, usage and library management (especially for inexperienced users).

Please ensure you have enough disk space for the LaTeX installation (1.2 GB minimum, or about 5 GB for a full installation).
A base LaTeX installation plus the `gregoriotex` package (less than 70 MB) and a few other lightweight libraries which should be included in the installation (if not, they can also be downloaded later) should be enough for this application to work.

### MikTeX

1. Follow the [MikTeX installation instructions](https://miktex.org/howto/install-miktex) (_tl;dr_: download and run the installer). You can keep the default options.
2. After installing MikTeX, open the MikTeX console (if there's a choice between User and Administrator mode, choose Administrator).
3. Select the _Packages_ tab and look for `gregoriotex`. If it's not there, try updating the package list (menu _Tasks_ -> _Refresh file name database_).
4. Select the `gregoriotex` package from the list and install it (with the + button).

### TexLive

1. Follow the [TeXLive installation instructions](https://www.tug.org/texlive/windows.html) (_tl;dr_: download and run the installer). You can keep the default options.
2. [Install the `gregoriotex` package if not present.]

## Installation

_TODO_

## Usage

Write the GABC code and press the Compile button (shortcut: `Ctrl + P`). The compilation process may take a few seconds; the score will appear in the preview on the left side.

## License

MIT License
(see LICENSE.txt)

## Features in progress

- Settings for the layout of the compiled page
- Export as image and other formats
- Special characters map

## Wishlist

- Graphical WYSIWYG editor for GABC (beside the existing text editor)

---

# Version history

## Pre-release

### 0.1.1

- (WIP) fixing file management
- (WIP) adding settings
- added snippets tool (left sidebar)
- fixed zoom options in pdf preview window

### 0.1.0
Initial commit
- main compilation function
- gabc text editor with syntax coloring
- log window
- crude file management system
- settings management (stub)

---