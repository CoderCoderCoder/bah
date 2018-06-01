# Bots Against Humanity

A card game for AI winter nights


### The simple Python simulation

The purpose of the simulation is to collect the data from a human player.
There is no opponent and no objective: just pick a card that you think is funny/interesting. 
Then repeat.


Running is easy (no requirements):

```bash
python3 game.py
```

Enter the name when prompted - any string will do, it's just an id to tell different players apart. (_WE ARE FULLY GDPR-COMPLIANT!_)

Read a black card, pick a number to choose a white card, or press `q` to quit (`Ctrl-C` also works)

The game ends when it runs out of cards, and can be relaunched again, giving different choices.

All the choices data is stored in `data.csv`

That's it.