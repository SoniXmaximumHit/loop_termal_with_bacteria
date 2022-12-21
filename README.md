# loop_termal_with_bacteria

#Heat transfer in a circuit with a simplified model of a swarm of bacteria




#program05_10_heat.py
With the help of this code, the problem of active control of heat transfer with inclusions of microkiborgs is solved by the finite difference method.  Micro-cyborgs here move along the thermal gradient in the direction of increasing.
The 'initial' function starts the process of creating a one-dimensional array of the thermal field in and sets the coordinates of the location of the micro-cyborgs at the initial moment of time. 
If the calculation was performed earlier and was written to a file, then the data array was extracted from it (codecs, json).
The 'while t < tend' loop  contains all the calculations of the problem.
At the moment of time, the real coordinates of the location of microkiborgs on the contour are translated into the discrete form 'real_to_disc'. 
The thermal field is calculated by the 'heat_mass' function. 
The forces of repulsion and attraction of micro-cyborgs relative to each other 'heatFinder' are calculated.
The new location of the micro-cyborgs 'movi_mass_pos' is calculated.
The resulting data arrays are visualized by the 'draw_polar' function using the matplotlib library in polar coordinates and at the same time saved as a drawing in a folder (savefig).
The final data array is saved by 'print_mass_to_txt'.
