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
import helpers.figure_helpers as fh

def display_range_component(_x_range: list(float), _y_range: list(float))->go.Figure:
    range_dict={'x_range':(),'y_range':(), 'slice_range':()}
    container_1=st.container()
    with container_1:
        col1, col2 = st.columns(2)
        with col1:
            x_range=range_slider_with_checkbox("X Range Bracket", 'X range', _x_range)
            range_dict.update({'x_range':x_range}) 
        with col2:
            y_range=range_slider_with_checkbox("Y Range Bracket", 'Y range', _y_range)
            range_dict.update({'y_range':y_range})  
    container_2=st.container()
    with container_2:
        slice_range=single_slider("Select Data", 0.0, 100.0, (0.0,100.0))
        range_dict.update({'slice_range':slice_range})
    return range_dict

def single_slider(_label: str, _min: float, _max: float, _start_value)->float:
    """
    Can display a single slider, or a single range slider
    returns the current slider value or a range min/max tuple
    """
    return st.slider(label=_label, min_value=_min, max_value=_max, value=_start_value, step=0.001)

def percentage_slider(_label: str, _start_value)->float:
    """
    Displays a single slider with values from 0-100, returns a percent value
    """
    return st.slider(label=_label, min_value=0.0, max_value=100.0, value=_start_value)

def range_slider_with_checkbox(_chk_label: str, _sldr_label: str, _range: list(float))->tuple:
    """
    Display a range slider that can be enabled and disabled via checkbox
    """
    checked=st.checkbox(_chk_label)
    range_dict={_sldr_label:""}
    if checked:
        range=st.slider(_sldr_label,
            value=[0.0001,
            max(_range)],
            min_value=0.001,
            max_value=max(_range),
            step=0.001)
        return range 