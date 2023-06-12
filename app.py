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
import scipy
from scipy import signal as sig
import helpers.figure_helpers as fh
import helpers.dataframe_helpers as dh
import numpy as np
import io



#stl.display_sidebar()
with st.sidebar:
    tab1, tab2, tab3 = st.tabs(['File','Traces', 'Tools'])
    with tab1:
        st.header('Upload file or Use Sample') 
        try: 
            upload=st.file_uploader("Choose data file to upload", type='csv')
            
            try:
                df=pd.read_csv(upload, index_col=0)  #, index_col=0
            except ValueError:
                df=pd.read_csv('Cable_1_test_8.csv')
            
            stress_raw=df['Stress'].tolist()
            stress_raw_max=max(stress_raw)
            stress_raw_min=min(stress_raw)
            
            stress_average=df['Stress_avg'].tolist()
            stress_average_max=max(stress_average)
            stress_average_min=min(stress_average)
            
            strain_raw= df['Strain_Raw'].tolist()
            strain_raws_max=max(strain_raw)
            strain_raws_min=min(strain_raw)
            
            strain_norm=df['Strain_Norm'].tolist()
            strain_norm_max=max(strain_norm)
            strain_norm_min=min(strain_norm)
        except ValueError:
            pass
    
    with tab2:
        container_t21=st.container()
        with container_t21:
            #stress_display=st.selectbox('Curve Data', ('Raw Stress','Filtered Stress', 'Average Stress'))
            #if stress_display=='Filtered Stress':
            st.header('Plot Filtered Data')
        
        container_t22=st.container()
        with container_t22:
            col1, col2 = st.columns(2)
            with col1:
                smoothing_window=st.number_input('Smoothing Length', min_value=5, value=5, step=2)
            with col2:
                smoothing_order=st.number_input('Smoothing Order', min_value=2, value=2, step=1)
        
        container_t23=st.container()
        with container_t23:            
            filter_mode=st.selectbox('Filter Mode',('mirror', 'constant', 'nearest', 'wrap', 'interp'))
        try:
            df.insert(4,'Stress_Filtered', sig.savgol_filter(df['Stress'], smoothing_window, smoothing_order, mode=filter_mode))
        except NameError:
            pass
        container_t24=st.container()
        with container_t24:
            st.header('Add Curves to Compare') 
            disp_raw=st.checkbox('Plot Raw Stress Data')
            disp_avg=st.checkbox('Plot Avg Stress Data') 
        
        container_t25=st.container()
        with container_t25:  
            st.header('Add Guidelines') 
            curve_count=st.number_input("Guideline Number (6x max)", min_value=0, max_value=6) 
            container_t26=st.container()
            
            with container_t26:
                if curve_count>=1:
                    colt2_1, colt2_2 = st.columns(2)
                    count=np.arange(0,curve_count, 1)
                    slope_keys=[]
                    incpt_keys=[]
                    for i in count:
                        with colt2_1:
                            st.number_input('Slope', key=f'slope_key{i}')
                            slope_keys.append(f'slope_key{i}')
                        with colt2_2:
                            st.number_input('Intercept', key=f'incpt_key{i}') 
                            incpt_keys.append(f'incpt_key{i}')
        
        container_t26=st.container()
        with container_t26:
            st.header('Add Secant Modulus')
            colt26_1, colt26_2=st.columns(2)
            with colt26_1:
                secant_max_x=st.number_input("X Max",value=0.0,format='%.4f', key="secant_x", step=0.001)
            with colt26_2:
                secant_max_y=st.number_input("Y Max",value=0.0,format='%.4f', key="secant_y")
            try:
                secant_slope=secant_max_y/secant_max_x
                st.info(f'Sec Mod.: {round(secant_slope, 2)}')
            except ZeroDivisionError:
                pass

    
    with tab3:
        st.header('Add Curve Offset')
        try:
            x_offset=st.number_input('X Offset', format='%.4f', value=0.0, min_value=-strain_norm_max, max_value=strain_norm_max, step=0.001) 
            y_offset=st.number_input('Y Offset', format='%.4f', value=0.0)   
        except:                   
            pass


tab0_1, tab0_2, tab0_3 = st.tabs(['Main', 'Data', 'Template'])
with tab0_1:
    container_1=st.container()
    with container_1:
        range_dict=stl.display_range_component(strain_norm, stress_raw)
        # st.info(f"X Range={range_dict['x_range']}")
        # st.info(f"Y Range={range_dict['y_range']}")

    slice_low=range_dict['slice_range'][0]
    slice_high=range_dict['slice_range'][1]

    idx_count=len(df.index)
    idx_low=round(idx_count*(slice_low/100.0))
    idx_high=round(idx_count*(slice_high/100.0))

    df_sub=df.iloc[idx_low:idx_high]

    strain_range=[x+x_offset for x in list(df_sub['Strain_Norm'])]
    stress_range=[y+y_offset for y in list(df_sub['Stress'])]
    stress_avg_range=[y+y_offset for y in list(df_sub['Stress_avg'])]
    stress_filter_range=[y+y_offset for y in list(df_sub['Stress_Filtered'])]

    try: 
        if range_dict['x_range'][0]>0 and range_dict['y_range']==None:
            data_slice_low=range_dict['x_range'][0]
            data_slice_high=range_dict['x_range'][1]
            df_slice=dh.bracket_value(df_sub,"Strain_Norm", data_slice_low, data_slice_high)
        elif range_dict['y_range'][0]>0 and range_dict['x_range']==None:
            data_slice_low=range_dict['y_range'][0]
            data_slice_high=range_dict['y_range'][1]
            df_slice=dh.bracket_value(df_sub,"Strain_Norm", data_slice_low, data_slice_high)
        elif range_dict['y_range'][0]>0 and range_dict['x_range'][0]>0:
            data_slice_low=range_dict['x_range'][0]
            data_slice_high=range_dict['x_range'][1]
            df_slice=dh.bracket_value(df_sub,"Strain_Norm", data_slice_low, data_slice_high)
        else:
            df_slice=df_sub
    except TypeError:
        df_slice=df_sub

    container_3=st.container()
    with container_3:
        fig_ss_main=fh.draw_main_figure(strain_range, stress_filter_range, range_dict['x_range'], range_dict['y_range'])
        if disp_raw:
            fh.fig_add_trace(fig_ss_main, "Raw Stress", strain_range, stress_range)
        if disp_avg:
            fh.fig_add_trace(fig_ss_main, "Avg Stress", strain_range, stress_avg_range, _color='green')
        try:
            for idx, slope in enumerate(slope_keys):
                try: 
                    if st.session_state[slope]:
                        #st.info(st.session_state[slope])
                        in_slope=st.session_state[slope]
                        in_incpt=st.session_state[incpt_keys[idx]]
                        trace_dict=fh.get_trace_points(in_slope, in_incpt, max(strain_range), max(stress_filter_range))
                        fh.fig_add_trace(fig_ss_main, f'Guide {idx+1}', trace_dict['x'], trace_dict['y'])
                        pass
                except KeyError:
                    pass
        except NameError:
            pass
        try: 
            try:
                secant_slope=st.session_state['secant_y']/st.session_state['secant_x']
                sect_trace_dict=fh.get_trace_points(secant_slope, 0, secant_max_y, secant_max_y)
                fh.fig_add_trace(fig_ss_main, 'Secant', sect_trace_dict['x'], sect_trace_dict['y'])
            except ZeroDivisionError:
                pass
        except KeyError:
            pass
        st.plotly_chart(fig_ss_main, use_container_width=True)  
    
    container_4=st.container()
    with container_4:
        st.markdown("<h5 style='text-align: center; color: gray;'>Slope and Intercept</h5>", unsafe_allow_html=True)
        col4_1, col4_2 = st.columns(2)
        with col4_1:
            x_list=[x+x_offset for x in list(df_slice['Strain_Norm'])]
            y_list=[y+y_offset for y in list(df_slice['Stress_Filtered'])]
            slope_incpt=dh.get_np_slope_and_intercept(_x=x_list, _y=y_list, _degree=1)
            slope_button=st.button('Slope', key='slope_button', use_container_width=True) 
            if slope_button:
                try:
                    st.info(round(slope_incpt[1], 2))
                except NameError:
                    st.info(0)

        with col4_2:
            incpt_button=st.button('Intercept', key='incpt_button', use_container_width=True) 
            if incpt_button:
                try:
                    st.info(round(slope_incpt[0], 2))
                except NameError:
                    st.info(0)

        st.markdown("<h5 style='text-align: center; color: gray;'>X Max and Min</h5>", unsafe_allow_html=True)
        col4_3, col4_4 = st.columns(2)  
        with col4_3:
            x_min_df=(df_slice['Strain_Norm'].min())+x_offset
            x_min_df_button=st.button('Min', key='x_min_df_button', use_container_width=True) 
            if x_min_df_button:
                try:
                    st.info(round(x_min_df, 4))
                except NameError:
                    st.info(0)
        with col4_4:
            x_max_df=(df_slice['Strain_Norm'].max())+x_offset
            x_max_df_button=st.button('Max', key='x_max_df_button', use_container_width=True) 
            if x_max_df_button:
                try:
                    st.info(round(x_max_df, 4))
                except NameError:
                    st.info(0)
        
        st.markdown("<h5 style='text-align: center; color: gray;'>Y Max and Min</h5>", unsafe_allow_html=True)
        col4_3, col4_4 = st.columns(2)  
        with col4_3:
            y_min_df=(df_slice['Stress_Filtered'].min())+y_offset
            y_min_df_button=st.button('Min', key='y_min_df_button', use_container_width=True) 
            if y_min_df_button:
                try:
                    st.info(round(y_min_df, 2))
                except NameError:
                    st.info(0)
        with col4_4:
            y_max_df=(df_slice['Stress_Filtered'].max())+y_offset
            y_max_df_button=st.button('Max', key='y_max_df_button', use_container_width=True) 
            if y_max_df_button:
                try:
                    st.info(round(y_max_df,2))
                except NameError:
                    st.info(0)
#-------------
with tab0_2:
    container2_1 = st.container()
    with container2_1:
        col1, col2, col3 = st.columns(3)
        with col1:
            df_info_chkbox=st.checkbox('DF Info')
        with col2:
            df_select=st.selectbox('', ['All Data', 'Data Sub Slice','Range Slice'], label_visibility='collapsed')
            if df_select=='All Data':
                df_out=df
            elif df_select=='Data Sub Slice':
                df_out=df_sub
            elif df_select=='Range Slice':
                df_out=df_slice
        # with col2:
        #     get_df_info=st.button('Dataframe Info', use_container_width=True)
        with col3:
            csv_out=df_out.to_csv().encode('utf-8')
            st.download_button("Export Data", data=csv_out, file_name='dataframe_output.csv', mime='text/csv', use_container_width=True)    
    container2_2=st.container()
    with container2_2:    
        st.dataframe(df_out, use_container_width=True)
    container2_3=st.container()
    with container2_3:
        if df_info_chkbox==True:
            buf=io.StringIO()
            df_out.info(buf=buf, verbose=True)
            info=buf.getvalue()
            st.text(info)   

with tab0_3:
    st.markdown("<h5 style='text-align: center; color: gray;'>Data Import Format Template</h5>", unsafe_allow_html=True)
    container3_2 = st.container()

    with container3_2:
        col3_1, col3_2, col3_3 = st.columns(3)
        df_org=pd.read_csv('Stress_Strain_Template.csv')
        template_out=df_org.to_csv().encode('utf-8')
        with col3_2:
            st.download_button("Download Data Template", data=csv_out, file_name='Stress_Strain_Template.csv', mime='text/csv', use_container_width=True)    
            
    container3_2 = st.container()
    with container3_2:

        st.dataframe(df_org, use_container_width=True)
