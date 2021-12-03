import streamlit as st
from main import start_comparison
import plotly.graph_objects as go
import json

st.title("RSA Vs RSA-CRT")

if 'curr_bit' not in st.session_state:
    st.session_state.curr_bit = None

if 'prev_bit' not in st.session_state:
    st.session_state.prev_bit = None

if 'prev_efficiency' not in st.session_state:
    st.session_state.prev_efficiency = None

if 'curr_efficiency' not in st.session_state:
    st.session_state.curr_efficiency = None

if 'graph_data' not in st.session_state:
    st.session_state.graph_data = None

if 'cal_values' not in st.session_state:
    st.session_state.cal_values = json.dumps({}, indent=4)

bit = st.select_slider('Select number of bits for values of p & q', options=[32, 64, 128, 256, 512, 1024, 2048, 4096], value=32)
app_slowness_placeholder = st.empty()

if bit >=2048:
    app_slowness_placeholder.warning('This application will get slow as value for bits is very high')
else:
    app_slowness_placeholder.empty()

def calculate_efficiency_value(t1, t2):

    if t2 > t1:
        val = -1 * t2/t1
    else:
        val = t1/t2
    
    val = "{:.2f}".format(val)
    return val

def insert_graph_values(eff, t1, t2):

    if st.session_state.graph_data == None:
       st.session_state.graph_data = {
           'x' : [],
           't1' : [],
           't2' : []
       }

    st.session_state.graph_data['x'].append(eff)
    st.session_state.graph_data['t1'].append(t1)
    st.session_state.graph_data['t2'].append(t2)

if st.button('Start Comparison'):
    with st.spinner("Please wait while calculations are completed..."):
        t1, t2, cal_values = start_comparison(bit)
        st.session_state.prev_efficiency = st.session_state.curr_efficiency
        st.session_state.curr_efficiency = calculate_efficiency_value(t1, t2)
        t1 = "{:f}".format(t1)
        t2 = "{:f}".format(t2)
        insert_graph_values(bit, float(t1), float(t2))
        st.session_state.prev_bit = st.session_state.curr_bit
        st.session_state.curr_bit = bit
        st.session_state.cal_values = cal_values
    st.subheader("RSA: {}".format(t1))
    st.subheader("RSA-CRT: {}".format(t2))

metrics_placeholder = st.empty()

if st.session_state.curr_bit == None:
    metrics_placeholder.empty()
else:
    col1, col2, col3, col4 = st.columns(4)
    if st.session_state.prev_bit == None:
        col1.metric("Previous Bit", "---")
    else:
        col1.metric("Previous Bit", st.session_state.prev_bit)
    col2.metric("Current Bit", st.session_state.curr_bit)
    if st.session_state.curr_bit == None:
        col3.metric("Please run 'Start Comparison'", "")
    else:
        col3.metric("Efficiency", st.session_state.curr_efficiency, "")
    if st.session_state.prev_efficiency == None:
        col4.metric("Previous Efficiency", "---")
    else:
        col4.metric("Previous Efficiency", st.session_state.prev_efficiency)
        
graph_placeholder = st.empty()

if st.session_state.graph_data == None:
    graph_placeholder.empty()
else:
    fig = go.Figure(data=[
        go.Bar(name='RSA', x=st.session_state.graph_data['x'], y=st.session_state.graph_data['t1']),
        go.Bar(name='RSA-CRT', x=st.session_state.graph_data['x'], y=st.session_state.graph_data['t2'])
    ])

    fig.update_layout(barmode='group')
    # fig.show()
    st.plotly_chart(fig)

button_placeholder = st.empty()

if st.session_state.graph_data == None:
    button_placeholder.empty()
else:
    if button_placeholder.button('Reset Graph'):
        st.session_state.graph_data = None

show_values_placeholder = st.empty()

if st.checkbox("Show Values"):
    st.json(st.session_state.cal_values)
else:
    show_values_placeholder.empty()