# loop_termal_with_bacteria

#Heat transfer in a circuit with a simplified model of a swarm of bacteria

#termal_loop_19_12_2022_2.py
With the help of this code, the problem of active control of heat transfer by the finite difference method is solved.
A model of thermal convection is implemented in a toroidal vertical contour in the field of the earth's gravity with heating from below and cooling from above from articles [1], [2].
The algorithm of actions is divided into classes (Parameter_Solution, Create_array, Heat_Calc,BuildPlot, #Draw_Polar_Cards, Array_in_txt), which contain special functions for a specific data type.
The 'main' function of the 'Create_array' class starts the program.
This class inherits all the attributes of the 'Parameter_Solution' class and uses them as its own.
The initial data of the thermal field and velocity field arrays are either read from the text file 'Array_in_txt' (codecs, json), or set on the spot.
At each moment of time, the thermal field is calculated using the functions of the 'Heat_Calc' class, where the data array of the thermal field at the previous time is transmitted.
This class is a child and inherits the attributes of the 'Parameter_Solution' class.
Here, the method of finite differences is the main calculation of the temperature field 'term_calc' and the velocity field 'u_calc', as necessary using 'term_calc' and 'term_fluid1' to calculate the boundary conditions and 'sum_term' to calculate the integral by the method of "trapezoids".
'Draw_Polar_Cards' plots the thermal field and velocity field using the matplotlib library in polar coordinates.


#program05_10_heat.py
With the help of this code, the problem of active control of heat transfer with inclusions of micro-cyborgs is solved by the finite difference method.  Micro-cyborgs here move along the thermal gradient in the direction of increasing.
The 'initial' function starts the process of creating a one-dimensional array of the thermal field in and sets the coordinates of the location of the micro-cyborgs at the initial moment of time. 
If the calculation was performed earlier and was written to a file, then the data array was extracted from it (codecs, json).
The 'while t < tend' loop  contains all the calculations of the problem.
At the moment of time, the real coordinates of the location of Micro-cyborgs on the contour are translated into the discrete form 'real_to_disc'. 
The thermal field is calculated by the 'heat_mass' function. 
The forces of repulsion and attraction of micro-cyborgs relative to each other 'heatFinder' are calculated.
The new location of the micro-cyborgs 'movi_mass_pos' is calculated.
The resulting data arrays are visualized by the 'draw_polar' function using the matplotlib library in polar coordinates and at the same time saved as a drawing in a folder (savefig).
The final data array is saved by 'print_mass_to_txt'.


1.	Singer J., Bau H. H. Active control of convection //Physics of Fluids A: Fluid Dynamics. – 1991. – Т. 3. – №. 12. – С. 2859-2865.

2. Singer J., Wang Y. Z., Bau H. H. Controlling a chaotic system // Physical Review Letters. – 1991. – Т. 66. – №. 9. – С. 1123.
