# scenario_utils.py

import re
from pydantic import BaseModel
from typing import List, Optional, Tuple
from collections import defaultdict

# -------------------- DATA MODELS --------------------

class Unit(BaseModel):
    id: str
    name: str
    type: str
    strength: int
    position: Optional[Tuple[float, float]] = None
    allegiance: str
    status: str = "active"

class TerrainFeature(BaseModel):
    type: str
    position: Tuple[float, float]
    size: float

class Terrain(BaseModel):
    type: str
    features: List[TerrainFeature]
    dimensions: Tuple[int, int]

class Objective(BaseModel):
    id: str
    description: str
    controlling_unit_ids: List[str] = []
    completed: bool = False
    location: Optional[Tuple[float, float]] = None
    priority: int = 1

class BattleEvent(BaseModel):
    timestamp: str
    description: str
    involved_units: List[str] = []
    location: Optional[Tuple[float, float]] = None
    event_type: str

class Scenario(BaseModel):
    title: str
    description: str
    terrain: Terrain
    units: List[Unit]
    objectives: List[Objective]
    timeline: List[BattleEvent]

# -------------------- TOKENIZER --------------------

KEYWORDS = ['Title', 'Description', 'Unit', 'Feature', 'Objective', 'Event']

def tokenize_by_keyword(text: str):
    text = text.replace("minus", "-")
    pattern = r'\\b(' + '|'.join(KEYWORDS) + r')\\b(?:\\s+is)?'
    tokens = re.split(pattern, text)
    data = defaultdict(list)
    current_key = None
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in KEYWORDS:
            current_key = token
        elif current_key:
            data[current_key].append(token)
    return data

# -------------------- PARSERS --------------------

def parse_unit(chunk: str) -> Unit:
    unit_id = re.compile(r"ID\\s?\\w+\\s?(\\w+)\\.")
    unit_name = re.compile(r"Name\\s?\\w+\\s?(.+?)\\.")
    unit_type = re.compile(r"Type\\s?\\w+\\s?(.+?)\\.")
    unit_ste = re.compile(r"Strength\\s?\\w+\\s?(\\d+)\\.")
    unit_all = re.compile(r"Allegiance\\s?\\w+\\s?(\\w+)\\.")
    unit_x = re.compile(r"X\\s?\\w+\\s?(-?\\d+(?:\\.\\d+)?)\\.")
    unit_y = re.compile(r"Y\\s+\\w+\\s+(-?\\s*\\d+(?:\\.\\d+)?)\\.")
    unit_status = re.compile(r"Status\\s?\\w+\\s?(\\w+)\\.")
    return Unit(
        id=re.findall(unit_id, chunk)[0],
        name=re.findall(unit_name, chunk)[0],
        type=re.findall(unit_type, chunk)[0],
        strength=int(re.findall(unit_ste, chunk)[0]),
        allegiance=re.findall(unit_all, chunk)[0],
        position=(float(re.findall(unit_x, chunk)[0].replace(" ","")),
                  float(re.findall(unit_y, chunk)[0].replace(" ",""))),
        status=re.findall(unit_status, chunk)[0]
    )

def parse_feature(chunk: str) -> TerrainFeature:
    feat_type = re.compile(r'Type\\s?\\w+\\s?(\\w+)\\.')
    feat_x = re.compile(r'X\\s?\\w+\\s?(-?\\d+(?:\\.\\d+)?)\\.')
    feat_y = re.compile(r'Y\\s+\\w+\\s+(-?\\s*\\d+(?:\\.\\d+)?)\\.')
    feat_size = re.compile(r'Size\\s+\\w+\\s(\\d+)\\.')
    return TerrainFeature(
        type=re.findall(feat_type, chunk)[0],
        position=(float(re.findall(feat_x, chunk)[0].replace(" ","")),
                  float(re.findall(feat_y, chunk)[0].replace(" ",""))),
        size=float(re.findall(feat_size, chunk)[0])
    )

def parse_objective(chunk: str) -> Objective:
    obj_id = re.compile(r'ID\\s?\\w+\\s?(\\w+)\\.')
    obj_desc = re.compile(r'Desk\\s?\\w+\\s?(.+?)\\.')
    obj_x = re.compile(r'X\\s?\\w+\\s?(-?\\d+(?:\\.\\d+)?)\\.')
    obj_y = re.compile(r'Y\\s+\\w+\\s+(-?\\s*\\d+(?:\\.\\d+)?)\\.')
    obj_prior = re.compile(r'Priority\\s?\\w+\\s?(\\d+)\\.')
    return Objective(
        id=re.findall(obj_id, chunk)[0],
        description=re.findall(obj_desc, chunk)[0],
        location=(float(re.findall(obj_x, chunk)[0].replace(" ","")),
                  float(re.findall(obj_y, chunk)[0].replace(" ",""))),
        priority=int(re.findall(obj_prior, chunk)[0])
    )

def parse_event(chunk: str) -> BattleEvent:
    battle_time = re.compile(r'Time\\s?\\w+\\s?(\\d+\\.\\d+)\\.')
    battle_desc = re.compile(r'Desk\\s?\\w+\\s?(.+?)\\.')
    battle_units = re.compile(r'Units\\s?\\w+\\s?(.+?)\\.')
    battle_type = re.compile(r'Type\\s?\\w+\\s?(.+?)\\.')
    battle_x = re.compile(r'X\\s?\\w+\\s?(-?\\d+(?:\\.\\d+)?)\\.')
    battle_y = re.compile(r'Y\\s+\\w+\\s+(-?\\s*\\d+(?:\\.\\d+)?)\\.')
    return BattleEvent(
        timestamp=re.findall(battle_time, chunk)[0],
        description=re.findall(battle_desc, chunk)[0],
        involved_units=list(re.findall(battle_units, chunk)[0].split('|')),
        event_type=re.findall(battle_type, chunk)[0].lower(),
        location=(float(re.findall(battle_x, chunk)[0].replace(" ","")),
                  float(re.findall(battle_y, chunk)[0].replace(" ","")))
    )

def parse_scenario(text: str) -> Scenario:
    tokens = tokenize_by_keyword(text)
    title = tokens['Title'][0] if tokens['Title'] else "Untitled Scenario"
    description = tokens['Description'][0] if tokens['Description'] else ""
    units = [parse_unit(chunk) for chunk in tokens['Unit']]
    features = [parse_feature(chunk) for chunk in tokens['Feature']]
    objectives = [parse_objective(chunk) for chunk in tokens['Objective']]
    timeline = [parse_event(chunk) for chunk in tokens['Event']]

    terrain = Terrain(type="unknown", features=features, dimensions=(10, 10))

    return Scenario(
        title=title,
        description=description,
        terrain=terrain,
        units=units,
        objectives=objectives,
        timeline=timeline
    )
