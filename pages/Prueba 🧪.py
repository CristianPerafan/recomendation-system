import streamlit as st
from streamlit_js_eval import get_geolocation
from src.tools import generate_recomendation

st.title("🧪 Prueba el sistema recomendador tú mismo")



location = get_geolocation()

lat, lon = location['coords']['latitude'], location['coords']['longitude']

st.markdown("##### Ubicación de la finca")

st.write("Tu ubicación actual es:")
col1, col2 = st.columns(2)
col1.metric("📌 Latitud", f"{lat}")
col2.metric("📌 Longitud", f"{lon}")

opciones = ["TODOS", "ANUAL", "PERMANENTE", "TRANSITORIO"]
# Selectbox para elegir una opción
opcion_seleccionada = st.selectbox("Selecciona el ciclo de cultivo:", opciones)

st.map(
    data={
        'lat': [lat],
        'lon': [lon]
    },  
    width=700,
    height=400
)



if st.button("🔍 Generar recomendación", type="primary"):
    with st.spinner("⏳ Generando recomendación para Doña Elena..."):
        try:
            recomendados = generate_recomendation(lat, lon, opcion_seleccionada)  

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
    