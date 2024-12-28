import streamlit as st
from Bios_Info import Bios_Version_Fetch

fileldnames = ["Hostname", "Data"]
data = []
sys_info = ["Hostname", "System Model", "Chipset", "Bios Version", "Service"]

st.title("Remote System Data Fetcher")
Hostnames = st.text_area("Enter Hostname")
Hostnames_list = [comp.strip() for comp in Hostnames.split(",")]
selected_option = st.sidebar.selectbox(
    "Select an option",
    ["Fetch System Details", "Fetch Service Tag", "Fetch SystemStates", "Fetch BIOS Version", "System_Restart", "Fetch Chipset", "Fetch System model", "Storage Controller Info","OEM Manufacturer"],
)
if st.button("Submit"):

    progress_bar = st.progress(0)

    for i, machine in enumerate(Hostnames_list, 1):
        # percentage = int((i / len(Hostnames_list)) * 100)
        # progress_bar.progress(i / len(Hostnames_list), f"Feching Data {percentage}% Completed")

        if selected_option == "Fetch System Details":
            sys_info[4] = "Service Tag"
            sys_model_info = Bios_Version_Fetch.Check_System_Model(machine)
            chipset_info = Bios_Version_Fetch.Check_Chipset(machine)
            Bios = Bios_Version_Fetch.Check_Bios_Version(machine)
            service_tag = Bios_Version_Fetch.Check_Servicetag(machine)
            storage_driver_info = Bios_Version_Fetch.Get_Drive_Controller(machine)
            OEM_Manufacturer = Bios_Version_Fetch.Get_manufacturer_info(machine)
            data.append(
                {
                    "Hostname": machine,
                    "System Model": sys_model_info,
                    "Chipset": chipset_info,
                    "Bios Version": Bios,
                    "Service Tag": service_tag,
                    "Storage Controller Info": storage_driver_info,
                    "OEM Manufacturer":oem_info,
                }
            )

        if selected_option == "Fetch Service Tag":
            fileldnames[1] = "Service Tag"
            service_tag = Bios_Version_Fetch.Check_Servicetag(machine)
            data.append({"Hostname": machine, "Service Tag": service_tag})

        if selected_option == "Fetch SystemStates":
            fileldnames[1] = "SystemStates"
            States = Bios_Version_Fetch.Check_SystemStates(machine)
            data.append({"Hostname": machine, "SystemStates": States})

        if selected_option == "Fetch BIOS Version":
            fileldnames[1] = "Bios Version"
            Bios = Bios_Version_Fetch.Check_Bios_Version(machine)
            data.append({"Hostname": machine, "Bios Version": Bios})

        if selected_option == "System_Restart":
            fileldnames[1] = "Status"
            sys_status = Bios_Version_Fetch.System_Restart(machine)
            data.append({"Hostname": machine, "Status": sys_status})

        if selected_option == "Fetch Chipset":
            fileldnames[1] = "Chipset"
            chipset_info = Bios_Version_Fetch.Check_Chipset(machine)
            data.append({"Hostname": machine, "Chipset": chipset_info})

        if selected_option == "Fetch System model":
            fileldnames[1] = "System Model"
            sys_model_info = Bios_Version_Fetch.Check_System_Model(machine)
            data.append({"Hostname": machine, "System Model": sys_model_info})

        if selected_option == "Storage Controller Info":
            fileldnames[1] = "Storage Controller Info"
            storage_driver_info = Bios_Version_Fetch.Get_Drive_Controller(machine)
            data.append({"Hostname": machine, "Storage Controller Info": storage_driver_info})
        
        if selected_option =="OEM Manufacturer":
            fileldnames[1]="OEM Manufacturer"
            oem_info=Bios_Version_Fetch.Get_manufacturer_info(machine)
            data.append({"Hostname": machine, "OEM Manufacturer":oem_info})
            
    st.success("Task Finished")
    st.table(data)