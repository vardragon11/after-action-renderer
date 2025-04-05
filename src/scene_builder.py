# ------------------------
# Manim Visualization
# ------------------------

from manim import *

class ScenarioVisualizer(Scene):
    def construct(self):
        # Sample hardcoded scenario for demo
        unit_positions = {
            "Alpha Squad": (-4, -2),
            "Bravo Armor": (2, 1),
            "Red Team": (1, -3)
        }

        for name, pos in unit_positions.items():
            dot = Dot(point=pos, radius=0.15)
            label = Text(name).scale(0.4).next_to(dot, UP)
            self.add(dot, label)

        # Draw terrain feature (e.g., building)
        building = Square(side_length=1).move_to((0, 0))
        building_label = Text("Building").scale(0.3).next_to(building, UP)
        self.add(building, building_label)

        # Title
        title = Text("Battlefield Visualization").scale(0.6).to_edge(UP)
        self.add(title)
        self.wait(2)
