# solit_py

# Bestärkendes Lernen am Beispiel von (Peg)Solitär 

Diese README Datei soll eine Übersicht über den im Rahmen des Projekts geschriebenen Code geben, 
damit dieser einfach verwendet, geändert und/oder darauf aufgebaut werden kann.

Zunächst empfiehlt es sich mit Solitär vertraut zu machen.

# Wie wird Solitär gespielt

Gespielt wird auf einem Spielbrett, auf dem Spielfiguren oder Steine nebeneinander verteilt sind. Vor dem Start wird ein Stein entfernt. Aufgabe ist es durch Sprünge am Ende so wenig Steine wie möglich zu hinterlassen, idealerweise nur noch ein Stein in der Mitte des Spielbretts. Es darf immer nur über einen Stein gesprungen werden und der übersprungene Stein entfernt werden. Mögliche Zugrichtungen hängen von der Variante des Spielbretts ab. Beim klassischen Solitär (Englisches Brett), darf horizontal und vertikal gezogen werden. Es gibt zahlreiche Varianten (http://www.onlinesologames.com/peg-solitaire), wobei sich in diesem Projekt auf das Englische Brett, Dreieck und Raute beschränkt wurde.

# Wichtige Files

*SimWorld.py*:

Diese File stellt die Spielbretter und die Spielfiguren bereit, in den Klassen *English()*, *Triangular(n)*, *Diamond(n)*. n steht für die Größe der Kantenlänge der beiden Spielbretter Dreieck und Raute. Das Englische Spielbrett hat eine feste Größe, die nicht geändert werden kann. Für die Spielfiguren bzw. den Zellen auf dem Spielbrett steht die Klasse *Cell(value,row,column)* bereit, wobei *value=1* bedeutet, dass auf Zelle (*row,column*) eine Spielfigur steht. *value=0* bedeutet, dass hier keine Spielfigur steht. Nachfolgend werden die wichtigsten Methoden für die Spielbretter aufgelistet.

-*populate_board()*: Setzt Zellen (Spielsteine) auf das Spielbrett und muss vor dem Spielen aufgerufen werden.

-*set_neighbor_pairs()*: Erstellt Liste von benachbarten Zellen zu den einzelnen Steinen und dient zur späteren Berechnung der möglichen Züge (Aktionen) und muss vor dem Spielen aufgerufen werden.

-*get_actions()*: Liefert eine Liste an möglichen Aktionen zurück.

-*in_final_state()*: Prüft, ob keine Aktionen mehr möglich sind.

-*get_sample_action()*: Gibt eine zufällige, mögliche Aktion zurück.

-*take_action(action)*: Macht den Zug, der in *action* steht.

-*get_board_view()*: Gibt das momentane Spielbrett als 2D-Array zurück und dient als Zustand für späteres lernen.

-*get_previous_state()*: Gibt den letzten Zustand des Spielbretts zurück.

Ein Beispiel für das erzeugen eines Spielbretts:
```bash
import SimWorld

Brett=SimWorld.English()
Brett.populate_board()
Brett.set_neighbor_pairs()
```
So würde man einen zufälligen Zug machen:
```bash
Aktion=Brett.get_sample_action()
Brett.take_action(Aktion)
```
So einen aus der Liste der möglichen Züge:
```bash
Zug_Liste=Brett.get_actions()
Brett.take_action(Zug_Liste[3])
```

*Q_Agent.py*:

Diese File beinhaltet die Klasse *QLearner(alpha,gamma,epsilon,epsilon_decay,alpha_decay,name)*. Sie stellt den Agenten auf Basis des Q-Learning Algorithmuses dar. *alpha* ist die Learning Rate, *gamma* der Discount und *epsilon* die Exploration Rate. *epsiolon_decy* und *alpha_decay* geben an wie schnell *epsilon* bzw. *alpha* absinken und sind optional. Soll *epsilon* oder *alpha* nicht kleiner werden, dann muss der jeweilige Decay Null sein. *name* gibt den Namen der Q-Table File an. Nachfolgend werden die wichtigste Methoden für den Agenten aufgelistet.

-*update_epsilon()*: Aktualisiert den Wert von *epsilon*, falls *epsilon_decay* ungleich Null.

-*update_alpha()*: Aktualisiert den Wert von *alpha*, falls *alpha_decay* ungleich Null.

-*get_next_action(state,actions)*: Gibt die nächste Aktion zurück. Diese wird abhängig von *epsilon* entweder zufällig oder optimiert gewählt.

-*train_agent(sate,actions,chosen_action,prev_state,game_over)*: Aktualisiert die Q-Table.

So wird der Agent erzeugt:
```bash
Agent=Q_Agent.QLearner(0.5,0.5,0.01,0.01,'Table')
```
So würde ein Spielzug mit Aktualisierung der Q-Table aussehen:
```bash
State=Brett.get_board_view()
Zug_Liste=Brett.get_actions()
Aktion=Agent.get_next_action(State,Zug_Liste)
Agent.train_agent(State,Zug_Liste,Aktion,Brett.get_previous_state(),Brett.in_final_state())
Agent.update_epsilon()
Agent.update_alpha()
```

Die Reward Function kann in der File über *ACTIVE_FUNCTION* gändert werden zwischen:

-*normalized_reward*: 

-*strict_reward*:

-*tactical_reward*:
