
import sys

sys.path.append("C:/pdk/")
#sys.path.append("C:/Work/Software/")  # Need to change the path to the folder containing icrofluidics_ipkiss3 and microfluidics_pdk


# Import basic microfluidics PDK
import microfluidics_pdk.all as pdk

# Import IPKISS3 Packages.
from ipkiss3 import all as i3

# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics

from components.marker.pcell import MicroscopyAidMarker

marker = MicroscopyAidMarker()
marker_lo = marker.Layout(length=1000, line_width=60, arrow_width=200, box_size=(2000., 1000.))
marker_lo.visualize()
