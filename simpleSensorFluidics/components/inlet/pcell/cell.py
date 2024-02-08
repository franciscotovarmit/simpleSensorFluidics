
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import numpy as np

import math


from math import factorial
def comb(n, k):
    "k combinations of n"
    v, n1 = 1, n + 1; nk = n1 - k
    for i in range(nk, n1): v *= i
    return v // factorial(k)

def bezier(control_points, num_points=10, end_point=True):
    m,q,p,s=list(zip(*control_points)), len(control_points),[],(num_points - 1 if end_point else num_points)/1.
    for i in range(num_points):
        b=[comb(q - 1, v)*(i / s) ** v *(1 - (i / s))**(q - 1 - v)for v in range(q)]
        p+=[(tuple(sum(j*k for j,k in zip(d,b))for d in m))]
    return p

class _Inlet(i3.PCell):
    """"
    Base class for different types of cell traps
    """
    channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Inport channel template")

    out_channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                                doc="Outport channel template")

    class Layout(i3.LayoutView):
        in_length = i3.PositiveNumberProperty(default=0, doc="Input part of the channel")
        out_length = i3.PositiveNumberProperty(default=400, doc="Output part of the channel")

        radius = i3.PositiveNumberProperty(default=714*0.5, doc="Radius of the outlet")
        length = i3.PositiveNumberProperty(default= 500, doc="Length of the channel from the hole centre")

        def _generate_ports(self, ports):
            # input port

            ports += microfluidics.FluidicPort(name='out', position = (0,self.radius + self.length*0.25),
                                               direction = i3.PORT_DIRECTION.OUT,
                                               angle_deg=90,
                                               trace_template=self.out_channel_template
                                               )

            return ports


    class Netlist(i3.NetlistFromLayout):
        pass

'''
class TrapCupRectangle(_TrapCup):
    """
    Trap Cup with rectangle shapes
    """

    class Layout(_TrapCup.Layout):
        def _generate_elements(self, elems):
            in_width = self.channel_template.channel_width
            out_width = self.out_channel_template.channel_width
            point_list = [(in_width * 0.5, 0),
                          (in_width * 0.45, -self.in_length),
                          (-in_width * 0.45, -self.in_length),
                          (-in_width * 0.5, 0)
                          ]

            shape = i3.Shape(point_list, closed=True)
            boundary = i3.Boundary(self.channel_template.layer, shape)
            elems += boundary

            return elems

'''
class Inlet(_Inlet): #Outlet(_InletOutlet):
    """"

    """

    class Layout(_Inlet.Layout): #Layout(_InletOutlet.Layout):
        def _generate_elements(self, elems):
            layer = self.channel_template.layer
            circle = i3.Circle(layer=layer, center=(0, 0), radius=self.radius)
            print ('len(circle.shape.points)',len(circle.shape.points))
            p1 = circle.shape.points[int(len(circle.shape.points) / 8)]
            l = self.length - p1[0]

            curve_points = bezier(control_points=[(p1[0], -p1[1]),
                                                  (p1[0] + p1[1] - self.channel_template.width * 0.5, -self.channel_template.width * 0.5),
                                                  ((self.length, -self.channel_template.width * 0.5))
                                                 ],
                                  num_points=101
                                  )

            curve_points_mirror = bezier(control_points=[p1,
                                                  (p1[0] + p1[1] - self.channel_template.width * 0.5,
                                                   self.channel_template.width * 0.5),
                                                  ((self.length, self.channel_template.width * 0.5))
                                                  ],
                                  num_points=101
                                  )

            curve_points_mirror.reverse()

            funnel = i3.Boundary(layer=layer, shape=i3.Shape(curve_points_mirror + curve_points).transform(i3.Rotation(rotation=90)))  #ft added rotation

            elems += (circle | funnel)
            return elems