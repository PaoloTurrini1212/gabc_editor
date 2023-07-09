# GABC Editor 0.1 (alpha)

_(C) 2023 Paolo Turrini_

## Descrizione

GABC Editor è un'interfaccia grafica ed editor di testo per il linguaggio GABC e la compilazione di partiture di canti gregoriani tramite `LuaLaTeX + Gregorio`.

## Prerequisiti: distribuzione LaTeX

GABC Editor è sviluppato su Windows 10. Al momento non è testato su altri sistemi operativi.

Per usare tutte le funzionalità del programma, occorre avere già installato una distribuzione LaTeX ([sito del progetto LaTeX](https://www.latex-project.org/get/)) e la libreria Gregorio. Le due distribuzioni LaTeX più comuni sono **TexLive** e **MikTeX**. Si raccomanda MikTeX perché più semplice e veloce come installazione, utilizzo e gestione dei pacchetti (soprattutto per utenti meno esperti); d'altra parte, TexLive dovrebbe avere la libreria Gregorio preinstallata.

Si può controllare in qualsiasi momento se è presente un'installazione LaTeX: aprire il terminale (o la shell), digitare `latex --version` e premere Invio. Se si ottiene un messaggio di errore, LaTeX non è installato; altrimenti si potrà vedere il numero di versione di LaTeX (insieme ad altre informazioni sulla distribuzione). Si consiglia di controllare anche l'installazione di LuaLaTeX e Gregorio tramite questi comandi: `lualatex --version` e `gregorio --version`.

Se si deve installare LaTeX, occorre assicurarsi di avere spazio sufficiente su disco per l'installazione di LaTeX (1,2 GB minimo, circa 5 GB se si installano tutti i pacchetti). Ai fini di questa applicazione è sufficiente un'installazione LaTeX di base più il pacchetto `gregoriotex` (meno di 70 MB) e pochi altri pacchetti leggeri, che dovrebbero essere inclusi automaticamente nell'installazione (se no, si possono installare in seguito).

### MikTeX

1. Seguire le [istruzioni per installare MikTeX](https://miktex.org/howto/install-miktex) (_tl;dr_: scaricare e avviare l'installer). Si possono lasciare le opzioni di default.
2. Dopo l'installazione, aprire la console MikTeX (se c'è la scelta fra modalità utente e amministratore, scegliere amministratore).
3. Selezionare la scheda _Packages_ (Pacchetti) e controllare se nell'elenco è presente `gregoriotex`. Se non c'è, provare ad aggiornare l'elenco (menu _Tasks_ -> _Refresh file name database_).
4. Selezionare il pacchetto `gregoriotex` dall'elenco e installarlo (pulsante col simbolo +).

### TexLive

1. Seguire le [istruzioni per installare TeXLive](https://www.tug.org/texlive/windows.html) (_tl;dr_: scaricare e avviare l'installer). Si possono lasciare le opzioni di default.
2. Il pacchetto `gregoriotex` dovrebbe essere incluso nell'installazione.

## Installazione

Al momento (versione 0.1.2 alpha) GABC Editor è distribuito come eseguibile già compilato nella cartella d'installazione, insieme alle risorse (icone, file ausiliari, ...) e ai file di configurazione. Una volta copiata la cartella d'installazione nel percorso desiderato (e decompressa se necessario), dovrebbe essere sufficiente avviare `GabcEditor.exe` dalla stessa cartella. E' consigliabile, soprattutto su Windows, di scegliere per l'installazione una cartella con accesso di lettura/scrittura (ad esempio una sottocartella del Desktop o di Documenti)

L'intera cartella di GABC Editor occupa circa 100 MB di spazio su disco, di cui 1 MB per l'eseguibile. Il programma avviato (se non si compiono azioni) occupa 35 MB di memoria; la compilazione con LuaLaTeX può occupare temporaneamente 300-400 MB di memoria.

## Utilizzo

Scrivere il codice GABC e premere il pulsante Compila. La compilazione può richiedere circa 15-20 secondi; lo spartito apparirà nell'anteprima sulla destra.

## Licenza

GABC Editor è rilasciato sotto licenza MIT (testo: [LICENSE.txt](./LICENSE.txt)).
Il software usa la libreria [PySide (Qt for Python)](https://www.qt.io/qt-for-python) (non modificata); questa è rilasciata sotto licenza [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html).
Il codice sorgente di GABC Editor si trova su [questo repository Github](https://github.com/PaoloTurrini1212/gabc_editor).

## Per glli sviluppatori

Questa sezione riporta i passaggi per replicare l'ambiente virtuale Python e la build del programma.

### Setup

Clonare il repository: `> git clone https://github.com/PaoloTurrini1212/gabc_editor.git`

Creare l'ambiente virtuale: `> python -m virtualenv venv`

Attivare l'ambiente virtuale: `> .\venv\Scripts\activate`

Installare le dipendenze: `> pip install PySide6 pyinstaller`

### Build

Usare il file `.spec` per la creazione rapida della cartella di distribuzione:

`(venv) > pyinstaller gabc_editor.spec`

## Funzionalità in sviluppo

- Impostazioni e scelta del layout della pagina compilata
- Personalizzazione dell'interfaccia grafica (tema colori, font, ...)
- Miglioramento dell'evidenziatore di sintassi
- Funzioni di ricerca/sostituzione e di autocompletamento nell'editor testuale
- Supporto per traduzioni dell'interfaccia grafica e della documentazione
- Miglioramenti generali (velocità di compilazione, messaggi informativi)
- Editor grafico WYSIWYG per GABC (a fianco di quello testuale già presente)

---

# Storico versioni

## Pre-rilascio

### 0.1.2

- corretta gestione file .gabc
- aggiunta mappa caratteri speciali (inserimento veloce)
- gestione automatica della geometria della finestra e dei widget figli
- funzioni di esportazione in .png, .jpg, .pdf e .tex
- aggiornata documentazione

### 0.1.1

- (in corso) correzione gestione file
- (in corso) aggiunta impostazioni
- aggiunta strumento frammenti (barra laterale sx)
- corretti comandi zoom in anteprima pdf

### 0.1.0
Commit iniziale
- funzione principale di compilazione
- editor di testo gabc con colorazione sintassi
- finestra log
- sistema grezzo di gestione file
- gestione impostazioni (stub)
