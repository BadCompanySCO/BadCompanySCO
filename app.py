import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
from streamlit_option_menu import option_menu

def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title="Race Data",
                   page_icon=":bar_chart:",
                   layout="wide"

)


st.title('Race Data Analysis 📈')
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
   # st.dataframe(df)
  
st.sidebar.header("Please Filter Here:")
event = st.sidebar.multiselect(
    "Select the Event:",
    options=df["Event"].unique(),
    default=df["Event"].unique()
)

st.sidebar.header("Please Filter Here:")
distance = st.sidebar.multiselect(
    "Select the Distance:",
    options=df["Race_Distance"].unique(),
    default=df["Race_Distance"].unique()
)

df_selection = df.query(
    "Event == @event & Race_Distance == @distance"
)

st.dataframe(df_selection)

st.markdown("---")

total_runners = int(df_selection["ID"].count())
filt_male = str(df_selection["Gender"].value_counts()['Male'])
filt_female = str(df_selection["Gender"].value_counts()['Female'])



left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Number of runners:")
    st.subheader(f"{total_runners}")

with middle_column:
    st.subheader("Total Number of Male:")
    st.subheader(f"{filt_male}")
    
with middle_column:
    st.subheader("Total number of Female:")
    st.subheader(f"{filt_female}")
    
st.markdown("---")

st.subheader("Top 5 runner:")
df_selection.set_index('Position', inplace=True)
df_grouped = df_selection.iloc[0:5,]
df_selection.reset_index()

df_grouped[['Number', 'First_Name', 'Surname', 'Gender', 'Category', 'Run_Time']]

st.markdown("---")

#-- DOWNLOAD SECTION
st.subheader('Downloads:')
generate_excel_download_link(df_grouped)
#generate_html_download_link(fig)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)