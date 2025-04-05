# ------------------------
# Manim Visualization
# ------------------------

from manim import *


class DunkirkBeachScene(Scene):
    def construct(self):
        # Load SVG representing Dunkirk map or shoreline layout
        dunkirk_svg = SVGMobject("dunkirk_map.svg").scale(2)
        dunkirk_svg.set_fill(opacity=0.3)
        dunkirk_svg.set_color(YELLOW_E)
        self.add(dunkirk_svg)

        # Title
        title = Text("Dunkirk Evacuation - Visualization").scale(0.6).to_edge(UP)
        self.add(title)

        # Units
        british_troop = Dot(point=(-4, -2), radius=0.15, color=GREEN)
        british_label = Text("British Infantry").scale(0.4).next_to(british_troop, UP)
        self.add(british_troop, british_label)

        evac_zone = Square(side_length=1.5, color=WHITE, fill_opacity=0.2).move_to((2, 2))
        evac_label = Text("Evacuation Zone").scale(0.3).next_to(evac_zone, DOWN)
        self.add(evac_zone, evac_label)

        # Animate troop movement to evacuation
        self.wait(1)
        self.play(british_troop.animate.move_to((2, 2)), run_time=3)
        self.wait(1)
        
        # Add final state or completion message
        complete_label = Text("Evacuation Successful").scale(0.5).next_to(evac_zone, UP).set_color(GREEN)
        self.play(FadeIn(complete_label))
        self.wait(2)