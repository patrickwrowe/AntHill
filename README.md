AntHill.

Toying around with using PyGame/MatPlotLib as a live visualisation for Monte-Carlo simulations. Making an attempt to simulate the behaviour of ants using "fields" representing ant pheremones, topology, etc, which impact the probability of a Monte-Carlo move being accepted. 

Just a weekend project - and no longer being worked on.

Notes:
Food collection rate with random motion something like 1e-5

<img width="802" alt="Screenshot 2023-03-08 at 23 07 24" src="https://user-images.githubusercontent.com/103279917/223946869-64970c2f-28ff-4f9a-9c99-895a71ab342e.png">

ToDo List:
- Enable ants to withdraw/deposit food. -> Implement "home" or "storage cache" for depositing. 
- Set item-specific quantities to be withdrawn/deposited by default.
- Update found food pheremones when food is withdrawn..
- further tuning of parameters.
- fix apparent bug where bugs (lol) seem to prefer moving vertically rather than horizontally?
- add mask where potential == np.inf to block ants from getting wet.

Nice To Have List:
1. Enable printing of relevant information about tile/square by mouse click.

