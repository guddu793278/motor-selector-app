import streamlit as st
import pandas as pd
import math

# Constants
g = 9.81
theta_deg = 20
theta_rad = math.radians(theta_deg)
mu = 0.5
FOS = 2.5
efficiency = 0.75
R_drive_roof = 0.02
R_drive_shade = 0.015

st.title("Motor Selection Tool for Sunroof and Sunshade System")

# Inputs
m_glass = st.number_input("Mass of Glass Panel (kg)", min_value=0.0, step=0.1)
m_fabric = st.number_input("Mass of Fabric / Sunshade (kg)", min_value=0.0, step=0.1)
L_arm = st.number_input("Link Arm Length (m)", min_value=0.0, step=0.01)
motor_file = st.file_uploader("Upload Motor Library CSV", type=["csv"])

if st.button("Calculate Torque Requirements"):
    if m_glass == 0 or L_arm == 0:
        st.error("Please enter all values.")
    else:
        # Calculations
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

        # Show torque calculations
        st.subheader("Motor Torque Requirements (Nm)")
        st.write(f"Tilt Torque (raw): {T_tilt:.2f}")
        st.write(f"Tilt Torque (adjusted): {T_tilt_adj:.2f}")
        st.write(f"Sunroof Slide Torque (raw): {T_slide_roof:.2f}")
        st.write(f"Sunroof Slide Torque (adjusted): {T_slide_roof_adj:.2f}")
        st.write(f"Sunshade Slide Torque (raw): {T_slide_shade:.2f}")
        st.write(f"Sunshade Slide Torque (adjusted): {T_slide_shade_adj:.2f}")

        # Motor selection
        if motor_file:
            try:
                motor_df = pd.read_csv(motor_file)

                spec_motors = motor_df[
                    (motor_df["Has Curve Only (Yes/No)"].str.lower() == "no") &
                    (motor_df["Rated Torque (Nm)"] >= max_required_torque)
                ]

                curve_only = motor_df[
                    motor_df["Has Curve Only (Yes/No)"].str.lower() == "yes"
                ]

                st.subheader("✅ Suitable Motors from Specifications")
                if not spec_motors.empty:
                    st.dataframe(spec_motors[["Motor Name", "Rated Torque (Nm)", "Operating Voltage (V)", "RPM", "Power (W)"]])
                else:
                    st.warning("❌ No suitable motors found based on specifications.")

                st.subheader("📉 Motors with Only Graphs (Manual Review Needed)")
                if not curve_only.empty:
                    st.dataframe(curve_only[["Motor Name"]])
                else:
                    st.info("None marked as curve-only.")

            except Exception as e:
                st.error(f"Error reading motor library: {e}")
        else:
            st.warning("Upload a motor library CSV to check for suitable motors.")

