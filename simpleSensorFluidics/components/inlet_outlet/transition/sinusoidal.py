
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import numpy as np

class SinusoidalTransition(i3.PCell):
    start_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Start channel template")
    end_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                   doc="Start channel template")

    class Layout(i3.LayoutView):
        length = i3.PositiveNumberProperty(default=100, doc="Length of the transition")
        number_points = i3.PositiveIntProperty(default=101, doc="Number of sampling points a long the transitions")

        def _generate_elements(self, elems):
            start_width = self.start_channel_template.width
            end_width = self.end_channel_template.width

            layer = self.start_channel_template.layer

            u_points = [(0, start_width * 0.5)]
            l_points = [(0, -start_width * 0.5)]

            length_step = self.length / (self.number_points - 1)

            for i in range(1, self.number_points - 1):
                x = length_step * i
                u_points.append((x, np.cos( x / self.length * np.pi) * (start_width - end_width) / 4 + (end_width + start_width) / 4))
                l_points.append((x, -np.cos(x / self.length * np.pi) * (start_width - end_width) / 4 - (
                            end_width + start_width) / 4))

            u_points.append((self.length, end_width * 0.5))
            l_points.append((self.length, -end_width * 0.5))

            l_points.reverse()

            elems += i3.Boundary(layer=layer, shape=i3.Shape(u_points + l_points))

            return elems

        def _generate_ports(self, ports):
            ports += microfluidics.FluidicPort(name='in', position=(0, 0.0),
                                               direction=i3.PORT_DIRECTION.IN,
                                               angle_deg=180,
                                               trace_template=self.start_channel_template
                                               )

            ports += microfluidics.FluidicPort(name='out', position=(self.length, 0),
                                               direction=i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.end_channel_template
                                               )
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass


