import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Streamlit App Title
st.title("Interactive Data Analysis Tool")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load the Dataset
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    st.sidebar.header("Data Analysis Options")

    st.subheader("Dataset Preview")
    st.write(data.head())



    # Show the Data Types
    if st.sidebar.checkbox("Show shape of the Dataset"):
        st.subheader("Check the shape of the data:")
        st.write(data.shape)  
        st.write(f"No of rows: {data.shape[0]}")
        st.write(f"No of columns: {data.shape[1]}")



    # Show Dataset Description
    if st.sidebar.checkbox("Show Dataset Description"):
        st.subheader("Dataset Description")
        st.write(data.describe())



    
    # Show the Data Types
    if st.sidebar.checkbox("Show Data types"):
        st.subheader("Check the data type:")
        st.write(data.dtypes)    

    # Show the Null values
    if st.sidebar.checkbox("Show Null Value"):
        # Check for missing values
        missing_summary = data.isnull().sum()
        missing_cols = missing_summary[missing_summary > 0]
        
        if not missing_cols.empty:
            st.write("### Missing Value Summary")
            st.write(missing_cols)
            
            # Select column to handle missing values
            column = st.selectbox("Select column to handle missing values", missing_cols.index)
            method = st.radio("Choose a method to fill missing values", ["Mean", "Median", "Mode"])
            
            if st.button("Replace Missing Values"):
                if method == "Mean":
                    data[column].fillna(data[column].mean(), inplace=True)
                elif method == "Median":
                    data[column].fillna(data[column].median(), inplace=True)
                elif method == "Mode":
                    data[column].fillna(data[column].mode()[0], inplace=True)
                
                st.success(f"Missing values in '{column}' replaced using {method}.")
                st.write("### Updated Data Preview")
                st.dataframe(data)
                st.write(f"Missing Value: {data[column].isnull().sum()}")
                
        else:
            st.write("✅ No missing values found in the dataset.")



    





             

    # Display Column Selection
    st.sidebar.subheader("Column Selection for Analysis")
    selected_columns = st.sidebar.multiselect("Select columns", options=data.columns)

    if selected_columns:
        st.subheader("Selected Columns Preview")
        st.write(data[selected_columns].head())

        # Correlation Heatmap
        if st.sidebar.checkbox("Show Correlation Heatmap"):
            st.subheader("Correlation Heatmap")
            plt.figure(figsize=(10, 6))
            sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm")
            st.pyplot(plt)

        # Pairplot
        if st.sidebar.checkbox("Show Pairplot"):
            st.subheader("Pairplot of Selected Columns")
            st.write("Generating pairplot, please wait...")
            sns.pairplot(data[selected_columns], diag_kind="kde")
            st.pyplot()

        # Line Plot
        if st.sidebar.checkbox("Show Line Plot"):
            st.subheader("Line Plot")
            x_axis = st.selectbox("X-axis column", options=selected_columns, key="line_x")
            y_axis = st.selectbox("Y-axis column", options=selected_columns, key="line_y")

            if x_axis and y_axis:
                plt.figure(figsize=(10, 6))
                sns.lineplot(data=data, x=x_axis, y=y_axis)
                st.pyplot(plt)

        # Bar Plot
        if st.sidebar.checkbox("Show Bar Plot"):
            st.subheader("Bar Plot")
            category_col = st.selectbox("Category column", options=selected_columns, key="bar_cat")
            value_col = st.selectbox("Value column", options=selected_columns, key="bar_val")

            if category_col and value_col:
                plt.figure(figsize=(10, 6))
                sns.barplot(data=data, x=category_col, y=value_col)
                st.pyplot(plt)

        # Histogram
        if st.sidebar.checkbox("Show Histogram"):
            st.subheader("Histogram")
            hist_col = st.selectbox("Column for Histogram", options=selected_columns, key="hist")

            if hist_col:
                plt.figure(figsize=(10, 6))
                sns.histplot(data[hist_col], kde=True)
                st.pyplot(plt)

        # Box Plot
        if st.sidebar.checkbox("Show Box Plot"):
            st.subheader("Box Plot")
            x_box = st.selectbox("X-axis column", options=selected_columns, key="box_x")
            y_box = st.selectbox("Y-axis column", options=selected_columns, key="box_y")

            if x_box and y_box:
                plt.figure(figsize=(10, 6))
                sns.boxplot(data=data, x=x_box, y=y_box)
                st.pyplot(plt)


        # Scatter plot (Added)
        if st.sidebar.checkbox("Show Scatter Plot"):
            st.subheader("Scatter Plot")
            x_scatter = st.selectbox("X-axis column", options=selected_columns, key="scatter_x")
            y_scatter = st.selectbox("Y-axis column", options=selected_columns, key="scatter_y")

            if x_scatter and y_scatter:
                plt.figure(figsize=(10, 6))
                sns.scatterplot(data=data, x=x_scatter, y=y_scatter)
                st.pyplot(plt)


       

    else:
        st.warning("Please select at least one column for analysis.")
else:
    st.info("Awaiting file upload. Please upload a dataset to begin.")