from models import *

# ------------------------
# Parser Function
# ------------------------
test_input = """
Title: Operation Dynamo
Description: Allied forces are retreating and preparing for naval evacuation under fire from advancing Axis troops.
Unit: ID=U1, Name=British Infantry, Type=infantry, Strength=85, Allegiance=friendly, X=-3, Y=-2.5
Unit: ID=U2, Name=French Infantry, Type=infantry, Strength=78, Allegiance=friendly, X=-1, Y=-2.2
Unit: ID=U3, Name=German Armor, Type=armor, Strength=92, Allegiance=enemy, X=2, Y=-1.8
Feature: Type=Bunker, X=0, Y=-2, Size=10
Objective: ID=O1, Desc=Evacuate to naval boats, X=4, Y=0.5, Priority=1
Event: Time=00:00, Desc=British Infantry begins fallback to coast, Units=U1, Type=move
Event: Time=00:01, Desc=German Armor advances toward beach, Units=U3, Type=move
"""


def parse_scenario_text(text: str) -> Scenario:
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    units = []
    features = []
    objectives = []
    timeline = []
    title = "Generated Scenario"
    description = ""
    terrain_type = "beach"
    terrain_dims = (1000, 1000)

    for line in lines:
        if line.startswith("Title:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("Description:"):
            description = line.split(":", 1)[1].strip()
        elif line.startswith("Unit:"):
            props = dict(item.split("=") for item in line.split(":", 1)[1].split(", "))
            unit = Unit(
                id=props["ID"],
                name=props["Name"],
                type=props["Type"],
                strength=int(props["Strength"]),
                allegiance=props["Allegiance"],
                position=(float(props.get("X", 0)), float(props.get("Y", 0)))
            )
            units.append(unit)
        elif line.startswith("Feature:"):
            props = dict(item.split("=") for item in line.split(":", 1)[1].split(", "))
            features.append(TerrainFeature(
                type=props["Type"],
                position=(float(props["X"]), float(props["Y"])),
                size=float(props["Size"])
            ))
        elif line.startswith("Objective:"):
            props = dict(item.split("=") for item in line.split(":", 1)[1].split(", "))
            objectives.append(Objective(
                id=props["ID"],
                description=props["Desc"],
                location=(float(props.get("X", 0)), float(props.get("Y", 0))),
                priority=int(props.get("Priority", 1))
            ))
        elif line.startswith("Event:"):
            props = dict(item.split("=") for item in line.split(":", 1)[1].split(", "))
            timeline.append(BattleEvent(
                timestamp=props["Time"],
                description=props["Desc"],
                involved_units=props["Units"].split("|"),
                event_type=props["Type"]
            ))

    return Scenario(
        title=title,
        description=description,
        terrain=Terrain(type=terrain_type, features=features, dimensions=terrain_dims),
        units=units,
        objectives=objectives,
        timeline=timeline
    )