
import ipkiss3.all as i3

__all__ = ["Label"]

class Label(i3.PCell):
    class Layout(i3.LayoutView):
        label = i3.StringProperty(default="", doc="label")
        font_size = i3.PositiveNumberProperty(default=25, doc="Height of the text")
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.FLUID.TRENCH, doc="Layer to draw text on")
        alignment = i3.Tuple2Property(default=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.CENTER), doc="Horizontal & vertical alignment" )

        def _generate_elements(self, elems):
            elems += i3.PolygonText(layer=self.layer,
                                    text=self.label,
                                    height=self.font_size,
                                    coordinate=(0, 0),
                                    alignment=self.alignment)
            return elems
