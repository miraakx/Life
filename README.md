# Life

### Descriprion
This program implements a genetic algorithm to evolve a population of individuals (called Eaters) according to the following rules.

The simulation consists of a fixed-size arena, individuals (the Eaters) who can move within this arena, and food.
The goal of the simulation is for each Eater to eat as much food as possible. Food regenerates every time it is eaten.
Each Eater moves in the arena based solely on what is in front of them, the state of their internal memory, and their genome, which determines the next move to make.

Each Eater has a memory (internal state) consisting of a number between 0 and 15.
Each Eater sees only the square directly in front of them; each possible item in view is associated with a number indicating what it is: 

* 0: empty square,
* 1: food,
* 2: wall,
* 3: another Eater

Each possible move is associated with a number between 0 and 3: 

* 0: move forward one square,
* 1: turn right,
* 2: turn 180 degrees,
* 3: turn left

The genome consists of 128 numbers organized into two 4 x 16 matrices:

* Memory Matrix: 64 possible memory states obtained from 4 possible items in view (empty, food, wall, Eater) x 16 internal memory states.
* Move Matrix: 64 possible moves based on 4 possible items in view x 16 possible internal memory states.

The algorithm follows these steps:

* Initialize the population of Eaters in random positions and orientations.
* Initialize the genome with random values.
* Initialize the food in random positions.
* For each Eater, check what is in front of them.
* Consult the Move Matrix to determine the next move based on the internal memory and what is in front of them.
* Execute the move.
* Consult the Memory Matrix to determine the new internal memory state.
* If an Eater lands on a square with food, its score is automatically incremented by one (for technical reasons related to the selection algorithm, the initial score of each Eater is one, not zero).
* Regenerate the eaten food.
* Return to step 4.

The entire process is repeated for a set number of times, and at the end of the repetitions, the genetic algorithm evaluates the score of each Eater and evolves the population.

In each generation, two sets of N individuals are selected (where N is the population size), and the probability of an individual being selected is proportional to their score (see: [Fitness proportionate selection](https://en.wikipedia.org/wiki/Fitness_proportionate_selection).
The individuals in the two sets are randomly paired, and each pair produces two offspring.
The genome of the offspring is a random mix of the parents' genomes.
The offspring's genome is mutated according to the mutation_rate; the mutation is applied to both matrices that make up the genome with the same mutation_rate for each matrix.
The mutation consists of replacing some of the numbers in these matrices with other random numbers.

This program attempts to replicate, with some differences, what is described at the following link: [Genetic Algorithm Info](http://math.hws.edu/eck/js/genetic-algorithm/ga-info.html).

The program was created with the goal of learning Numpy.

### Dependencies

The program depends on the file **graphics.py version 5.0**, which can be downloaded from here: [graphics.py](https://mcsp.wartburg.edu/zelle/python/graphics.py) and should be placed in the same folder as the life.py file.

### Usage

```
s = SimulationParams(100, 100, 50, 200)
g = GraphicGeneticAlgorithm(s, RouletteWheelSelector(2), 0.5, 25)
g.play(100, 200)
```

--------------------------------------------------------------------
### Descrizione

Questo programma implementa un algoritmo genetico per fare evolvere una popolazione di individui (detti Eater) secondo le seguenti regole.  
  
La simulazione è costituita da una arena di dimensioni prefissate, da degli individui (detti appunto Eater) che possono muoversi in questa arena e da del cibo.  
Lo scopo della simulazione è che ogni Eater mangi più cibo possibile. Il cibo si rigenera ogni volta che viene mangiato.  
Ogni Eater si muove nell'arena basandosi esclusivamente su ciò che si trova di fronte a lui, sullo stato della sua memoria interna e sul suo genoma che gli consente di stabilire la prossima mossa da compiere.  
  
Ogni Eater ha una memoria (stato interno) costituita da un numero compreso tra 0 e 15.  
Ogni Eater vede solo la casella di fronte a sé, a ogni possibile item in vista è associato un numero che indica di cosa si tratta: 

* 0: casella vuota
* 1: cibo
* 2: parete
* 3: altro Eater

Ogni possibile mossa è associata a un numero compreso tra 0 a 3, 

* 0: va avanti di una casella,
* 1 gira a destra,
* 2 gira di 180 gradi,
* 3 gira a sinistra

Il genoma consiste di 128 numeri organizzati in due matrici 4 x 16:   
Matrice di memoria: 64 possibili stati di memoria ottenuti da 4 possibili item in vista (vuoto, cibo, muro, Eater) x 16 stati di memoria interna.  
Matrice delle mosse: 64 possibili mosse ottenute in base a 4 possibili item in vista x 16 possbili stati di memoria interna.  
  
L'algoritmo consiste nei seguenti passaggi:  
  
* Inizializza la popolazione degli Eater in posizioni e orientamenti casuali.  
* Inizializza il genoma con valori casuali.  
* Inizializza il cibo in posizioni casuali.  
* Per ogni Eater guarda cosa c'è di fronte.  
* Consulta la matrice delle mosse per stabilire la mossa successiva in base alla memoria interna e a cosa c'è di fronte.  
* Esegui la mossa.  
* Consulta la matrice di memoria per stabilire il nuovo stato di memoria interna.  
* Se un Eater si trova su una casella con del cibo il suo punteggio (score) viene automaticamente incrementato di uno (per ragiorni tecniche legate all'algoritmo di selezione lo score iniziale di ogni Eater è uno e non zero).  
* Rigenera il cibo mangiato.  
* Ritorna al punto 4.  

Il tutto viene ripetuto per un numero prefissato di volte, al termine delle ripetizioni entra in gioco l'algoritmo genetico che valuta il punteggio ottenuto da ogni Eater e fa evolvere la popolazione.

Ad ogni generazione vengono selezionati due insiemi di N individui ciascuno (dove N è la dimensione della popolazione), la probabilità che un individuo venga selezionato è proporzionale al suo score (vedi: https://en.wikipedia.org/wiki/Fitness_proportionate_selection).  
Gli individui dei due insiemi vengono accoppiati in modo casuale e ogno coppia genera due figli.  
Il genoma dei figli è un mix casuale dei genomi dei genitori.  
Il genoma dei figli viene mutato in proporzione al mutation_rate, la mutazione si applica a entrambe le matrici che costituiscono il genoma con lo stesso mutation_rate per ciascuna matrice.  
La mutazione consiste nel sostituire alcuni dei numeri che costituiscono queste matrici con altri numeri casuali.  
  
Questo programma cerca di replicare, con alcune differenze, quanto descritto al seguente indirizzo: http://math.hws.edu/eck/js/genetic-algorithm/ga-info.html  
  
Il programma è stato realizzato con lo scopo di imparare Numpy.  
  
### Dipendenze
  
Il programma dipende dal file graphics.py versione 5.0, il file può essere scaricato da qui: https://mcsp.wartburg.edu/zelle/python/graphics.py e va inerito nella stessa cartella del file life.py.  

### Utilizzo
```
s = SimulationParams(100, 100, 50, 200)  
g = GraphicGeneticAlgorithm(s, RouletteWheelSelector(2), 0.5, 25)  
g.play(100, 200)  
```
