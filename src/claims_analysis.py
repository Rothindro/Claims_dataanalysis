import streamlit as st
from PIL import Image
import pandas as pd
import io
import plotly.graph_objects as go
import plotly.express as px

with st.container():
    image = Image.open('images/Poster.png')
    st.image(image, use_column_width=True)
    image = Image.open('images/Problem_statement.png')
    st.image(image, use_column_width=True)
    st.write("**_To see the original dataset, please download the table from **Claims Data** section or [click here](https://1drv.ms/x/c/b5af2d6d1ff645f7/Ecy0_vUQvANJoxcOJzBIUXUBY9U7eZ97roxlk2E1GIrYcQ?e=ZCr63t)_*")
    st.write("**_To see the analyzed dataset, please download the table from **Final Sheet** section or [click here](https://1drv.ms/x/c/b5af2d6d1ff645f7/EV8JS0KxsIBKmFuN0VzMXdsBXC786KYcJz3v2jOsV2geFg?e=0Fsap9&nav=MTVfezhGQkMyQzZDLTRDODYtNDQ4Ny05OTJBLTI5NzcwODUyMTEyRH0)_*")
    st.write("*_For a comprehensive overview of the project, please refer to this client ready [ppt](https://1drv.ms/p/c/b5af2d6d1ff645f7/EcvDYZIM85dHqWGC-yqpB-gBdKcSUVWFcIThYWeVtcNEJA?e=vmlm8s) file_")
    st.write("######")
with st.container():
    o_file_path = "data/G & J_Medicine Claims Data Case Study.xlsx"
    xls = pd.ExcelFile(o_file_path, engine='openpyxl')
    sheet_names = xls.sheet_names
    st.subheader("Claims Data", divider='blue')
    st.write("######")
    sheet_name = st.selectbox("Select a sheet", sheet_names)
    df = pd.read_excel(o_file_path, sheet_name=sheet_name, engine='openpyxl')
    column1, column2=st.columns([2,1])
    with column1:
        st.write(df)
    with column2:
        shape=df.shape
        st.write("_Shape of DataFrame:_", shape)
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        st.write("_Info of DataFrame:_")
        st.text(info)
    st.divider()
    st.write("To answer the given problem statements, i have combined all the required data from other sheets into one and to ensure the data integrity and completeness of the data i have applied few dat checks mentioned below:")
    st.write("_Validity Checks_")
    st.write("_Consistency Checks_")
    st.write("_Duplication Checks_ and")
    st.write("_Referential Integrity_")
    st.write("######")
with st.container():
    f_file_path = "data/Source_file_G & J_Medicine_Claims_Data_Case_Study.xlsx"
    st.subheader("Final Sheet", divider='blue')
    st.write("######")
    df = pd.read_excel(f_file_path, engine='openpyxl')
    column1, column2 = st.columns([1,2])
    with column2:
        st.write(df)
    with column1:
        shape = df.shape
        st.write("_Shape of DataFrame:_", shape)
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        st.write("_Info of DataFrame:_")
        st.text(info)
    st.write("######")
    st.subheader("Patients Transition Rate, From Diagnosis to Treatment", divider='blue')
    st.write("Question: What % of patients move from diagnosis to treatment❓")
    st.write("######")
    column1, column2 = st.columns([1.5, 1.5])
    with column1:
        unique_count = df['Patient ID'].nunique()
        patients_distribution = df.pivot_table(index='Patient ID', columns='Diagnosis Code', aggfunc='size', fill_value=0).reset_index()
        patients_distribution.columns.name = None
        patients_distribution.columns = ['Patient ID', 'On_drug', 'L20', 'L209']
        st.write("Patients distribution summary")
        unique_count = patients_distribution[patients_distribution['On_drug'] != 0]['Patient ID'].nunique()
        unique_count1 = patients_distribution[patients_distribution['On_drug'] == 0]['Patient ID'].nunique()
        summary_df = pd.DataFrame({
            'Condition': [
                'Patients moved to treatment',
                'Patients on diagnosis',
            ],
            'Count': [
                unique_count,
                unique_count1,
            ]
        })
        st.write(summary_df)
        st.divider()
        st.write("➡️A total of 7,261 patients are there in the “Claims Data” sheet.")
        st.write("➡️About 2,754 patients are still on diagnosis and haven’t moved to treatment.")
        st.write("➡️About 4,507 patients were moved from diagnosis to treatment; therefore, 62.07% of patients moved from diagnosis to treatment.")
    with column2:
        percentage_on_drug = round((summary_df['Count'][0] / (summary_df['Count'][0] + summary_df['Count'][1])) * 100, 2)
        percentage_on_diagnosis = round((summary_df['Count'][1] / (summary_df['Count'][0] + summary_df['Count'][1])) * 100, 2)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Patients'],
            y=[percentage_on_drug],
            text=[f"{percentage_on_drug:.2f}% ({summary_df['Count'][0]})"],  # Text label for Patients on Drug
            textposition='inside',  # Display text inside the bar
            name='Patients on Treatment',
            marker_color='blue',
            width=0.5  # Adjusted width
        ))
        fig.add_trace(go.Bar(
            x=['Patients'],
            y=[percentage_on_diagnosis],
            text=[f"{percentage_on_diagnosis:.2f}% ({summary_df['Count'][1]})"],
            # Text label for Patients on Diagnosis
            textposition='inside',  # Display text inside the bar
            name='Patients on Diagnosis',
            marker_color='orange',
            width=0.5
        ))
        fig.update_layout(
            title='Distribution of patients',
            barmode='stack',
            xaxis=dict(),
            yaxis=dict(title='Percentage of Patients (%)', range=[0, 100], tickformat=".2f%%"),
            legend=dict(
                x=0.5,  # Center legend horizontally
                y=-0.2,  # Position legend at the bottom
                xanchor='center',  # Anchor legend to the center
                yanchor='top',  # Anchor legend to the top
                orientation='h'  # Horizontal orientation
))
        st.plotly_chart(fig)
    st.write("######")
    st.subheader("Duration of Diagnosis to Treatment Journey", divider='blue')
    st.write("Question: On average, how long (in days) do patients take to move from diagnosis to treatment❓ Create a graph to show patients started with the treatment within 45, 90, 180 and post 180 days.")
    st.write("######")
    column1, column2 = st.columns([1.5, 1.5])
    with column1:
        st.write("Filtered and Aggregated DataFrame with Days Interval Between Diagnosis and Treatment")
        d_file_path="data/Duration_of_Diagnosis_to_treatm.xlsx"
        d_df = pd.read_excel(d_file_path, engine='openpyxl')
        st.write(d_df)
    with column2:
        st.write("Duration of diagnosis to treatment")
        category_counts = d_df['Days_Category'].value_counts().sort_index().reset_index()
        category_counts.columns = ['Days_Category', 'No. of patients']
        st.write(category_counts)
        filtered_numbers = [num for num in d_df["Days_Between"] if num > 0]
        average = round((sum(filtered_numbers) / len(filtered_numbers) if filtered_numbers else 0),2)
        st.write(f"Average duration of diagnosis to treatment: {average}")
        fig = px.bar(category_counts, x='Days_Category', y='No. of patients',
                     title='Patients journey from diagnosis to treatment',
                     labels={'Days_Category': 'Days Category', 'No. of patients': 'No. of patients'},
                     color_discrete_sequence=['blue'],
                     text='No. of patients')
        fig.update_layout(
            xaxis_title='Days Category',
            yaxis=dict(title='No. of patients',
                            range=[0, 4000]),
            bargap=0.6,
            width=350,
            height=350,
            xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig)
    st.subheader("Insights into Payer Channel Claim Share Dynamics", divider='blue')
    st.write("Question: What is the claim share of the payer channel over the years❓ Provide insights and visualizations. Do you see any change in claim pattern across years❓")
    st.write("######")
    column1, column2=st.columns([1.5, 1.5])
    with column1:
        st.write("Payer Channel Claim Share")
        payer_channel_estimate=df['Payer Channel'].value_counts().sort_index().reset_index()
        payer_channel_estimate.columns = ['Payer Channel', 'Count of Plan ID']
        total_count = payer_channel_estimate['Count of Plan ID'].sum()
        payer_channel_estimate['Claim Share'] = round((payer_channel_estimate['Count of Plan ID'] / total_count) * 100, 2)
        payer_channel_estimate['Claim Share'] = payer_channel_estimate['Claim Share'].apply(lambda x: f'{x:.2f}%')
        payer_channel_estimate.loc[0, 'Payer Channel'] = 'Other'
        st.write(payer_channel_estimate)
        st.write("➡️There is no significant change observed in the claim pattern across years.")
        st.write("➡️If we look towards a specific category like “Claim share for patients in treatment” it was observed that for year 2017, there was only “COMMERCIAL” payer channels were operating.")
    with column2:
        fig = go.Figure(data=[go.Pie(
            labels=payer_channel_estimate['Payer Channel'],
            values=payer_channel_estimate['Count of Plan ID'],
            hoverinfo='label+percent+value',
            textinfo='label+percent',
            texttemplate='%{value} (%{percent})',
            insidetextorientation='horizontal',
            textposition='outside',
            hole=0)])
        fig.update_layout(
            title='Payer Channel Distribution')
        st.plotly_chart(fig)
    st.subheader("Dominant Payers in Commercial Claims Across Years", divider='blue')
    st.write("Question: Who are the top payers (Payer name) within the commercial channel over the years❓")
    st.write("######")
    column1, column2 = st.columns([1.5, 1.5])
    with column1:
        selected_payer_channel = st.selectbox('Select Payer Channel', df['Payer Channel'].unique())
        filtered_df = df[df['Payer Channel'] == selected_payer_channel]
        payer_channel_estimate = filtered_df['Payer name'].value_counts().sort_index().reset_index()
        payer_channel_estimate.columns = ['Payer name', 'No. of patients']
        payer_channel_estimate_sorted = payer_channel_estimate.sort_values(by='No. of patients', ascending=False)
        st.write(payer_channel_estimate_sorted)
    with column2:
        top_10 = payer_channel_estimate_sorted.head(10)
        fig = go.Figure(data=[go.Bar(
            x=top_10['Payer name'],
            y=top_10['No. of patients'],
            marker_color='blue'
        )])
        fig.update_layout(
            title=f'Top 10 Payer Names for Channel: {selected_payer_channel}',
            xaxis= dict(title='Payer Name'),
            yaxis= dict(title='No. of patients',
                        range=[0, 2000]),
            bargap=0.4,
            height=600)
        st.plotly_chart(fig)
    st.subheader("Key Payer Channels for Targeted Specialties", divider='blue')
    st.write("Question: Considering Dermatology and Nurse Practitioners specialty physicians as the major targets for ProcDNA, which payer channel becomes more important and why❓")
    st.write("######")
    column1, column2 = st.columns([1.4, 1.6])
    with column1:
        specialty = df.pivot_table(index='Specialty Code', columns='Payer Channel', aggfunc='size', fill_value=0).reset_index()
        specialty.columns.name = None
        specialty.columns = ['Specialty Code', 'Other', 'COMMERCIAL', 'MEDICAID', 'MEDICARE']
        specialty.loc[0, 'Specialty Code'] = 'Allergy & Immunology'
        specialty.loc[1, 'Specialty Code'] = 'Dermatology'
        specialty.loc[2, 'Specialty Code'] = 'Nurse Practitioner'
        specialty.loc[3, 'Specialty Code'] = 'Primary Care Physician'
        specialty.loc[4, 'Specialty Code'] = 'Pediatrics'
        specialty.loc[5, 'Specialty Code'] = 'Rheumatology'
        st.write(specialty)
    with column2:
        melted_specialty = pd.melt(specialty.iloc[1:3], id_vars=['Specialty Code'], value_vars=['Other', 'COMMERCIAL', 'MEDICAID', 'MEDICARE'], var_name='Subcategory', value_name='Value')
        fig = px.bar(melted_specialty, x='Specialty Code', y='Value', color='Subcategory', barmode='group',
                     title='Key Payer Channels in Targeted Specialities',
                     labels={'Specialty Code': 'Specialty', 'Value': 'No. of Claims'},
                     width=400,
                     height=300)
        fig.update_layout(
            xaxis_title='Specialty',
            yaxis= dict(title='No. of Claims', range=[0, 8500]),
            bargap=0.2,
            bargroupgap=0.1,
            xaxis_tickangle=45,
            height=400
        )
        st.plotly_chart(fig)
    st.write("➡️Considering Dermatology and Nurse Practitioners specialty physicians, “Commercial Channel” seems to be most important as the number of claims is significantly high, therefore commercial channels has the highest reach compared to others")
st.divider()
st.write("*_For a comprehensive overview of the project, please refer to this client ready [ppt](https://1drv.ms/p/c/b5af2d6d1ff645f7/EcvDYZIM85dHqWGC-yqpB-gBdKcSUVWFcIThYWeVtcNEJA?e=vmlm8s) file_")
