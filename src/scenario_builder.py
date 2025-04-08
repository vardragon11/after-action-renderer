# pages/scenario_builder.py

import streamlit as st
import json
import re
import subprocess

from Scenario2d import ScenarioScene
from Scenario3D import SpaceScenario3DScene
from pydantic import BaseModel
from collections import defaultdict
from typing import List, Optional

from scenario_utils import (
    Scenario,
    parse_scenario
)
# --- Page UI ---
st.title("🛰️ Scenario Builder")

text_input = st.text_area("Enter scenario script:", height=300)

if st.button("🧠 Parse to JSON"):
    if text_input.strip():
        parsed = parse_scenario(text_input)
        st.success("Scenario parsed successfully!")
        st.json(parsed)
        with open("scenario.json", "w") as f:
            json.dump(parsed.dict(), f, indent=2)
        st.write("✅ Saved to `scenario.json`")
    else:
        st.warning("Please enter some scenario text.")

scene_type = st.selectbox("Choose scene type", ["2D Ground Scenario", "3D Space Scenario"])
if scene_type == "2D Ground Scenario":
    manim_class = "ScenarioScene"
    manim_file = "Scenario2d.py"
else:
    manim_class = "SpaceScenario3DScene"
    manim_file = "Scenario3D.py"

if st.button("🎬 Run Manim Animation"):
    result = subprocess.run(
        ["manim", "-pql", manim_file, manim_class],
        capture_output=True, text=True
    )
    st.text_area("📋 Manim Output Log", value=result.stdout + result.stderr, height=300)

    # Display rendered video
    video_path = f"media/videos/{manim_file.replace('.py','')}/480p15/{manim_class}.mp4"
    try:
        st.video(video_path)
        st.success("🎥 Playback complete.")
    except Exception as e:
        st.error(f"Could not load video: {e}")
