import streamlit as st
import math

# Constants
g = 9.81
theta_deg = 20
theta_rad = math.radians(theta_deg)
mu = 0.5
fos = 2.5
efficiency = 0.75
R_drive = 0.02
R_drive_shade = 0.015

st.title("Motor Selection Tool for Sunroof and Sunshade System")

m_glass = st.number_input("Mass of Glass Panel (kg)", min_value=0.0, step=0.1)
m_fabric = st.number_input("Mass of Fabric / Sunshade (kg)", min_value=0.0, step=0.1)
L_arm = st.number_input("Link Arm Length (m)", min_value=0.0, step=0.01)

if st.button("Calculate Torque Requirements"):
    if m_glass == 0 or L_arm == 0:
        st.error("Please enter valid non-zero values.")
    else:
        F_tilt = m_glass * g * (math.sin(theta_rad) + mu * math.cos(theta_rad))
        T_tilt = F_tilt * L_arm
        T_tilt_adj = T_tilt * fos / efficiency

        F_slide_roof = mu * m_glass * g
        T_slide_roof = F_slide_roof * R_drive
        T_slide_roof_adj = T_slide_roof * fos / efficiency

        F_slide_shade = mu * m_fabric * g
        T_slide_shade = F_slide_shade * R_drive_shade
        T_slide_shade_adj = T_slide_shade * fos / efficiency

        st.subheader("Motor Torque Requirements (Nm)")
        st.write(f"**Tilt Torque (raw):** {T_tilt:.2f}")
        st.write(f"**Tilt Torque (adjusted):** {T_tilt_adj:.2f}")
        st.write(f"**Sunroof Slide Torque (raw):** {T_slide_roof:.2f}")
        st.write(f"**Sunroof Slide Torque (adjusted):** {T_slide_roof_adj:.2f}")
        st.write(f"**Sunshade Slide Torque (raw):** {T_slide_shade:.2f}")
        st.write(f"**Sunshade Slide Torque (adjusted):** {T_slide_shade_adj:.2f}")
