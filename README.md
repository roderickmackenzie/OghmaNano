OghmaNano - Simulate Organic Solar Cells, Inorganic solar cells, OLEDs and OFETs
================================================================================

OghmaNano is a free organic solar cells model. It is specifically designed to 
simulate bulk-heterojuncton organic solar cells, such as those based on the 
P3HT:PCBM material system. The model contains both an electrical and an optical 
solver, enabling both current/voltage characteristics to be simulated as well 
as the optical modal profile within the device. The model and it's easy to use 
graphical interface is available for both Linux and Windows.
The model can simulate:

    -Dark JV curves
    -Light JV curves
    -Dark CELIV transients
    -Light CELIV transients
    -Voltage transients of an arbitrary shape
    -Full optical model taking into account reflection at interfaces and absorption.
    -Calculation of reflection profile
    -Ability to simulate OLEDs

The physical model solves both electron and hole drift-diffusion, and carrier 
continuity equations in position space to describe the movement of charge 
within the device. The model also solves Poisson's equation to calculate the 
internal electrostatic potential. Recombination and carrier trapping are 
described within the model using a Shockley-Read-Hall (SRH) formalism, the 
distribution of trap sates can be arbitrarily defined. A fuller description of 
the model can be found in the at https://www.Oghma-Nano.com, in the associated
publications  and in the manual.
Example simulations

The model makes it easy to study the influence of material parameters such as 
mobility, energetic disorder, doping and recombination cross-sections on device 
performance. All internal device parameters such as current density, charge 
density, distribution of trapped carriers in position and energy space are 
accessible either through the graphical interface or directly through output 
files. 

Installing/building OghmaNano
==============

1 Windows
----------

I would recommend downloading the binary from the OghmaNano web page.  Double click on the installer and follow the instructions.  I always keep the windows exe up-to date and on the latest stable release.

2 Linux
--------

Download the OghmaNano by issuing the command 

~~~~
git clone  https://github.com/roderickmackenzie/OghmaNano
~~~~

Find your operating system in
~~~~
build_system/dependency_scripts
~~~~

This script should install all the packages you need to run/compile OghmaNano for a given OS.  I don't always keep them up to date, so if you have a new version of an OS and the packages have been renamed you may have to hunt around.


Then run:

~~~~
./build
~~~~

Then select, (compile), and (auto).  Then hit return to build.


Help using OghmaNano
----------------
I'm very happy to provide help in using OghmaNano, or if you wold prefer I am 
equally happy to collaborate and model your data for you. See the contact page.


More information
----------------
More information can be found on the home page https://www.Oghma-Nano.com

Licensing
---------
oghma comes in three parts with different licenses:
- oghma_core: This is licensed under a 3-clause BSD license.
- oghma_gui: This is licensed under a GPLv2 license.
- oghma_build_system: This is also licensed under a BSD 3-clause license
- oghma_data: Creative Commons BY-CC.
See the individual license files for details.
