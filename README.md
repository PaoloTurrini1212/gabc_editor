# GABC Editor 0.1.2 (alpha)

_(C) 2023 Paolo Turrini_

_(Per la versione italiana di questo file, vedi [README_it.md](./README_it.md))_

## Description

GABC Editor is a graphical interface and text editor for GABC language and typesetting of gregorian chant using `LuaLaTeX + Gregorio`.

_Note: the in-app documentation is in italian. Multilingual support will be added in a future version._

## Prerequisites: LaTeX distribution

GABC Editor is being developed on Windows 10. It hasn't been tested on other operating systems yet.

In order to use all features of this software, a previously installed LaTeX distribution and the Gregorio library are required ([LaTeX project site](https://www.latex-project.org/get/)). The two most common LaTeX distributions are **TexLive** and **MikTeX**. MikTeX is recommended for its easier and faster setup, usage and library management (especially for inexperienced users); on the other hand, TexLive should have the Gregorio library preinstalled.

You can check at any time if you have LaTeX installed in your system: open the terminal (or shell), type `latex --version` and press Enter. If you get an error message, LaTeX is not installed; otherwise, you will see your LaTeX version number (along with some other info about your distribution). You should also check if LuaLaTeX and Gregorio are installed by typing these commands: `lualatex --version` and `gregorio --version`.

If you need to install LaTeX, please ensure you have enough disk space for the installation (1.2 GB minimum, or about 5 GB for a full installation).
A base LaTeX installation plus the `gregoriotex` package (less than 70 MB) and a few other lightweight libraries which should be included in the installation (if not, they can also be downloaded later) should be enough for this application to work.

### MikTeX

1. Follow the [MikTeX installation instructions](https://miktex.org/howto/install-miktex) (_tl;dr_: download and run the installer). You can keep the default options.
2. After installing MikTeX, open the MikTeX console (if there's a choice between User and Administrator mode, choose Administrator).
3. Select the _Packages_ tab and look for `gregoriotex`. If it's not there, try updating the package list (menu _Tasks_ -> _Refresh file name database_).
4. Select the `gregoriotex` package from the list and install it (with the + button).

### TexLive

1. Follow the [TeXLive installation instructions](https://www.tug.org/texlive/windows.html) (_tl;dr_: download and run the installer). You can keep the default options.
2. The `gregoriotex` package should be included in the installation.

## Installation

Currently (version 0.1.2 alpha) GABC Editor is released as a compiled executable within the installation folder, together with the resources (icons, auxiliary files, ...) and the configuration files. Once the installation folder has been copied to the desired path (and uncompressed if necessary), it should suffice to run `GabcEditor.exe` from the same folder. It is advisable (especially on Windows) to choose a folder with read/write access (e.g. a subfolder of Desktop or Documents).

The entire GABC Editor folder occupies around 100 MB of disk space. While idle, the application itself occupies 35 MB of memory; compilation with LuaLaTeX can temporarily occupy 300-400 MB of memory.

## Usage

Write the GABC code and press the Compile button. The compilation process may take about 15-20 seconds; the score will appear in the preview on the left side.

## License

GABC Editor is released under MIT license (text: [LICENSE.txt](./LICENSE.txt)).
This software is written in Python 3.10 and uses the [PySide (Qt for Python)](https://www.qt.io/qt-for-python) library (unmodified, version 6.4.3); the latter is released under [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html) license.
The program is built with PyInstaller 5.9.0.
The source code for GABC Editor is available on [this Github repository](https://github.com/PaoloTurrini1212/gabc_editor).

## For developers

This section details the steps for replicating the Python virtual environment and the software build.

### Setup

Clone the repository: `> git clone https://github.com/PaoloTurrini1212/gabc_editor.git`

Create the virtual environment: `> python -m virtualenv venv`

Activate the virtual environment: `> .\venv\Scripts\activate`

Install dependencies: `> pip install PySide6 pyinstaller`

### Build

Use the `.spec` file for quick PyInstaller packaging:

`(venv) > pyinstaller gabc_editor.spec`

## Features under development

- Settings and layout management for compiled TeX page
- Customization for the graphical interface (color theme, fonts, ...)
- Improved syntax highlighting
- Search/replace and autocompleting functions in the text editor
- Support for translation of graphical interface and documentation
- General improvements (compilation speed, feedback messages)
- Graphical WYSIWYG editor for GABC (beside the existing text editor)

---

# Version history

## Pre-release

### 0.1.2

- fixed .gabc file management
- added special character map (quick insert)
- automatic management of page and child widgets geometry
- export output in .png, .jpg, .pdf e .tex formats
- updated documentation

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