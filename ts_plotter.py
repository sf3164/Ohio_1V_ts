import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import plotly.graph_objects as go
import plotly.express as px

'''
UDF Format
("route starting point(rs)", "route ending point(re)", "run number", "sub run number", "sub run start time") --> "event" (TBD the event list stucture)
"pos_x_av_m" --> "x_map_location"
"pos_y_av_m" --> "y_map_location"
"lane_id_av" --> "lane_id"
"pos_x_av_f" --> "x_frenet"
"pos_y_av_f" --> "y_frenet"
"av_latitude" --> "vehicle_lat"
"av_longitude" --> "vehicle_lon"
"speed_av" --> "sped"
"acc_av" --> "acceleration"
'''
# === Load dataset ===
df = pd.read_csv("Updated_Ohio_One_Vehicle.csv")

# === GUI Initialization ===
root = tk.Tk()
root.title("Ohio Time-Space Diagram GUI")

# === Variables ===
selected_rs = tk.StringVar()
selected_re = tk.StringVar()
selected_run = tk.StringVar()
selected_sub_run = tk.StringVar()
selected_start_time = tk.StringVar()
selected_lane = tk.StringVar()
selected_limit = tk.StringVar()
time_min = tk.StringVar()
time_max = tk.StringVar()
space_min = tk.StringVar()
space_max = tk.StringVar()

# === Utility function ===
def get_filtered_df_base():
    return df[
        (df["route starting point(rs)"].astype(str) == selected_rs.get()) &
        (df["route ending point(re)"].astype(str) == selected_re.get()) &
        (df["run number"] == int(float(selected_run.get()))) &
        (df["sub run number"] == float(selected_sub_run.get())) &
        (df["sub run start time"] == int(float(selected_start_time.get()))) &
        (df["lane_id_av"] == int(float(selected_lane.get())))
    ]

# === Update Functions ===
def update_re_options(*args):
    try:
        rs_val = selected_rs.get()
        filtered = df[df["route starting point(rs)"].astype(str) == rs_val]
        re_menu["values"] = sorted(filtered["route ending point(re)"].dropna().astype(str).unique())
        selected_re.set("")
        selected_run.set("")
        selected_sub_run.set("")
        selected_start_time.set("")
        selected_lane.set("")
    except Exception as e:
        print("Error in update_re_options:", e)

def update_run_options(*args):
    try:
        rs_val = selected_rs.get()
        re_val = selected_re.get()
        filtered = df[
            (df["route starting point(rs)"].astype(str) == rs_val) &
            (df["route ending point(re)"].astype(str) == re_val)
        ]
        run_menu["values"] = sorted(filtered["run number"].dropna().unique())
        selected_run.set("")
        selected_sub_run.set("")
        selected_start_time.set("")
        selected_lane.set("")
    except Exception as e:
        print("Error in update_run_options:", e)

def update_sub_run_options(*args):
    try:
        rs_val = selected_rs.get()
        re_val = selected_re.get()
        run_val = int(float(selected_run.get()))
        filtered = df[
            (df["route starting point(rs)"].astype(str) == rs_val) &
            (df["route ending point(re)"].astype(str) == re_val) &
            (df["run number"] == run_val)
        ]
        sub_run_menu["values"] = sorted(filtered["sub run number"].dropna().unique())
        selected_sub_run.set("")
        selected_start_time.set("")
        selected_lane.set("")
    except Exception as e:
        print("Error in update_sub_run_options:", e)

def update_start_time_options(*args):
    try:
        rs_val = selected_rs.get()
        re_val = selected_re.get()
        run_val = int(float(selected_run.get()))
        sub_run_val = float(selected_sub_run.get())
        filtered = df[
            (df["route starting point(rs)"].astype(str) == rs_val) &
            (df["route ending point(re)"].astype(str) == re_val) &
            (df["run number"] == run_val) &
            (df["sub run number"] == sub_run_val)
        ]
        start_time_menu["values"] = sorted(filtered["sub run start time"].dropna().unique())
        selected_start_time.set("")
        selected_lane.set("")
    except Exception as e:
        print("Error in update_start_time_options:", e)

def update_lane_options(*args):
    try:
        rs_val = selected_rs.get()
        re_val = selected_re.get()
        run_val = int(float(selected_run.get()))
        sub_run_val = float(selected_sub_run.get())
        start_time_val = int(float(selected_start_time.get()))

        filtered = df[
            (df["route starting point(rs)"].astype(str) == rs_val) &
            (df["route ending point(re)"].astype(str) == re_val) &
            (df["run number"] == run_val) &
            (df["sub run number"] == sub_run_val) &
            (df["sub run start time"] == start_time_val)
        ]

        lane_vals = sorted(filtered["lane_id_av"].dropna().unique())
        if len(lane_vals) == 0:
            print("[INFO] No lane_id_av found for this combination.")
        lane_menu["values"] = [str(lv) for lv in lane_vals]
        selected_lane.set("")

        update_limit_options()
    except Exception as e:
        print("Error in update_lane_options:", e)

def update_limit_options(*args):
    for widget in [time_min_entry, time_max_entry, space_min_entry, space_max_entry]:
        widget.config(state=tk.DISABLED)
    try:
        filtered = get_filtered_df_base()
        if selected_limit.get() == "Time":
            time_min.set(filtered["Time"].min())
            time_max.set(filtered["Time"].max())
            time_min_entry.config(state=tk.NORMAL)
            time_max_entry.config(state=tk.NORMAL)
        elif selected_limit.get() == "Space":
            space_min.set(filtered["pos_x_av_f"].min())
            space_max.set(filtered["pos_x_av_f"].max())
            space_min_entry.config(state=tk.NORMAL)
            space_max_entry.config(state=tk.NORMAL)
    except:
        pass

def update_vehicle_list(*args):
    try:
        filtered_df = get_filtered_df_base()
        if selected_limit.get() == "Time":
            filtered_df = filtered_df[
                (filtered_df["Time"] >= float(time_min.get())) &
                (filtered_df["Time"] <= float(time_max.get()))
            ]
        elif selected_limit.get() == "Space":
            filtered_df = filtered_df[
                (filtered_df["pos_x_av_f"] >= float(space_min.get())) &
                (filtered_df["pos_x_av_f"] <= float(space_max.get()))
            ]
        vehicle_listbox.delete(0, tk.END)
        for vid in sorted(filtered_df["ID"].dropna().unique()):
            vehicle_listbox.insert(tk.END, str(vid))
    except Exception as e:
        print("Error in update_vehicle_list:", e)

def plot_time_space():
    try:
        filtered_df = get_filtered_df_base()
        selected_vehicles = [vehicle_listbox.get(i) for i in vehicle_listbox.curselection()]
        all_vehicles = filtered_df["ID"].unique()
        if "All" in selected_vehicles or not selected_vehicles:
            vehicle_ids = all_vehicles
        else:
            vehicle_ids = [int(float(v)) for v in selected_vehicles]


        fig = go.Figure()
        color_scale = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Plotly
        vehicle_color_map = {vid: color_scale[i % len(color_scale)] for i, vid in enumerate(sorted(vehicle_ids))}

        for vid in vehicle_ids:
            vehicle_df = filtered_df[filtered_df["ID"] == vid].sort_values("Time")
            if selected_limit.get() == "Time":
                vehicle_df = vehicle_df[
                    (vehicle_df["Time"] >= float(time_min.get())) &
                    (vehicle_df["Time"] <= float(time_max.get()))
                ]
            elif selected_limit.get() == "Space":
                vehicle_df = vehicle_df[
                    (vehicle_df["pos_x_av_f"] >= float(space_min.get())) &
                    (vehicle_df["pos_x_av_f"] <= float(space_max.get()))
                ]
            fig.add_trace(go.Scatter(
                x=vehicle_df["Time"],
                y=vehicle_df["pos_x_av_f"],
                mode="markers",
                name=f"Vehicle {vid}",
                marker=dict(color=vehicle_color_map[vid]),
                customdata=vehicle_df[["ID", "Time", "pos_x_av_f"]],
                hovertemplate=(
                    "Vehicle ID: %{customdata[0]}<br>" +
                    "Time: %{customdata[1]:.2f}<br>" +
                    "Distance: %{customdata[2]:.2f} m<br>" +
                    "<extra></extra>"
                )
            ))
        fig.update_layout(
            title="Time-Space Diagram",
            xaxis_title="Time (s)",
            yaxis_title="x frenet Distance (m)",
            template="plotly_white"
        )
        fig.write_html("Ohio_One_Vehicle_TS_Diagram.html")
        fig.show()
    except Exception as e:
        messagebox.showerror("Plot Error", str(e))

# === GUI Layout ===
row = 0
tk.Label(root, text="Trip Origin (rs):").grid(row=row, column=0)
rs_menu = ttk.Combobox(root, textvariable=selected_rs, values=sorted(df["route starting point(rs)"].dropna().astype(str).unique()), state="readonly")
rs_menu.grid(row=row, column=1)
rs_menu.bind("<<ComboboxSelected>>", update_re_options)

row += 1
tk.Label(root, text="Trip Destination (re):").grid(row=row, column=0)
re_menu = ttk.Combobox(root, textvariable=selected_re, values=[], state="readonly")
re_menu.grid(row=row, column=1)
re_menu.bind("<<ComboboxSelected>>", update_run_options)

row += 1
tk.Label(root, text="Run Number:").grid(row=row, column=0)
run_menu = ttk.Combobox(root, textvariable=selected_run, values=[], state="readonly")
run_menu.grid(row=row, column=1)
run_menu.bind("<<ComboboxSelected>>", update_sub_run_options)

row += 1
tk.Label(root, text="Sub Run Number:").grid(row=row, column=0)
sub_run_menu = ttk.Combobox(root, textvariable=selected_sub_run, values=[], state="readonly")
sub_run_menu.grid(row=row, column=1)
sub_run_menu.bind("<<ComboboxSelected>>", update_start_time_options)

row += 1
tk.Label(root, text="Sub Run Start Time:").grid(row=row, column=0)
start_time_menu = ttk.Combobox(root, textvariable=selected_start_time, values=[], state="readonly")
start_time_menu.grid(row=row, column=1)
start_time_menu.bind("<<ComboboxSelected>>", update_lane_options)

row += 1
tk.Label(root, text="Lane:").grid(row=row, column=0)
lane_menu = ttk.Combobox(root, textvariable=selected_lane, values=[], state="readonly")
lane_menu.grid(row=row, column=1)
lane_menu.bind("<<ComboboxSelected>>", update_limit_options)

row += 1
tk.Label(root, text="Limit by:").grid(row=row, column=0)
limit_menu = ttk.Combobox(root, textvariable=selected_limit, values=["None", "Time", "Space"], state="readonly")
limit_menu.grid(row=row, column=1)
limit_menu.bind("<<ComboboxSelected>>", update_limit_options)

row += 1
tk.Label(root, text="Time Range:").grid(row=row, column=0)
time_min_entry = tk.Entry(root, textvariable=time_min, state=tk.DISABLED)
time_max_entry = tk.Entry(root, textvariable=time_max, state=tk.DISABLED)
time_min_entry.grid(row=row, column=1)
time_max_entry.grid(row=row, column=2)

row += 1
tk.Label(root, text="Space Range:").grid(row=row, column=0)
space_min_entry = tk.Entry(root, textvariable=space_min, state=tk.DISABLED)
space_max_entry = tk.Entry(root, textvariable=space_max, state=tk.DISABLED)
space_min_entry.grid(row=row, column=1)
space_max_entry.grid(row=row, column=2)

row += 1
tk.Label(root, text="Select Vehicles:").grid(row=row, column=0)
vehicle_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
vehicle_listbox.grid(row=row, column=1)
tk.Button(root, text="Update Vehicles", command=update_vehicle_list).grid(row=row, column=2)

row += 1
tk.Button(root, text="Plot Time-Space Diagram", command=plot_time_space).grid(row=row, column=0, columnspan=3)

root.mainloop()
