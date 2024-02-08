
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

import math

class _Channel(i3.PCell):
    """"
    Base class for different types of cell traps
    """
    in_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Inport channel template")
    out_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Outport channel template")

    class Layout(i3.LayoutView):
        in_length = i3.PositiveNumberProperty(default=4000, doc="Input part of the channel")
        out_length = i3.PositiveNumberProperty(default=10, doc="Output part of the channel")
        width = i3.PositiveNumberProperty(default=250, doc="channel width") #how to link this to template?

        def _generate_ports(self, ports):
            # input port

            ports += microfluidics.FluidicPort(name='in', position = (0, -self.in_length*0.5),
                                               direction = i3.PORT_DIRECTION.IN,
                                               angle_deg=270,
                                               trace_template=self.in_channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out', position = (0, self.in_length * 0.50),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=90,
                                               trace_template=self.out_channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out2', position = (0.0, -self.out_length),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=270,
                                               trace_template=self.out_channel_template
                                               )

            return ports


    class Netlist(i3.NetlistFromLayout):
        pass

class Channel(_Channel):
    """
    Cell channel with rectangle shapes
    """

    class Layout(_Channel.Layout):
        def _generate_elements(self, elems):
            in_length = self.in_length #1000 #self.in_channel_template.channel_width
            in_width = self.width
            out_width = self.out_channel_template.channel_width

            '''
            point_list = [(in_length * 0.5,-in_width*0.5),
                          (in_length * 0.5,in_width*0.5),
                          (-in_length * 0.5,in_width*0.5),
                          (-in_length * 0.50,-in_width*0.5)
                          ]
                          '''


            point_list = [(-in_width*0.5, in_length * 0.5),
                          (in_width*0.5, in_length * 0.5),
                          (in_width*0.5, -in_length * 0.5),
                          (-in_width*0.5, -in_length * 0.50)
                          ]
            shape = i3.Shape(point_list, closed=True)
            boundary = i3.Boundary(self.in_channel_template.layer, shape)
            elems += boundary

            return elems