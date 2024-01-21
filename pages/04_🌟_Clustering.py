import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import sys
from pathlib import Path

# Get the parent directory
parent_dir = str(Path(__file__).parent.parent)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from spotify import df, download_df, artList, albList, overallGraph
st.title(":smile_cat: Clutering (Coming Soon)")