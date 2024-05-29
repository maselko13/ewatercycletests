import logging
logging.basicConfig(level=logging.INFO)
import ewatercycle
# Which container engine is used to run the hydrological models
ewatercycle.CFG.container_engine = 'docker'   # or 'docker'
# If container_engine==apptainer then where can the Apptainer images files (*.sif) be found.
ewatercycle.CFG.apptainer_dir = './apptainer-images'
# Directory in which output of model runs is stored. Each model run will generate a sub directory inside output_dir
ewatercycle.CFG.output_dir = './'
# Where can GRDC observation files (<station identifier>_Q_Day.Cmd.txt) be found.
ewatercycle.CFG.grdc_location = './grdc-observations'
# Where can parameters sets prepared by the system administator be found
ewatercycle.CFG.parameterset_dir = './parameter-sets'

ewatercycle.CFG.save_to_file('./ewatercycle.yaml')

a = ewatercycle.CFG.load_from_file('./ewatercycle.yaml')

print(a)
