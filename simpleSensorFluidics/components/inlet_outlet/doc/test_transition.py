import sys
sys.path.append("C:/pdk/")
sys.path.append("../../../")
#sys.path.append("C:/Users/e54491/OneDrive - RMIT University-/Software")
sys.path.append("../")

from microfluidics_pdk.technology import *

# Import IPKISS3 Packages.

from ipkiss3 import all as i3
import microfluidics_pdk.all as pdk


from components.inlet_outlet.transition import SinusoidalTransition

start_channel_template = pdk.FluidChannelTemplate()
start_channel_template.Layout(channel_width=100)

end_channel_template = pdk.FluidChannelTemplate()
end_channel_template.Layout(channel_width=20)

trans = SinusoidalTransition(start_channel_template=start_channel_template, end_channel_template=end_channel_template)
lo = trans.Layout(length=200)

lo.visualize(annotate=True)
