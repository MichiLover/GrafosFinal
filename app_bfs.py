import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import re

# ====================================================================
# [1] FUNCIONES DE GRAFOS Y ALGORITMO BFS
# ====================================================================

def parsear_entrada_a_grafo(texto_conexiones):
    """
    Convierte el texto de entrada del usuario (ej: A B, B C) en un diccionario de grafo.
    """
    grafo = {}
    lineas = texto_conexiones.strip().split('\n')
    
    for linea in lineas:
        # Usa regex para limpiar y dividir la línea, aceptando letras y números
        nodos = re.findall(r'[\w]+', linea.strip())
        
        if len(nodos) == 2:
            nodo1, nodo2 = nodos
            
            # Asegurar que ambos nodos existan como claves
            if nodo1 not in grafo:
                grafo[nodo1] = []
            if nodo2 not in grafo:
                grafo[nodo2] = []
            
            # Conexión no dirigida (si A se conecta a B, B se conecta a A)
            if nodo2 not in grafo[nodo1]:
                grafo[nodo1].append(nodo2)
            if nodo1 not in grafo[nodo2]:
                grafo[nodo2].append(nodo1)
                
    return grafo

def bfs_grados_de_separacion(grafo, inicio, destino):
    """
    Ejecuta el BFS para encontrar la ruta más corta en saltos.
    Devuelve la ruta (lista) y el mensaje de error si aplica.
    """
    if inicio not in grafo or destino not in grafo:
        return None, "Error: El nodo de inicio o destino no existe en el grafo definido."
        
    cola = deque([(inicio, [inicio])]) 
    visitados = {inicio}
    
    while cola:
        nodo_actual, camino_actual = cola.popleft()
        
        if nodo_actual == destino:
            return camino_actual, None
        
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino_actual + [vecino]))
    
    return None, "No hay conexión posible entre los dos nodos seleccionados."

def dibujar_grafo(grafo, ruta):
    """
    Dibuja el grafo usando NetworkX y Matplotlib, resaltando la ruta.
    """
    G = nx.Graph(grafo)
    
    # 1. Definir la posición de los nodos
    pos = nx.spring_layout(G, seed=42)
    
    # 2. Colorear los nodos de la ruta
    node_colors = ['#FF6347' if nodo in ruta else '#ADD8E6' for nodo in G.nodes()]
    
    # 3. Colorear las aristas de la ruta
    ruta_edges = list(zip(ruta, ruta[1:]))
    edge_colors = ['#FF6347' if (u, v) in ruta_edges or (v, u) in ruta_edges else '#CCCCCC' 
                   for u, v in G.edges()]
    
    # Dibujar
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw(G, pos, ax=ax, with_labels=True, node_size=3000, 
            node_color=node_colors, font_size=12, font_weight='bold', 
            edge_color=edge_colors, width=3)
    
    return fig

# ====================================================================
# [2] INTERFAZ STREAMLIT
# ====================================================================

st.set_page_config(layout="wide")
st.title("🌐 Demostración Interactiva del Algoritmo BFS")
st.subheader("Aplicación Real: Grados de Separación en Redes")
st.markdown("---")

st.markdown("## 📚 Contexto Teórico: Teoría de Grafos y BFS")
st.markdown(
    """
    La **Teoría de Grafos** es una herramienta matemática fundamental para modelar **relaciones** y **conexiones** entre elementos (como personas, ciudades, o sistemas).
    
    * **Nodos (Vértices):** Los elementos (personas, ubicaciones).
    * **Aristas (Conexiones):** La relación entre ellos (amistad o amigos en común).
    """
)

st.markdown("---")

st.markdown("### Resultado")
st.markdown(
    """
        "Para la demostración, se va a usar la lógica de Facebook. 
        El Orígen será el usuario (Yo), y el Destino será una persona desconocida. 
        El algoritmo BFS va a recorrer la red nivel por nivel para garantizarnos 
        que la ruta que se muestra en rojo (la ruta más corta) es el camino más eficiente para conectar a esas dos personas, dándonos el número exacto de intermediarios."
    """
)

st.markdown("### Algoritmo: Búsqueda en Anchura (BFS)")
st.markdown(
    """
        Implementamos el algoritmo **Búsqueda en Anchura (BFS)** porque es ideal para encontrar el camino más corto en redes donde todas las conexiones tienen el mismo 'peso' (un costo unitario de 1).
        
        **Propósito:** Encontrar la ruta con la **menor cantidad de pasos** o **intermediarios** (los 'grados de separación').
        
        **💡 Caso de Uso Real: Búsqueda de Amigos en Redes Sociales**
        
        Este algoritmo es el corazón de sistemas como **Facebook o LinkedIn**. Se utiliza para:
        
        1.  **Sugerir Amigos en Común:** Mostrar contactos que están a **1 o 2 pasos** de distancia.
        2.  **Calcular Grados de Separación:** Determinar la ruta con el **mínimo número de personas** (o saltos) que te separan de cualquier otra persona en la red.
    """
)
# --- Grafo por defecto para facilitar la prueba ---
DEFAULT_CONNECTIONS = """
A B
B C
C D
D E
E F
A G
G H
H I
I J
J F
C G
"""

# --- Área de entrada y Creación del Grafo ---
st.sidebar.header("1. Definir Conexiones (Aristas)")
st.sidebar.caption("Ingrese cada conexión en una nueva línea (ej: 'Nodo1 Nodo2').")
conexiones_texto = st.sidebar.text_area(
    "Estructura del Grafo:", 
    DEFAULT_CONNECTIONS,
    height=200
)

# Parsear el texto para obtener el grafo
grafo = parsear_entrada_a_grafo(conexiones_texto)
nodos_disponibles = sorted(list(grafo.keys()))

# --- Selección de Origen y Destino ---
st.sidebar.header("2. Seleccionar Recorrido")
if not nodos_disponibles:
    st.sidebar.warning("Defina las conexiones para ver los nodos disponibles.")
    inicio = None
    destino = None
else:
    # Usamos st.selectbox para que el usuario elija
    inicio = st.sidebar.selectbox("Nodo de Origen:", nodos_disponibles)
    destino = st.sidebar.selectbox("Nodo de Destino:", nodos_disponibles)

# --- Botón de Ejecución ---
st.sidebar.markdown("---")
if st.sidebar.button("🔍 Buscar Camino (Ejecutar BFS)"):
    if inicio and destino:
        
        # 3. Ejecutar el Algoritmo BFS
        ruta, error_msg = bfs_grados_de_separacion(grafo, inicio, destino)
        
        if ruta:
            grados_separacion = len(ruta) - 1
            
            # Mostrar resultados
            st.success("✅ ¡Ruta más corta encontrada por BFS!")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Grados de Separación (Pasos)", value=grados_separacion)
            
            with col2:
                st.write(f"**Ruta:** {' → '.join(ruta)}")

            # 4. Mostrar el Grafo Visual
            st.markdown("---")
            st.markdown("### 🗺️ Visualización del Recorrido (Ruta resaltada en rojo)")
            figura = dibujar_grafo(grafo, ruta)
            st.pyplot(figura)
            
        else:
            st.error(f"❌ {error_msg}")
    else:
        st.error("Por favor, defina un grafo válido y seleccione Origen/Destino.")

# --- Mostrar Grafo Inicial (Solo para referencia) ---
st.markdown("### 📊 Estructura del Grafo Actual")
st.json(grafo)