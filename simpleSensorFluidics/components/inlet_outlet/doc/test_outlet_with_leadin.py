import sys
sys.path.append("C:/pdk/")
sys.path.append("../../../")
#sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Software")
sys.path.append("../")

from microfluidics_pdk.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import microfluidics_pdk.all as pdk


from components.inlet_outlet.pcell import OutletWithLeadin

main_channel_template = pdk.FluidChannelTemplate()
main_channel_template.Layout(channel_width=50)

outlet = OutletWithLeadin(channel_template=main_channel_template)
outlet_lo = outlet.Layout(radius=400, funnel_length=800, transition_length=500)
outlet_lo.visualize(annotate=True)