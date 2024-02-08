
from ipkiss3 import all as i3
import microfluidics_ipkiss3.all as microfluidics

from ...channel.pcell import Channel
from ...inlet.pcell import Inlet
from ...marker.pcell import MicroscopyAidMarker
from ...label.pcell import Label

class SimpleSensorFluidics (i3.Circuit):
    """
    A full cell channel PCell
    """

    trace_template = microfluidics.ChannelTemplateProperty(default=i3.TECH.PCELLS.FLUID_CHANNEL.DEFAULT, doc="what is this template used for?")

    channel = i3.ChildCellProperty()
    inlet = i3.ChildCellProperty()
    marker = i3.ChildCellProperty()
    id =  i3.ChildCellProperty() #i3.StringProperty(default="SIMPLE SENSOR FLUIDICS", doc="ID of the CHIP")

    def _default_channel(self):
        channel = Channel(in_channel_template = self.trace_template)
        return channel

    def _default_inlet(self):
        inlet = Inlet(channel_template = self.trace_template, out_channel_template=self.trace_template)
        return inlet
    def _default_marker(self):
        marker = MicroscopyAidMarker()
        marker_lo = marker.Layout(length=1000, line_width=60, arrow_width=200, box_size=(13000., 12000.))
        return marker

    def _default_id(self):
        id = Label()
        id_lo = id.Layout(label="SIMPLE SENSOR FLUIDICS", font_size = 700)
        return id

    def _default_insts(self):

        return {'marker': self.marker,
                'idOnChip': self.id,

                'channel': self.channel,
                'inlet': self.inlet,
                'outlet': self.inlet,

                'channel2': self.channel,
                'inlet2': self.inlet,
                'outlet2': self.inlet,

                'channel3': self.channel,
                'inlet3': self.inlet,
                'outlet3': self.inlet,

                'channel4': self.channel,
                'inlet4': self.inlet,
                'outlet4': self.inlet,

                'channel5': self.channel,
                'inlet5': self.inlet,
                'outlet5': self.inlet,

                'channel6': self.channel,
                'inlet6': self.inlet,
                'outlet6': self.inlet,

                }
    
    def _default_specs(self):
        separation = 1335
        specs = [
            i3.Place('marker', (3200,4500)),
            i3.Place('idOnChip', (3200, 11500)),
            #i3.Rotation('idOnChip', (4500, 3500)),

            i3.Place('channel:in', (0, 0)),
            i3.Place('inlet:out', (-800,-900)),#(-900,-800)),
            i3.Place('outlet:out', (-800,8456+900)),#(8456+900,-800)),
            i3.FlipV('outlet'),
            microfluidics.ConnectManhattan([('channel:in','inlet:out')], bend_radius=250),
            microfluidics.ConnectManhattan([('channel:out', 'outlet:out', )], bend_radius=250),


            i3.Place('channel2:in', (0 + separation, 0)),
            i3.Place('inlet2:out', (-600 + separation,-900 )),
            i3.Place('outlet2:out', (-600 + separation, 8456 + 900  )),
            i3.FlipV('outlet2'),
            microfluidics.ConnectManhattan([('channel2:in', 'inlet2:out')], bend_radius=250),
            microfluidics.ConnectManhattan([('channel2:out', 'outlet2:out',)], bend_radius=250),

            i3.Place('channel3:in', (0 + separation*2, 0 )),
            i3.Place('inlet3:out', (-400 + separation*2, -900)),
            i3.Place('outlet3:out', (-400 + separation*2, 8456 + 900 )),
            i3.FlipV('outlet3'),
            microfluidics.ConnectManhattan([('channel3:in', 'inlet3:out')], bend_radius=150),
            microfluidics.ConnectManhattan([('channel3:out', 'outlet3:out',)], bend_radius=150),

            i3.Place('channel4:in', (0 + separation*3, 0)),
            i3.Place('inlet4:out', (400 + separation*3, -900)),
            i3.Place('outlet4:out', (400 + separation*3, 8456 + 900 )),
            i3.FlipV('outlet4'),
            microfluidics.ConnectManhattan([('channel4:in', 'inlet4:out')], bend_radius=150),
            microfluidics.ConnectManhattan([('channel4:out', 'outlet4:out',)], bend_radius=150),

            i3.Place('channel5:in', (0+ separation*4, 0 )),
            i3.Place('inlet5:out', (600 + separation*4,-900 )),
            i3.Place('outlet5:out', (600 + separation*4, 8456 + 900  )),
            i3.FlipV('outlet5'),
            microfluidics.ConnectManhattan([('channel5:in', 'inlet5:out')], bend_radius=250),
            microfluidics.ConnectManhattan([('channel5:out', 'outlet5:out',)], bend_radius=250),

            i3.Place('channel6:in', (0 + separation*5, 0 )),
            i3.Place('inlet6:out', (800 + separation*5,-900 )),
            i3.Place('outlet6:out', (800 + separation*5, 8456 + 900  )),
            i3.FlipV('outlet6'),
            microfluidics.ConnectManhattan([('channel6:in', 'inlet6:out')], bend_radius=250),
            microfluidics.ConnectManhattan([('channel6:out', 'outlet6:out',)], bend_radius=250),
                ]

        return specs
    
    def _default_exposed_ports(self):
        return {
                #'channel:in': 'in',
                #'channel:out': 'out',
                #'outlet:out': 'out',
                #'inlet:out': 'out'
                }

    class Layout(i3.Circuit.Layout):
        pass