# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)

numeric_cols = ['TD Thrown', 'TD Caught', 'Sacks', 'Safety', 'Interception']

@st.cache_data
def load_data():
    df = pd.read_csv('data/primetime_stats.csv')
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Convert numeric columns to integers
    df[numeric_cols] = df[numeric_cols].astype(int)
    return df


def run():
    st.set_page_config(
        page_title="Prime Time Sports League Flag Football Stats",
        page_icon="🏈",
    )

    data = load_data()

    player_search = st.text_input('Search for a player')
    summary = data.groupby('Team Player')[numeric_cols].sum().reset_index()

    if not player_search:
      st.table(summary)
    else:
      filtered_df = data[data['Team Player'].str.contains(player_search, case=False, na=False)].reset_index()
      
      st.subheader('Career stats')
      st.write('Career totals')
      sums = filtered_df[['TD Thrown', 'TD Caught', 'Sacks', 'Safety', 'Interception']].sum()
      st.table(sums)

      st.write('Season averages')
      means = filtered_df[['TD Thrown', 'TD Caught', 'Sacks', 'Safety', 'Interception']].mean()
      st.table(means)

      st.subheader('Season stats')
      st.table(filtered_df)




if __name__ == "__main__":
    run()
