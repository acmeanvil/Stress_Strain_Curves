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
    x_max=max(_x_range)
    x_min=min(_x_range)
    y_max=max(_y_range)
    y_min=min(_y_range)
    
    fig_ss_main = go.Figure()
    fig_ss_main.add_trace(
        go.Scatter(
        name="Stress Vs Strain",
        x=_x_range,
        y=_y_range,
        line_width=2,
        line_color="gray",
        legendrank=1)
    )
    #legend=dict( yanchor="top", y=1, xanchor="left", x=0.01)
    fig_ss_main.update_layout(showlegend=True, margin=dict(l=5, r=5, t=5, b=5), width=500, height=600)
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

def fig_add_trace(_fig: go.Figure, _trace_name: str, _x_range: list(float), _y_range: list(float), _color='blue'):
    _fig.add_trace(
            go.Scatter(
            name=_trace_name,
            x=_x_range,
            y=_y_range,
            line_width=1,
            line_color=_color)
    )

def get_trace_points(_slope: float, _incpt: float, _x_max: float, _y_max: float)->dict(dict):
    
    x_tmp=((_y_max-_incpt)/_slope)
    y_tmp=(_slope*_x_max)+_incpt
    if y_tmp<= _y_max:
        x=[0,_x_max]
        y=[_incpt,y_tmp]
    else: 
        x=[0,x_tmp]
        y=[_incpt,_y_max]
    line_dict={'x':x, 'y':y}
    return line_dict
    