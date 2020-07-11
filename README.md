# Life

Il gioco è costituito da una arena di dimensioni prefissate, da degli individui (detti eater) che possono muoversi in questa arena e da del cibo.
Lo scopo del gioco è che ogni eater mangi più cibo possibile. Il cibo si rigenera ogni volta.
Ogni eater si muove nell'arena basandosi esclusivamente su ciò che si trova di fronte a lui, sullo stato della sua memoria interna e sul suo genoma che gli consente di stabilire la prossima mossa da compiere.

Ogni eater ha una memoria (stato interno) costituita da un numero compreso tra 0 e 15.
A ogni item in vista è associato un numero che indica cosa c'è di fronte: 0: niente, 1: cibo, 2: parete, 3: eater.
Ogni eater vede solo la casella di fronte a sé.
Ogni possibile mossa è associata a un numero compreso tra 0 a 3, 0: va avanti di una casella, 1 gira a destra, 2 gira di 180 gradi, 3 gira a sinistra.

Il genoma consiste di 128 numeri organizzati in due matrici 4 x 16: 
Matrice di memoria: 64 possibili stati di memoria ottenuti da 4 possibili item in vista (vuoto, cibo, muro, eater) x 16 stati di memoria interna. 
Matrice delle mosse: 64 possibili mosse ottenute in base a 4 possibili item in vista x 16 possbili stati di memoria interna.

L'algoritmo consiste nei seguenti passaggi:
* Inizializza la popolazione degli eater in posizioni e orientamenti casuali.
* Inizializza il genoma con valori casuali.
* Inizializza il cibo in posizioni casuali.
* Se un eater si trova su una casella con del cibo -> incrementa automaticamente il suo score di 1.
* Rigenera il cibo mangiato.
* Per ogni eater guarda cosa c'è di fronte.
* Consulta la matrice delle mosse per stabilire la mossa successiva in base alla memoria interna e a cosa c'è di fronte.
* Consulta la matrice di memoria per stabilire il nuovo stato di memoria interna.
* Esegui la mossa.
* Ritorna al punto 3.

Ad ogni generazione vengono selezionati due indiemi di N individui ciascuno (dove N è la dimensione della popolazione), la probabilità che un individuo venga selezionato è proporzionale al suo score (vedi: https://en.wikipedia.org/wiki/Fitness_proportionate_selection).
Gli individui dei due insiemi vengono accoppiati in modo casuale e ogno coppia genera due figli.
Il genoma dei figli è un mix casuale dei genomi dei genitori.
Il genoma dei figli viene mutato in proporzione al mutation_rate, la mutazione si applica a entrambe le matrici che costituiscono il genoma con lo stesso mutation_rate per ciascuna matrice. 
La mutazione consiste nel sistituire alcuni dei numeri che costituiscono queste matrici con altri numeri casuali.

Questo programma cerca di replicare, con alcune differenze, quanto descritto al seguente indirizzo: http://math.hws.edu/eck/js/genetic-algorithm/ga-info.html

Il programma è stato realizzato con lo scopo di imparare Numpy.

Esempio di utilizzo:

s = SimulationParams(100, 100, 50, 200)
g = GraphicGeneticAlgorithm(s, RouletteWheelSelector(2), 0.5, 25)
g.play(100, 200)
