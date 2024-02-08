
import sys

sys.path.append("C:/pdk/")
#sys.path.append("C:/Work/Software/")  # Need to change the path to the folder containing icrofluidics_ipkiss3 and microfluidics_pdk


# Import basic microfluidics PDK
import microfluidics_pdk.all as pdk

# Import IPKISS3 Packages.
from ipkiss3 import all as i3

# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics


from components.simple_sensor_fluidics.pcell import SimpleSensorFluidics

simple_sensor_fluidics = SimpleSensorFluidics()
simple_sensor_fluidics_lo = simple_sensor_fluidics.Layout()

simple_sensor_fluidics_lo.visualize(annotate=True)
