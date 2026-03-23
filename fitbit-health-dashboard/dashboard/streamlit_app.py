import os

import pandas as pd
import requests
import streamlit as st

API_BASE = os.getenv('API_BASE_URL', 'http://localhost:8000')

st.set_page_config(page_title='Fitbit Predictive Health', layout='wide')
st.title('Fitbit Predictive Health Dashboard')

st.markdown('Connect Fitbit in backend first, then use your Fitbit `user_id` here.')
user_id = st.text_input('Fitbit user_id')

col1, col2 = st.columns(2)
with col1:
    if st.button('Backfill 365 days') and user_id:
        r = requests.post(f'{API_BASE}/sync/backfill', params={'user_id': user_id, 'days': 365}, timeout=120)
        st.write(r.json())

with col2:
    if st.button('Refresh Summary') and user_id:
        r = requests.get(f'{API_BASE}/analytics/summary', params={'user_id': user_id}, timeout=30)
        st.session_state['summary'] = r.json()

summary = st.session_state.get('summary')
if summary:
    st.subheader('Summary')
    st.json(summary)

    df = pd.DataFrame(
        [
            {'Metric': 'Data points', 'Value': summary.get('data_points')},
            {'Metric': 'Avg Resting HR', 'Value': summary.get('avg_resting_heart_rate')},
            {'Metric': 'Elevated RHR Days (%)', 'Value': summary.get('elevated_rhr_days_pct')},
        ]
    )
    st.dataframe(df, use_container_width=True)

st.info('Next step: add time-of-day stress heatmap and office vs non-office segmentation from intraday HR data.')
