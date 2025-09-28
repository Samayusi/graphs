import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Interactive Graph", layout="wide")

st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffe0e9 !important;
    color: #111111 !important;
}

/* Botón */
div.stButton > button:first-child {
    background-color: #ff7ea8;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 5px;
    border: none;
    font-size: 20px;
    font-weight: bold;
    margin-top: 10px;
}
div.stButton > button:first-child:hover {
    background-color: #ff7ea8;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: black;
    font-size: 20px;
    margin-top: 50px;
}
.footer a {
    color: #ff0080;
    text-decoration: none;
    margin: 0 10px;
}

/* Header logo */
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

#headder con el logop
st.markdown(
    """
    <div class="header-container">
        <img src="https://www.doitpoms.ac.uk/tlplib/crystallography3/images/lattice_parameters.gif" width="100" style="margin-right:15px;">
        <h1 style='color:#ff0080;'>Interactive Graph</h1>
    </div>
    """,
    unsafe_allow_html=True
)

#inputs del sidebar
st.sidebar.header("Graph Inputs")
titulo = st.sidebar.text_input("Graph Title:", "")
x_vals = st.sidebar.text_input("X values (Current A)", "")
y_vals = st.sidebar.text_input("Y values (Raman shift cm⁻¹)", "")
chart_type = st.sidebar.selectbox("Chart type", ["Scatter", "Line", "Bar"])
plot_btn = st.sidebar.button("Plot")

# toda la logic del grafico
if plot_btn:
    try:
        x_data = np.array([float(i.strip()) for i in x_vals.split(",")])
        y_data = np.array([float(i.strip()) for i in y_vals.split(",")])
        df = pd.DataFrame({"X": x_data, "Y": y_data})

        # Regresión lineal
        m, b = np.polyfit(x_data, y_data, 1)
        y_pred = m * x_data + b
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        eq_text = f"y = {m:.2f}x + {b:.2f} | R² = {r2:.4f}"

        # Gráfico interactivo
        color_palette = {"Scatter": "#ff7ea8", "Line": "#ff7ea8", "Bar": "#ffa0bd"}

        if chart_type == "Scatter":
            fig = px.scatter(df, x="X", y="Y", title=titulo,
                             labels={"X":"Current (A)", "Y":"Raman shift (cm⁻¹)"},
                             color_discrete_sequence=[color_palette["Scatter"]])
        elif chart_type == "Line":
            fig = px.line(df, x="X", y="Y", title=titulo, markers=True,
                          labels={"X":"Current (A)", "Y":"Raman shift (cm⁻¹)"},
                          color_discrete_sequence=[color_palette["Line"]])
        else:
            fig = px.bar(df, x="X", y="Y", title=titulo,
                         labels={"X":"Current (A)", "Y":"Raman shift (cm⁻¹)"},
                         color_discrete_sequence=[color_palette["Bar"]], opacity=0.8)

        from scipy.interpolate import make_interp_spline
        if len(x_data) > 3:
            x_smooth = np.linspace(min(x_data), max(x_data), 300)
            spline = make_interp_spline(x_data, y_data, k=3)
            y_smooth = spline(x_smooth)
            fig.add_scatter(x=x_smooth, y=y_smooth, mode='lines',
                            line=dict(color='black', width=2), showlegend=False)
            
     #cambie esto para q me apareceiran los indices negros   
        fig.update_layout(
    title_font=dict(size=25, color="#ff0080"),
    plot_bgcolor="#f5f5f5",
    paper_bgcolor="#f5f5f5",
    font=dict(color="#111111"),
    xaxis=dict(
        showgrid=True,
        gridcolor="#e0e0e0",
        linecolor="black",
        tickcolor="black",
        tickfont=dict(color="black", size=12),
        title_text="Current (A)",
        title_font=dict(color="black", size=14)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#e0e0e0",
        linecolor="black",
        tickcolor="black",
        tickfont=dict(color="black", size=12),
        title_text="Raman shift (cm⁻¹)",
        title_font=dict(color="black", size=14)
    ),
    hovermode="x unified"
)

        st.plotly_chart(fig, use_container_width=True)

        # Expander con info de regresión
        with st.expander("Show regression info"):
            st.markdown(f"**Equation:** {eq_text}")

    except Exception as e:
        st.error(f"Error: {e}")

#footer
st.markdown("""
<style>
.footer {
    width: 100%;
    background-color: #ffe0e9;
    text-align: center;
    color: black;
    font-size: 16px;
    padding: 10px 20px;
    box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
}
.footer p {
    margin: 2px 0;
    line-height: 1.3;
}
.footer a {
    color: #ff0080;
    text-decoration: none;
    margin: 0 5px;
}
</style>

<div class="footer">
    <p><strong>Paper:</strong> Current-Induced Atomic Displacements and Phonon Dissipation[O1.1] in Hexaborides: A Raman Spectroscopy Study</p>
    <p><strong>Authors:</strong> Oscar E. Jaime-Acuña¹, Jenifer S. Inzunza-Encines⁶, C. Ingram Vargas-Consuelos¹, Doreen Edwards³, Scott T. Misture⁴, Victor R. Vasquez⁵, Oscar Raymond-Herrera², Olivia A. Graeve¹*</p>
    <p>¹ Department of Mechanical and Aerospace Engineering, University of California, San Diego, 9500 Gilman Drive - MC 0411, La Jolla, CA 92093-0411, USA</p>
    <p>² Centro de Nanociencias y Nanotecnología, Universidad Nacional Autónoma de México, Km 107 Carretera Tijuana-Ensenada, C.P. 22800, Ensenada, Baja California, México</p>
    <p>³ Kate Gleason College of Engineering, Rochester Institute of Technology, 77 Lomb Memorial Drive, Rochester, NY 14623-5604</p>
    <p>⁴ Kazuo Inamori School of Engineering, Alfred University, 2 Pine Street, Alfred, NY 14802, USA</p>
    <p>⁵ Chemical and Materials Engineering Department, University of Nevada, Reno, 1644 N. Virginia Street - MS 388, Reno, NV 89557, USA</p>
    <p>⁶ Universidad Autónoma de Baja California, Calzada Universidad #14416, Parque Industrial Internacional, C.P. 22236, Tijuana, Mexico</p>
    <p><strong>Interactive Graph Creator:</strong> Jenifer S. Inzunza-Encines 
        <a href="https://www.linkedin.com/in/jenifer-samanta-inzunza-encines-46120234a/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25"
                 style="vertical-align:middle; margin:0 5px; filter: invert(31%) sepia(94%) saturate(5329%) hue-rotate(309deg) brightness(100%) contrast(101%);">
        </a>
        <span>|</span>
        <a href="mailto:jenifer.inzunza@uabc.edu.mx" style="color:#ff0080; text-decoration:none;">
            jenifer.inzunza@uabc.edu.mx
        </a>
    </p>
</div>
""", unsafe_allow_html=True)


#FIIIN

