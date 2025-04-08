from pydantic import BaseModel
from typing import List, Optional

class Unit(BaseModel):
    id: str
    name: str
    type: str  # e.g. "infantry", "armor", "air support"
    strength: int  # combat effectiveness, 0–100
    position: Optional[tuple[float, float]] = None  # (x, y) coords
    allegiance: str  # "friendly" or "enemy"
    status: str = "active"  # e.g. "active", "retreating", "destroyed"

class TerrainFeature(BaseModel):
    type: str  # e.g. "hill", "forest", "building"
    position: tuple[float, float]
    size: float  # area/radius in meters

class Terrain(BaseModel):
    type: str  # e.g. "urban", "desert", "jungle"
    features: List[TerrainFeature]
    dimensions: tuple[int, int]  # map size in meters (width, height)

class Objective(BaseModel):
    id: str
    description: str
    controlling_unit_ids: List[str] = []
    completed: bool = False
    location: Optional[tuple[float, float]]
    priority: int = 1  # Higher number = more critical

class BattleEvent(BaseModel):
    timestamp: object  # e.g. "00:05", "12:03 PM"
    description: str
    involved_units: List[str] = []
    location: Optional[tuple[float, float]]
    event_type: str  # e.g. "move", "fire", "retreat", "reinforce"

class Scenario(BaseModel):
    title: str
    description: str
    terrain: Terrain
    units: List[Unit]
    objectives: List[Objective]
    timeline: List[BattleEvent]