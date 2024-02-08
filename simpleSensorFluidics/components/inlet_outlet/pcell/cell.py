
import sys

sys.path.append("C:/pdk/")
sys.path.append("../../../")
#sys.path.append("C:/Work/Software/")  # Need to change the path to the folder containing icrofluidics_ipkiss3 and microfluidics_pdk
#sys.path.append("../../../")

# Import basic microfluidics PDK
import microfluidics_pdk.all as pdk

# Import IPKISS3 Packages.
from ipkiss3 import all as i3

# Import microfluidics API.
import microfluidics_ipkiss3.all as microfluidics

from ipkiss3 import all as i3
import numpy as np

from ..transition import SinusoidalTransition

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

class _InletOutlet(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                             doc="Main channel template")

    class Layout(i3.LayoutView):
        radius = i3.PositiveNumberProperty(default=75, doc="Radius of the outlet")
        length = i3.PositiveNumberProperty(default=50, doc="Length of the channel from the hole centre")

        def _generate_ports(self, ports):
            ports += microfluidics.FluidicPort(name='out', position=(self.length, 0),
                                               direction=i3.PORT_DIRECTION.OUT,
                                               angle_deg=0,
                                               trace_template=self.channel_template
                                               )
            return ports
    class Netlist(i3.NetlistFromLayout):
        pass

class Outlet(_InletOutlet):
    """"

    """

    class Layout(_InletOutlet.Layout):
        def _generate_elements(self, elems):
            layer = self.channel_template.layer
            circle = i3.Circle(layer=layer, center=(0, 0), radius=self.radius)

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

            funnel = i3.Boundary(layer=layer, shape=i3.Shape(curve_points_mirror + curve_points))

            elems += (circle | funnel)
            return elems

class Inlet(_InletOutlet):
    """"

    """

    class Layout(_InletOutlet.Layout):
        debris_trap_radius = i3.PositiveNumberProperty(default=30, doc="Radius of the debris trap pillars")
        debris_trap_spacing = i3.PositiveNumberProperty(default=80, doc="Spacing between debris trap pillars")
        debris_trap_location = i3.PositiveNumberProperty(default=2400, doc="Radius of the curve of debris trap pillars")


        def _generate_elements(self, elems):
            layer = self.channel_template.layer
            circle = i3.Circle(layer=layer, center=(0, 0), radius=self.radius)

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

            funnel = i3.Boundary(layer=layer, shape=i3.Shape(curve_points_mirror + curve_points))

            inlet = (circle | funnel)

            circle = i3.Circle(layer=layer, center=(0, 0), radius=self.debris_trap_location)
            boundary1 = inlet[0] & circle
            boundary2 = inlet[0] - circle

            angle_step = np.arcsin(self.debris_trap_spacing / self.debris_trap_location / 2) * 2

            for i in range(-int(np.pi / 4 / angle_step), int(np.pi / 4 / angle_step) + 1):
            #for i in range(3, 10):
                center = (np.cos(angle_step * i) * self.debris_trap_location, np.sin(angle_step * i) * self.debris_trap_location)
                pillar = i3.Circle(layer=layer, center=center, radius=self.debris_trap_radius)
                #layout = i3.LayoutCell().Layout(elements=inlet[0] + pillar)
                #layout.visualize()
                try:
                    boundary1 = boundary1[0] - pillar
                    boundary2 = boundary2[0] - pillar
                except:
                    pass

            circle = i3.Circle(layer=layer, center=(0, 0), radius=self.debris_trap_location + self.debris_trap_spacing)
            boundary3 = boundary2[0] & circle
            boundary4 = boundary2[0] - circle

            for i in range(-int(np.pi / 4 / angle_step), int(np.pi / 4 / angle_step) + 1):
                center = (np.cos(angle_step * (i + 0.5)) * (self.debris_trap_location + self.debris_trap_spacing),
                          np.sin(angle_step * (i + 0.5)) * (self.debris_trap_location + self.debris_trap_spacing))
                pillar = i3.Circle(layer=layer, center=center, radius=self.debris_trap_radius)
                try:
                    boundary3 = boundary3[0] - pillar
                    boundary4 = boundary4[0] - pillar
                except:
                    pass

            elems += (boundary1 + boundary3 + boundary4)
            return elems


class _InletOutletWithLeadin(i3.PCell):
    channel_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT,
                                                             doc="Main channel template")

    inlet_outlet = i3.ChildCellProperty(locked=True)
    transition = i3.ChildCellProperty(locked=True)
    leadin_template = i3.ChildCellProperty(locked=True)

    def _default_inlet_outlet(self):
        pass

    def _default_leadin_template(self):
        channel = i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT
        return channel

    def _default_transition(self):
        return SinusoidalTransition(start_channel_template=self.leadin_template,
                                    end_channel_template=self.channel_template)

    class Layout(i3.LayoutView):
        radius = i3.PositiveNumberProperty(default=75, doc="Radius of the outlet")
        funnel_length = i3.PositiveNumberProperty(default=50, doc="Length of the funnel from the hole centre")
        leadin_width = i3.PositiveNumberProperty(default=200, doc="Length of the funnel from the hole centre")
        leadin_length = i3.PositiveNumberProperty(default=2000, doc="Length of the funnel from the hole centre")
        transition_length = i3.PositiveNumberProperty(default=200, doc="Length of the transition to the in/out channel")

        def _default_leadin_template(self):
            lo = self.cell.leadin_template.get_default_view(i3.LayoutView)
            lo.width = self.leadin_width
            return lo

        def _default_transition(self):
            lo = self.cell.transition.get_default_view(i3.LayoutView)
            lo.length = self.transition_length
            return lo

        def _generate_instances(self, insts):
            leadin = microfluidics.Channel(trace_template=self.cell.leadin_template)
            leadin.Layout(shape=[(0, 0), (self.leadin_length, 0)])
            insts += i3.place_insts(
                insts={'inlet_outlet': self.cell.inlet_outlet,
                       'leadin': leadin,
                       'transition': self.cell.transition},
                specs=[i3.Place('inlet_outlet', (0, 0)),
                       i3.Join([('inlet_outlet:out', 'leadin:in'), ('leadin:out', 'transition:in')])
                       ]
            )

            return insts

        def _generate_ports(self, ports):
            return i3.expose_ports(self.instances,
                                   {'transition:out':'out'})

    class Netlist(i3.NetlistFromLayout):
        pass

class InletWithLeadin(_InletOutletWithLeadin):
    def _default_inlet_outlet(self):
        inlet = Inlet(channel_template=self.leadin_template)
        return inlet

    class Layout(_InletOutletWithLeadin.Layout):
        debris_trap_radius = i3.PositiveNumberProperty(default=30, doc="Radius of the debris trap pillars")
        debris_trap_spacing = i3.PositiveNumberProperty(default=80, doc="Spacing between debris trap pillars")
        debris_trap_location = i3.PositiveNumberProperty(default=2400, doc="Radius of the curve of debris trap pillars")

        def _default_inlet_outlet(self):
            lo = self.cell.inlet_outlet.get_default_view(i3.LayoutView)
            lo.radius = self.radius
            lo.length = self.funnel_length
            lo.debris_trap_radius = self.debris_trap_radius
            lo.debris_trap_spacing = self.debris_trap_spacing
            lo.debris_trap_location = self.debris_trap_location
            return lo

class OutletWithLeadin(_InletOutletWithLeadin):
    def _default_inlet_outlet(self):
        outlet = Outlet(channel_template=self.leadin_template)
        return outlet

    class Layout(_InletOutletWithLeadin.Layout):
        def _default_inlet_outlet(self):
            lo = self.cell.inlet_outlet.get_default_view(i3.LayoutView)
            lo.radius = self.radius
            lo.length = self.funnel_length
            return lo


