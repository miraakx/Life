# Life
  
Questo programma implementa un algoritmo genetico per fare evolvere una popolazione di individui (detti Eater) secondo le seguenti regole.  
  
La simulazione è costituita da una arena di dimensioni prefissate, da degli individui (detti appunto Eater) che possono muoversi in questa arena e da del cibo.  
Lo scopo della simulazione è che ogni Eater mangi più cibo possibile. Il cibo si rigenera ogni volta che viene mangiato.  
Ogni Eater si muove nell'arena basandosi esclusivamente su ciò che si trova di fronte a lui, sullo stato della sua memoria interna e sul suo genoma che gli consente di stabilire la prossima mossa da compiere.  
  
Ogni Eater ha una memoria (stato interno) costituita da un numero compreso tra 0 e 15.  
Ogni Eater vede solo la casella di fronte a sé, a ogni possibile item in vista è associato un numero che indica di cosa si tratta: 0: casella vuota, 1: cibo, 2: parete, 3: altro Eater.  

Ogni possibile mossa è associata a un numero compreso tra 0 a 3, 0: va avanti di una casella, 1 gira a destra, 2 gira di 180 gradi, 3 gira a sinistra.  

Il genoma consiste di 128 numeri organizzati in due matrici 4 x 16:   
Matrice di memoria: 64 possibili stati di memoria ottenuti da 4 possibili item in vista (vuoto, cibo, muro, Eater) x 16 stati di memoria interna.  
Matrice delle mosse: 64 possibili mosse ottenute in base a 4 possibili item in vista x 16 possbili stati di memoria interna.  
  
L'algoritmo consiste nei seguenti passaggi:  
  
* Inizializza la popolazione degli Eater in posizioni e orientamenti casuali.  
* Inizializza il genoma con valori casuali.  
* Inizializza il cibo in posizioni casuali.  
* Se un Eater si trova su una casella con del cibo il suo punteggio (score) viene automaticamente incrementato di uno (per ragiorni tecniche legate all'algoritmo di selezione lo score iniziale di ogni Eater è uno e non zero).  
* Per ogni Eater guarda cosa c'è di fronte.  
* Consulta la matrice delle mosse per stabilire la mossa successiva in base alla memoria interna e a cosa c'è di fronte.  
* Esegui la mossa.  
* Consulta la matrice di memoria per stabilire il nuovo stato di memoria interna.  
* Rigenera il cibo mangiato.  
* Ritorna al punto 4.  

Il tutto viene ripetuto per un numero prefissato di volte, al termine delle ripetizioni entra in gioco l'algoritmo genetico che valuta il punteggio ottenuto da ogni Eater e fa evolvere la popolazione.

Ad ogni generazione vengono selezionati due indiemi di N individui ciascuno (dove N è la dimensione della popolazione), la probabilità che un individuo venga selezionato è proporzionale al suo score (vedi: https://en.wikipedia.org/wiki/Fitness_proportionate_selection).  
Gli individui dei due insiemi vengono accoppiati in modo casuale e ogno coppia genera due figli.  
Il genoma dei figli è un mix casuale dei genomi dei genitori.  
Il genoma dei figli viene mutato in proporzione al mutation_rate, la mutazione si applica a entrambe le matrici che costituiscono il genoma con lo stesso mutation_rate per ciascuna matrice.  
La mutazione consiste nel sistituire alcuni dei numeri che costituiscono queste matrici con altri numeri casuali.  
  
Questo programma cerca di replicare, con alcune differenze, quanto descritto al seguente indirizzo: http://math.hws.edu/eck/js/genetic-algorithm/ga-info.html  
  
Il programma è stato realizzato con lo scopo di imparare Numpy.  
  
Esempio di utilizzo:  
  
ATTENZIONE: Il programma dipende dal file graphics.py versione 5.0, il file può essere scaricato da qui: https://mcsp.wartburg.edu/zelle/python/graphics.py e va inerito nella stessa cartella del file life.py.  
  
s = SimulationParams(100, 100, 50, 200)  
g = GraphicGeneticAlgorithm(s, RouletteWheelSelector(2), 0.5, 25)  
g.play(100, 200)  
