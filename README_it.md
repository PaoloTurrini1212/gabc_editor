# GABC Editor 0.1 (alpha)

_(C) 2023 Paolo Turrini_

## Descrizione

Interfaccia grafica ed editor di testo per il linguaggio GABC e la compilazione di partiture di canti gregoriani tramite `LuaLaTeX + Gregorio`.

## Prerequisiti: distribuzione LaTeX

GABC Editor è sviluppato su Windows 10. Al momento non è testato su altri sistemi operativi.
Occorre avere già installato una distribuzione LaTeX e la libreria Gregorio. Le due distribuzioni LaTeX più comuni sono **TexLive** e **MikTeX**. Si raccomanda MikTeX perché più semplice e veloce come installazione, utilizzo e gestione dei pacchetti (soprattutto per utenti meno esperti).

Assicurarsi di avere spazio sufficiente su disco per l'installazione di LaTeX (1,2 GB minimo, circa 5 GB se si installano tutti i pacchetti). Ai fini di questa applicazione è sufficiente un'installazione LaTeX di base più il pacchetto `gregoriotex` (meno di 70 MB) e pochi altri pacchetti leggeri, che dovrebbero essere inclusi automaticamente nell'installazione (se no, si possono installare in seguito).

### MikTeX

1. Seguire le [istruzioni per installare MikTeX](https://miktex.org/howto/install-miktex) (_tl;dr_: scaricare e avviare l'installer). Si possono lasciare le opzioni di default.
2. Dopo l'installazione, aprire la console MikTeX (se c'è la scelta fra modalità utente e amministratore, scegliere amministratore).
3. Selezionare la scheda _Packages_ (Pacchetti) e controllare se nell'elenco è presente `gregoriotex`. Se non c'è, provare ad aggiornare l'elenco (menu _Tasks_ -> _Refresh file name database_).
4. Selezionare il pacchetto `gregoriotex` dall'elenco e installarlo (pulsante col simbolo +).

### TexLive

1. Seguire le [istruzioni per installare TeXLive](https://www.tug.org/texlive/windows.html) (_tl;dr_: scaricare e avviare l'installer). Si possono lasciare le opzioni di default.
2. [Se non è già presente, installare il pacchetto `gregoriotex`.]

## Installazione

_TODO_

## Utilizzo

Scrivere il codice GABC e premere il pulsante Compila (o i tasti `Ctrl + P`). La compilazione può richiedere alcuni secondi; lo spartito apparirà nell'anteprima sulla destra.

## Licenza

Licenza MIT
(vedi LICENSE.txt)

## Funzionalità in sviluppo

- Impostazioni e scelta del layout della pagina compilata
- Esportazione come immagine
- Mappa caratteri speciali

## Lista desideri

- Editor grafico WYSIWYG per GABC (a fianco di quello testuale già presente)