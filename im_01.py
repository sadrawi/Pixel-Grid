import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# st.logo("logo.png")

st.image("i3L.png")

col00, col01 = st.columns([0.75,1])
with col01:
    st.image("BT v1.png")
with col00:
    st.image("SHL.png")
        
st.title("Pixel Grid Inspector")


uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:

    img = Image.open(uploaded_file).convert("RGB")
    width, height = img.size

    st.write(f"Image size: {width} x {height}")

    col1, col2, col3 = st.columns(3)

    with col1:
        # st.subheader("Start Position")
        x0 = st.number_input("Start X", 0, width-1, 5, step=1)
        y0 = st.number_input("Start Y", 0, height-1, 5, step=1)

    with col2:
        # st.subheader("Interval")
        dx = st.number_input("Interval X", 1, width, 50, step=1)
        dy = st.number_input("Interval Y", 1, height, 50, step=1)

    with col3:
        # st.subheader("Point No")
        nx = st.number_input("Number of points in X direction", 1, 100, 1)
        ny = st.number_input("Number of points in Y direction", 1, 100, 1)


    # # Base point
    # x0 = st.number_input("Start X", 0, width-1, 0, step=1)
    # y0 = st.number_input("Start Y", 0, height-1, 0, step=1)

    # # Interval
    # dx = st.number_input("Interval X (dx)", 1, width, 50, step=1)
    # dy = st.number_input("Interval Y (dy)", 1, height, 50, step=1)

    # # Number of points
    # nx = st.number_input("Number of points in X direction", 1, 100, 5)
    # ny = st.number_input("Number of points in Y direction", 1, 100, 5)

    points_x = []
    points_y = []
    marker_numbers = []
    rgb_values = []

    marker_id = 1

    for iy in range(ny):
        for ix in range(nx):

            x = x0 + ix * dx
            y = y0 + iy * dy

            if x < width and y < height:

                r, g, b = img.getpixel((x, y))

                points_x.append(x)
                points_y.append(y)
                marker_numbers.append(marker_id)

                rgb_values.append({
                    "Marker": marker_id,
                    "X": x,
                    "Y": y,
                    "R": r,
                    "G": g,
                    "B": b
                })

                marker_id += 1

    # Create DataFrame
    df = pd.DataFrame(rgb_values)

    # Show image
    fig = px.imshow(img)

    fig.add_scatter(
        x=points_x,
        y=points_y,
        mode="markers+text",
        marker=dict(size=2, color="red"),
        text=marker_numbers,
        textposition="top center",

        textfont=dict(
        color="rgb(255,15,0)",   # ← change number color here
        size=16,
        family="Arial"
        ),

        showlegend=False
    )

    fig.update_layout(
        width=1000,   # figure width in pixels
        height=800    # figure height in pixels
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show table AFTER image
    st.subheader("RGB Values Table")
    st.dataframe(df, use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download CSV",
        csv,
        "rgb_values.csv",
        "text/csv"

    )









