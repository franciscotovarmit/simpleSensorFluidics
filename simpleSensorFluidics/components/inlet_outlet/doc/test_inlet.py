import sys
sys.path.append("C:/pdk/")
sys.path.append("../../../")
#sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Software")
sys.path.append("../")

from microfluidics_pdk.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import microfluidics_pdk.all as pdk

from components.inlet_outlet.pcell import Inlet

main_channel_template = pdk.FluidChannelTemplate()
main_channel_template.Layout(channel_width=200)

inlet = Inlet(channel_template=main_channel_template)
inlet_lo = inlet.Layout(radius=2000, length=3000)
inlet_lo.visualize(annotate=True)