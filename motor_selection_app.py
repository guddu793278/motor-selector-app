import streamlit as st
import pandas as pd
import math

# === CONSTANTS ===
g = 9.81
theta_deg = 20
theta_rad = math.radians(theta_deg)
mu = 0.5
FOS = 2.0
efficiency = 0.80
R_drive_roof = 0.02
R_drive_shade = 0.015

st.title("Motor Selection Tool for Sunroof and Sunshade System")

# === USER INPUTS ===
m_glass = st.number_input("Mass of Glass Panel (kg)", min_value=0.0, step=0.1)
m_fabric = st.number_input("Mass of Fabric / Sunshade (kg)", min_value=0.0, step=0.1)
L_arm = st.number_input("Link Arm Length (m)", min_value=0.0, step=0.01)
motor_file = st.file_uploader("Upload Motor Library CSV (with specs only)", type=["csv"])

# === PROCESS ===
if st.button("Calculate and Select Motor"):
    if m_glass == 0 or L_arm == 0 or motor_file is None:
        st.error("Please enter all required values and upload the motor library.")
    else:
        # Torque Calculations
        F_tilt = m_glass * g * (math.sin(theta_rad) + mu * math.cos(theta_rad))
        T_tilt = F_tilt * L_arm
        T_tilt_adj = T_tilt * FOS / efficiency

        F_slide_roof = mu * m_glass * g
        T_slide_roof = F_slide_roof * R_drive_roof
        T_slide_roof_adj = T_slide_roof * FOS / efficiency

        F_slide_shade = mu * m_fabric * g
        T_slide_shade = F_slide_shade * R_drive_shade
        T_slide_shade_adj = T_slide_shade * FOS / efficiency

        max_required_torque = max(T_tilt_adj, T_slide_roof_adj, T_slide_shade_adj)

        # Show torque results
        st.subheader("Motor Torque Requirements (Adjusted, Nm)")
        st.write({
            "Tilt": round(T_tilt_adj, 2),
            "Sunroof Slide": round(T_slide_roof_adj, 2),
            "Sunshade Slide": round(T_slide_shade_adj, 2),
            "Max Required Torque": round(max_required_torque, 2)
        })

        # Load and filter motor library
        try:
            motor_df = pd.read_csv(motor_file)

            suitable_motors = motor_df[
                (motor_df["Rated Torque (Nm)"] >= max_required_torque)
            ]

            st.subheader("✅ Suitable Motors Based on Specifications")
            if not suitable_motors.empty:
                st.dataframe(suitable_motors[[
                    "Motor Name", "Rated Torque (Nm)", "Operating Voltage (V)", "RPM", "Power (W)"
                ]])
            else:
                st.warning("❌ No motors meet the required torque.")
        except Exception as e:
            st.error(f"Error reading motor library: {e}")

