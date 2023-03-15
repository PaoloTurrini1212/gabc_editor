#from pylatex import Document, Command, Package, MiniPage, Center, HugeText, NewLine
#from pylatex.utils import NoEscape
import subprocess as sp
from src.worker import WorkerSignals #, Worker

# Funzione per compilare l'anteprima pdf
def compile_preview(worker_signals: WorkerSignals, gabc):
    #print(gabc)

    worker_signals.partial.emit(("Creo file ausiliario...", None))
    with open("./resources/anteprima.gabc", "w", encoding="utf-8") as file:
        file.write(gabc)
        pass
    print("File ausiliario creato.")

    worker_signals.partial.emit(("Genero la struttura del documento...", None))

    
    with open("./resources/anteprima.tex", "w", encoding="utf-8") as file:
        file.write(build_tex())
        pass

    worker_signals.partial.emit(("Genero il file PDF...", None))
    """ doc.generate_pdf(
        "./resources/anteprima",
        compiler="lualatex",
        clean=False,
        clean_tex=False,
        silent=False,
    ) """
    
    cmd = f'lualatex anteprima.tex anteprima.pdf -interaction=nonstopmode'
    with sp.Popen(cmd, bufsize=1, shell=True, stdout=sp.PIPE, text=True, cwd="./resources") as sub:
        #print(sub)
        for line in sub.stdout:
            worker_signals.partial.emit((None, line))

    print("\nAnteprima PDF generata.")
    #print(output)

def build_tex():
    # Raw LuaLaTeX
    doc = r"""\nonstopmode
\documentclass[preview, border=0.2cm]{standalone}%
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
%\usepackage{textcomp}
\usepackage{lastpage}
\usepackage[cm]{fullpage}
\usepackage{fontspec}
\usepackage{libertine}
\usepackage[autocompile]{gregoriotex}
\usepackage{ragged2e}
%
\begin{document}
\normalsize
\begin{minipage}{\textwidth}
\gresetheadercapture{name}{section*}{}
%
\gresetheadercapture{name}{section*}{}
\gresetheadercapture{annotation}{greannotation}{}
\gresetheadercapture{date}{grecommentary}{}
\gresetheadercapture{commentary}{grecommentary}{}
%
\gresetgregoriofont{greciliae}
\gregorioscore{anteprima}
%
\gresetheadercapture{gabc-copyright}{grecommentary}{}
%
\end{minipage}
\end{document}"""
    return doc

    """
name: incipit;
gabc-copyright: copyright on this gabc file;
score-copyright: copyright on the source score;
office-part: introitus/...;
occasion: in church calendar;
meter: for metrical hymns;
commentary: source of words;
arranger: name of arranger;
author: if known;
date: xi c;
manuscript: ms name;
manuscript-reference: e.g. CAO reference;
manuscript-storage-place: library/monastery;
book: from which score taken;
language: of the lyrics;
transcriber: writer of gabc;
transcription-date: 2009;
mode: 6;
user-notes: whatever other comments you wish to make;
annotation: IN.;
annotation: 6;
"""

""" doc = Document("./resources/anteprima", documentclass="standalone", document_options="preview, border=0.2cm")
    doc.packages.append(Package("fullpage", "cm"))
    doc.packages.append(Package("fontspec"))
    doc.packages.append(Package("libertine"))
    doc.packages.append(Package("gregoriotex", "autocompile"))

    # Titolo
    with doc.create(MiniPage()) as minipage:
        minipage.append(NoEscape(r"\gresetheadercapture{name}{section*}{}"))

        minipage.append(NoEscape(r"\gresetheadercapture{annotation}{greannotation}{}"))
        #doc.append(NoEscape(r"\gresetheadercapture{date}{grecommentary}{}"))
        #doc.append(NoEscape(r"\gresetheadercapture{commentary}{grecommentary}{}"))
        # Spartito vero e proprio
        minipage.append(NoEscape(r"\gregorioscore{anteprima}")) """