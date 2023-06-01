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

def display_main_graph_component(_x_range: list(float), _y_range: list(float))->go.Figure:
    range_dict={'x_range':(),'y_range':()}
    container_1=st.container()
    with container_1:
        col1, col2 = st.columns(2)
        with col1:
            x_brack=st.checkbox('X Range Bracket')
            x_range=()
            if x_brack:
                x_range=st.slider('x range',
                    value=[min(_x_range)+2,
                    max(_x_range)-2],
                    min_value=min(_x_range),
                    max_value=max(_x_range))
                range_dict.update({'x_range':x_range})
        with col2:
            y_brack=st.checkbox('Y Range Bracket')
            y_range=()
            if y_brack:
                y_range=st.slider('y range',
                    value=[min(_y_range)+2,
                    max(_y_range)-2],
                    min_value=min(_y_range),
                    max_value=max(_y_range))
                range_dict.update({'y_range':y_range})   
    container_2=st.container()
    with container_2:
                fig_ss_main=fh.draw_main_figure(_x_range, _y_range, x_range, y_range)
                st.plotly_chart(fig_ss_main, use_container_width=True)
    return range_dict

def display_sidebar():
    with st.sidebar:
        tab1, tab2 = st.tabs(['File','Traces'])
        with tab1:
            upload=st.file_uploader("Choose data file to upload")
        with tab2:
            pass

def single_slider(_label: str, _min: float, _max: float, _start_value)->float:
    """
    Display a single slider, returns the current slider value
    """
    return st.slider(label=_label, min_value=_min, max_value=_max, value=_start_value)

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
            value=[min(_range)+2,
            max(_range)-2],
            min_value=min(_range),
            max_value=max(_range))
        return range_dict.update({_sldr_label:range}) 