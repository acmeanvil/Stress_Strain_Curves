"""
Copyright 2023 Acmeanvil

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.

A stress strain curve exploration tool
"""

from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go

def draw_main_figure(_x_range: list(float), _y_range: list(float), _x_bracket: tuple, _y_bracket: tuple):
    """ 
    
    """
    fig_ss_main = go.Figure()
    fig_ss_main.add_trace(
        go.Scatter(
        name="Stress Vs Strain",
        x=_x_range,
        y=_y_range,
        line_width=4,
        line_color="gray",
        legendrank=1)
    )
    fig_ss_main.update_layout(legend=dict( yanchor="top", y=0.90, xanchor="left", x=0.01), margin=dict(l=5, r=5, t=5, b=5))
    if _x_bracket:
        fig_ss_main.add_trace(
            go.Scatter(
            name="X-Min",
            x=[_x_bracket[0], _x_bracket[0]],
            y=[min(_y_range),max(_y_range)],
            line_width=1,
            line_color="red")
        )
        fig_ss_main.add_trace(
            go.Scatter(
            name="X-Max",
            x=[_x_bracket[1], _x_bracket[1]],
            y=[min(_y_range),max(_y_range)],
            line_width=1,
            line_color="red")
        )
    if _y_bracket:
        fig_ss_main.add_trace(
            go.Scatter(
            name="Y-Min",
            x=[min(_x_range),max(_x_range)],
            y=[_y_bracket[0], _y_bracket[0]],
            line_width=1,
            line_color="blue")
        )
        fig_ss_main.add_trace(
            go.Scatter(
            name="Y-Max",
            x=[min(_x_range),max(_x_range)],
            y=[_y_bracket[1], _y_bracket[1]],
            line_width=1,
            line_color="blue")
        )
    return fig_ss_main