
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics
import numpy as np

class Arrow(i3.PCell):
    """"
    A line with an arrow
    """

    class Layout(i3.LayoutView):
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.FLUID.TRENCH, doc="Layer to draw on")
        length = i3.PositiveNumberProperty(default=2000, doc="Length of the line")
        line_width = i3.PositiveNumberProperty(default=75, doc="With of the line")
        arrow_width = i3.PositiveNumberProperty(default=250, doc="With of the arrow")

        def _generate_elements(self, elems):
            line = i3.RoundedRectangle(layer=self.layer,
                                       center=(-self.length * 0.5, 0),
                                       box_size=(self.length, self.line_width),
                                       radius=self.line_width * 0.5
                                       )

            arrow = i3.Shape([(- self.arrow_width * 0.75, self.arrow_width * 0.5),
                                                                   (0, 0),
                              (- self.arrow_width * 0.75, -self.arrow_width * 0.5)
                            ])
            rounded_arrow = i3.ShapePathRounded(original_shape=arrow, path_width=self.line_width)

            elems += (line | i3.Boundary(layer=self.layer, shape=rounded_arrow))

            return elems
    class Netlist(i3.NetlistFromLayout):
        pass

class MicroscopyAidMarker(i3.PCell):
    """
    Marker with 4 arrows to help finding small target area on microscope
    """

    class Layout(i3.LayoutView):
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.FLUID.TRENCH, doc="Layer to draw on")
        length = i3.PositiveNumberProperty(default=2000, doc="Length of the line")
        line_width = i3.PositiveNumberProperty(default=75, doc="With of the line")
        arrow_width = i3.PositiveNumberProperty(default=250, doc="With of the arrow")

        box_size = i3.Coord2Property(default=(2000., 1000.), doc="Dimension of the area of the marker")

        def _generate_instances(self, insts):
            arrow = Arrow()
            arrow_lo = arrow.Layout(layer=self.layer,
                                    length=self.length,
                                    line_width=self.line_width,
                                    arrow_width=self.arrow_width)
            angle = np.arctan(float(self.box_size[1]) / float(self.box_size[0])) * 180 / np.pi

            insts += i3.SRef(reference=arrow,
                             position=(-self.box_size[0] * 0.5, self.box_size[1] * 0.5),
                             transformation=i3.Rotation(rotation=-angle)
                             )

            insts += i3.SRef(reference=arrow,
                             position=(self.box_size[0] * 0.5, self.box_size[1] * 0.5),
                             transformation=i3.Rotation(rotation= -180 + angle)
                             )

            insts += i3.SRef(reference=arrow,
                            position=(self.box_size[0] * 0.5, -self.box_size[1] * 0.5),
                            transformation=i3.Rotation(rotation=180 - angle)
                            )

            insts += i3.SRef(reference=arrow,
                            position=(-self.box_size[0] * 0.5, -self.box_size[1] * 0.5),
                            transformation=i3.Rotation(rotation=angle)
                            )

            return insts

    class Netlist(i3.NetlistFromLayout):
        pass
