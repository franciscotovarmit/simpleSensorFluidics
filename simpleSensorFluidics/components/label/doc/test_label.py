
import sys

sys.path.append("C:/pdk/") # Need to change the path to the folder containing icrofluidics_ipkiss3 and microfluidics_pdk


# Import basic microfluidics PDK
import microfluidics_pdk.all as pdk

# Import IPKISS3 Packages.
from ipkiss3 import all as i3

# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics

from components.label.pcell import Label

label = Label()
label_lo = label.Layout(label="jjjl")

label_lo.visualize()
