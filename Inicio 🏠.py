import streamlit as st
from streamlit_js_eval import get_geolocation
from src.tools import generate_recomendation


st.set_page_config(page_title="Sembrando Con-ciencia",
                   layout="centered",
                   initial_sidebar_state="expanded",
                   page_icon="🌾")


st.title("🌾 Historia de un Campesino Colombiano")


st.image("media/campesino.jpg", caption="Doña Elena, la campesina colombiana",use_container_width=True)


st.markdown("""
#### 👩‍🌾 Hola, soy Doña Elena

Vivo en **Aquitania, Boyacá**, y todos los días trabajo mi tierra con amor.  
""")

lat, lon = 5.518602, -72.88399  

st.markdown("##### Ubicación de la finca")

col1, col2 = st.columns(2)
col1.metric("📌 Latitud", f"{lat}")
col2.metric("📌 Longitud", f"{lon}")


st.map(
    data={
        'lat': [lat],
        'lon': [lon]
    },
    width=700,
    height=400
)


st.markdown("""
Pero a veces el clima cambia 🌧️, llegan plagas 🐛, o no sé qué sembrar para que valga la pena…

He escuchado que hay una herramienta que me puede ayudar **Sembrando Con-ciencia**.

Según dicen, me sugiere qué sembrar según el clima, el suelo y lo que más se vende por aquí.

La verdad, me da un poco de nervios porque no sé mucho de tecnología 😅  
Pero confío en ti...

👉 **¿Podrías generar una recomendación para mí?**
""")


if st.button("🔍 Generar recomendación", type="primary"):
    with st.spinner("⏳ Generando recomendación para Doña Elena..."):
        try:
            recomendados = generate_recomendation(lat, lon, "TODOS")  

            if not recomendados.empty:
                st.success("✅ Recomendación generada con éxito. ¡Gracias por tu ayuda!")

                st.markdown("### 🌱 Recomendación de cultivos para Doña Elena")
                st.markdown("Estos son los cultivos que podría considerar sembrar en su finca en **Aquitania, Boyacá**:")

                for index, row in recomendados.iterrows():
                    grupo = row['GRUPO \nDE CULTIVO']
                    cultivo = row['CULTIVO']
                    rendimiento = row['Rendimiento\n(t/ha)']

                    st.markdown(f"""
                    - **{grupo}** → 🌾 *{cultivo}*  
                      &nbsp;&nbsp;&nbsp;&nbsp;📈 Rendimiento estimado: **{rendimiento} t/ha**
                    """)

            else:
                st.warning("⚠️ No se encontraron recomendaciones con los criterios actuales.")

        except Exception as e:
            st.error(f"❌ Ocurrió un error al generar la recomendación: `{e}`")









