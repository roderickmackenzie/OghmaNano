#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Demo by Cai Williams and Roderick MacKenzie 18/07/24
# Released under the MIT license.
#
# To run this script you will need python, OghmaNano and PyOghma installed
# python -m pip install PyOghma

import PyOghma as po

Oghma = po.OghmaNano()
Results = po.Results()


source_simulation = "./"

Oghma.set_source_simulation(source_simulation)

experiment_name = 'NewExperiment'

Oghma.set_experiment_name(experiment_name)

mobility = 1e-5
trap_desnsity = 1e-18
trapping_crosssection = 1e-20
recombination_crosssection = 1e-20
urbach_energy = 40e-3
temperature = 300
intensity = 0.5


experiment_name = 'NewExperiment' + str(1)
Oghma.clone('NewExperiment0')

Oghma.Optical.Light.set_light_Intensity(intensity)
Oghma.Optical.Light.update()

Oghma.Thermal.set_temperature(temperature)
Oghma.Thermal.update()

Oghma.Epitaxy.load_existing()
Oghma.Epitaxy.pm6y6.dos.mobility('both', mobility)
Oghma.Epitaxy.pm6y6.dos.trap_density('both', trap_desnsity)
Oghma.Epitaxy.pm6y6.dos.trapping_rate('both', 'free to trap',trapping_crosssection)
Oghma.Epitaxy.pm6y6.dos.trapping_rate('both', 'trap to free',recombination_crosssection)
Oghma.Epitaxy.pm6y6.dos.urbach_energy('both', urbach_energy)
Oghma.Epitaxy.update()

Oghma.add_job(experiment_name)
Oghma.run_jobs()
