"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

A stress strain curve exploration tool
"""
from __future__ import annotations
import streamlit as st
import helpers.layout as stl
# import layout.figures as fgs
import plotly.graph_objects as go
import pandas as pd

fig_ss_x_range=[1,2,3,4,5,6,7,8]
fig_ss_y_range=[8,7,6,5,4,3,2,1]


stl.display_sidebar()
    
container_1=st.container()
with container_1:
    range_dict=stl.display_main_graph_component(fig_ss_x_range, fig_ss_y_range)
    st.info(f"X Range={range_dict['x_range']}")
    st.info(f"Y Range={range_dict['y_range']}")

        
        
        
