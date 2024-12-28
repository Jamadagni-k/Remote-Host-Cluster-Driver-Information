import streamlit as st
import subprocess
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bios_Info import Bios_Version_Fetch
import csv

st.set_page_config(layout="wide")
df =pd.DataFrame()
st.markdown("<h1 style='text-align: center;'>CVE Inventory and Data Dashboard</h1>", unsafe_allow_html=True)


def plot_pie_chart(data, column, container):
    data_counts = data[column].value_counts()
    fig, ax = plt.subplots(figsize=(20,18))
    ax.pie(data_counts, labels=data_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    container.pyplot(fig)

def plot_bar_chart(data, column, value, container):
    fig, ax = plt.subplots(figsize=(20,18))
    ax.bar(data[column], data[value])
    ax.set_xlabel(column)
    ax.set_ylabel(value)
    ax.set_title(f"Bar Chart of {column} vs {value}")
    container.pyplot(fig)

def download_outputs(output_folder):
# This function handles the downloading of outputs
    if os.path.exists(output_folder):
        output_files = os.listdir(output_folder)
        for output_file in output_files:
            download_path = os.path.join(output_folder, output_file)
            with open(download_path, 'rb') as file:
                file_content = file.read()
                st.download_button(label=f"Download {output_file}", data=file_content, file_name=output_file, mime='text/plain')
    else:
        st.write("No output files found.")

def Inventory_Management():
    srv_data = pd.read_excel("Dell_SRV_Machines.xlsx").fillna("N/A")
    sr_data = pd.read_excel("Dell_SR_Machines.xlsx").fillna("N/A")
    rhoads_data = pd.read_excel("Rhoads-PieChart.xlsx").fillna("N/A")
    project_select = st.sidebar.selectbox("Select Project",["StevieRayV","StevieRay","Rhoads","SpringsteenV","Springsteen"])
    oem_select = st.sidebar.selectbox("Select OEM",["Dell","HP","Asus","Acer","Fujitsu","Lenovo","STDOEM"])
    project_dataframes = {
            "StevieRayV": {
                           "Dell": pd.read_excel("Dell_SRV_Machines.xlsx").fillna("N/A"),
                            #"HP": pd.read_excel("").fillna("N/A"),
                            #"Asus": pd.read_excel("").fillna("N/A"),
                            #"Acer": pd.read_excel("").fillna("N/A"),
                            #"Fujitsu": pd.read_excel("").fillna("N/A"),
                            #"Lenovo": pd.read_excel("").fillna("N/A"),
                            #"STDOEM": pd.read_excel("").fillna("N/A"),
                        },  
            "StevieRay": {
                            "Dell": pd.read_excel("Dell_SR_Machines.xlsx").fillna("N/A"),
                            #"HP": pd.read_excel("").fillna("N/A"),
                            #"Asus": pd.read_excel("").fillna("N/A"),
                            #"Acer": pd.read_excel("").fillna("N/A"),
                            #"Fujitsu": pd.read_excel("").fillna("N/A"),
                            #"Lenovo": pd.read_excel("").fillna("N/A"),
                            #"STDOEM": pd.read_excel("").fillna("N/A"),
                        },
            "Rhoads":   {
                            "STDOEM": pd.read_excel("Rhoads-PieChart.xlsx").fillna("N/A"),
                            #"HP": pd.read_excel("").fillna("N/A"),
                            #"Asus": pd.read_excel("").fillna("N/A"),
                            #"Acer": pd.read_excel("").fillna("N/A"),
                            #"Fujitsu": pd.read_excel("").fillna("N/A"),
                            #"Lenovo": pd.read_excel("").fillna("N/A"),
                            #"STDOEM": pd.read_excel("").fillna("N/A"),               
                        }
                        }
    project_pie_chart_columns = {
        "StevieRayV": ['Chipset Name', 'OS', 'Sys Type'],
        "StevieRay": ['CPU_Family', 'Shipping OS Version', 'LP/DT/AIO/DM/SD'],
        "Rhoads": []
        }
    project_bar_chart_columns = {
        "StevieRayV": [('Sys Type', 'Chipset Name'), ('OS', 'Chipset Name'), ('Drive Density', 'Chipset Name')],
        "StevieRay": [('LP/DT/AIO/DM/SD', 'CPU_Family'), ('Shipping OS Version', 'CPU_Family'), ('Shipping drive density', 'CPU_Family')],
        "Rhoads": []
        }
    chosen_dataframe =[]
    chosen_dataframe = srv_data if project_select == "StevieRayV" else sr_data
    # if project_select == "StevieRayV":
    #     chosen_dataframe == srv_data
    # elif project_select == "StevieRay":
    #     chosen_dataframe == sr_data
    # elif project_select == "Rhoads":
    #     chosen_dataframe == rhoads_data
    # else:
    #     return 0
    
    if not chosen_dataframe.empty:
    # Retrieve the lists of columns for pie and bar charts
        pie_columns_to_plot = project_pie_chart_columns.get(project_select, [])
        bar_columns_to_plot = project_bar_chart_columns.get(project_select, [])
        pie_cols = st.columns(len(pie_columns_to_plot))
        for col, column_name in zip(pie_cols, pie_columns_to_plot):
            if column_name in chosen_dataframe.columns:
                plot_pie_chart(chosen_dataframe, column_name, col)
                col.text_area("Pie_chart info",f"Summary for {column_name}", height=100)
            else:
                st.error(f"The column '{column_name}' does not exist in the dataset.")

        bar_cols = st.columns(len(bar_columns_to_plot))
        for col, (x_column, y_column) in zip(bar_cols, bar_columns_to_plot):
            if x_column in chosen_dataframe.columns and y_column in chosen_dataframe.columns:
                #plot_bar_chart(chosen_dataframe, x_column, y_column, st)
                plot_bar_chart(chosen_dataframe, x_column, y_column, col)
                col.text_area("Bar Chart info", f"Data for {x_column} vs {y_column}", height=100)
            else:
                st.error(f"One or more columns '{x_column}' or '{y_column}' do not exist in the dataset.")
        st.write("Inventory Table for reference")
        st.dataframe(chosen_dataframe)
        csv = chosen_dataframe.to_csv(index=False)
        
        st.download_button(
            label="Download Inventory Data",
            data =csv,
            file_name=f'{project_select}_data.csv',
            mime='text/csv'
        )
    else:
        st.error("No data available for the selected project.")

def save_to_excel(data,filename='fetched_data.xlsx'):
    df= pd.DataFrame(data)
    #with pd.ExcelWriter(filename, mode='w'. engine='openpyxl') as writer:
    #    df.to_excel(writer,index=False)
    df.to_csv(filename, index=False)

def test_machine_data_fetcher():
    #st.title("Test Machine Data Fetcher")
    fileldnames = ["Hostname","Data"]
    data=[]
    sys_info=["Hostname","System Model","Chipset","Bios Version","Service"]
    
    Hostnames = st.text_area("Enter Hostname")
    Hostnames_list = [comp.strip() for comp in Hostnames.split(',')]
    selected_option = st.sidebar.selectbox("Select an option",["Fetch System Details","Fetch Service Tag","Fetch SystemStates","Fetch BIOS Version","System_Restart","Fetch Chipset","Fetch System model","Fetch Ram","Fetch GPU Details","Fetch OS Version","Drive Model","Drives Connected", "Storage Controller Info","OEM Manufacturer"])
    
    if st.button("Submit"):
        progress_placeholder=st.empty()
        progress_bar = st.progress(0)
        current_percentage=0
        
        for i, machine in enumerate(Hostnames_list, 1):
               
                percentage=int((i/len(Hostnames_list))*100)
                if percentage!=current_percentage:
                    progress_bar.progress(percentage)
                    progress_placeholder.text(f"Fetching Data {percentage}% Completed!")
                    current_percentage=percentage
                    
                
                if selected_option=="Fetch System Details":
                    sys_info[4]="Service Tag"
                    sys_model_info=Bios_Version_Fetch.Check_System_Model(machine)
                    chipset_info=Bios_Version_Fetch.Check_Chipset(machine)
                    Bios=Bios_Version_Fetch.Check_Bios_Version(machine)
                    service_tag=Bios_Version_Fetch.Check_Servicetag(machine)
                    ram=Bios_Version_Fetch.get_ram(machine)
                    gpu=Bios_Version_Fetch.get_gpu(machine)
                    os_version=Bios_Version_Fetch.Check_OS_Version(machine)
                    dc=Bios_Version_Fetch.getDriveCount(machine)
                    dm=Bios_Version_Fetch.getDriveModel(machine)
                    sc=Bios_Version_Fetch.Get_Drive_Controller(machine)
                    om=Bios_Version_Fetch.Get_manufacturer_info(machine)
                    data.append({"Hostname": machine, "System Model":sys_model_info, "Chipset":chipset_info,  "Bios Version":Bios, "Service Tag":service_tag,"RAM Size":ram,"GPU":gpu, "OS_Version":os_version, "Drives Connected":dc,"Drive Model":dm, "Storage Controller Info":sc, "OEM Manufacturer":om})
                   
                        
                if selected_option=="Fetch OS Version":
                    fileldnames[1]="OS Version"
                    os_version=Bios_Version_Fetch.Check_OS_Version(machine)
                    data.append({"Hostname": machine, "OS Version":os_version})

                if selected_option=="Fetch Service Tag":
                    fileldnames[1]="Service Tag"
                    service_tag=Bios_Version_Fetch.Check_Servicetag(machine)
                    data.append({"Hostname": machine, "Service Tag":service_tag})
                
                if selected_option=="Fetch SystemStates":
                    fileldnames[1]="SystemStates"
                    States=Bios_Version_Fetch.Check_SystemStates(machine)
                    data.append({"Hostname": machine, "SystemStates":States})

                if selected_option=="Fetch BIOS Version":
                    fileldnames[1]="Bios Version"
                    Bios=Bios_Version_Fetch.Check_Bios_Version(machine)
                    data.append({"Hostname": machine, "Bios Version":Bios})
                

                if selected_option=="System_Restart":
                    fileldnames[1]="Status"
                    sys_status=Bios_Version_Fetch.System_Restart(machine)
                    data.append({"Hostname": machine, "Status":sys_status})
        
                if selected_option=="Fetch Chipset":
                    fileldnames[1]="Chipset"
                    chipset_info=Bios_Version_Fetch.Check_Chipset(machine)
                    data.append({"Hostname": machine, "Chipset":chipset_info})   
                
                if selected_option=="Fetch System model":
                    fileldnames[1]="System Model"
                    sys_model_info=Bios_Version_Fetch.Check_System_Model(machine)
                    data.append({"Hostname": machine, "System Model":sys_model_info})
                    
                if selected_option=="Fetch Ram":
                   fileldnames[1]="Ram Size"
                   sys_Ram_info=Bios_Version_Fetch.get_ram(machine)
                   data.append({"Hostname": machine, "Ram Size":sys_Ram_info})

                if selected_option=="Fetch GPU Details":
                   fileldnames[1]="GPU Details"
                   sys_GPU_info=Bios_Version_Fetch.get_gpu(machine)
                   data.append({"Hostname": machine, "GPU":sys_GPU_info})   
                
                if selected_option=="Fetch Drives Connected to System":
                    fileldnames[1]="Drives Connected"  
                    dc=Bios_Version_Fetch.getDriveCount(machine)
                    data.append({"Hostname": machine, "Drives Connected":dc})
                
                if selected_option=="Fetch Drive model":
                    fileldnames[1]="Drive Model"
                    dm=Bios_Version_Fetch.getDriveModel(machine)
                    data.append({"Hostname": machine, "Drive Model":dm}) 
                
                
                if selected_option == "Storage Controller Info":
                    fileldnames[1] = "Storage Controller Info"
                    storage_driver_info = Bios_Version_Fetch.Get_Drive_Controller(machine)
                    data.append({"Hostname": machine, "Storage Controller Info": storage_driver_info})
                
                if selected_option == "OEM Manufacturer":
                   fileldnames[1] = "OEM Manufacturer"
                   oem_info=Bios_Version_Fetch.Get_manufacturer_info(machine)
                   data.append({"Hostname": machine, "OEM Manufacturer":oem_info})
    
        st.success("Task Finished")
        st.table(data)
        
        if selected_option == "Fetch System Details" and data:
             if st.download_button:
                df = pd.DataFrame(data)
                sys_data = df.to_csv(index=False)
                st.download_button(label="Download System Specs", data=sys_data, file_name ="System_Specs.csv", mime="text/csv")
def main():

    with st.sidebar:
        selected_option = st.selectbox('Choose an Option',
        ('Inventory_Management','TestMachine Data Fetcher')
        )
    
    if selected_option == 'TestMachine Data Fetcher':
        st.subheader("Test Machine Data Fetcher")
        test_machine_data_fetcher()

    elif selected_option == "Inventory_Management":
        st.subheader("Inventory_Management")
        Inventory_Management()
            
        
if __name__ == "__main__":
    main()


