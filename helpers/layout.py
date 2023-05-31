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
            pass
        with tab2:
            pass

