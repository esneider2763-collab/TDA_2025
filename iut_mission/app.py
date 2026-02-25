if enviar:
            nota = 0
            for i, p in enumerate(st.session_state.preguntas_examen):
                if respuestas_usuario[i] == p['correcta']:
                    nota += 4
            
            # --- EL TOQUE MAESTRO: Guardar en el Búnker de Notas ---
            resultado = pd.DataFrame({
                'Fecha': [datetime.now().strftime("%Y-%m-%d %H:%M")],
                'Cedula': [cedula],
                'Nota': [nota]
            })
            
            # Si el archivo no existe, lo crea con encabezados
            if not os.path.isfile("notas_iut.csv"):
                resultado.to_csv("notas_iut.csv", index=False)
            else:
                resultado.to_csv("notas_iut.csv", mode='a', header=False, index=False)
            
            st.metric("Resultado Final", f"{nota}/20")
            if nota >= 10: st.balloons()
