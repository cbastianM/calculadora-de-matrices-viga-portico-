import streamlit as st
import sympy as sp
import math

# === OPCIÓN 1: MATRIZ DE VIGA 4×4 (EI constante) ===
def matriz_viga_4x4(L: float):
    EI = 1
    return sp.Matrix([
        [ 12*EI/L**3,  6*EI/L**2, -12*EI/L**3,  6*EI/L**2],
        [  6*EI/L**2,   4*EI/L  ,  -6*EI/L**2,   2*EI/L  ],
        [-12*EI/L**3, -6*EI/L**2,  12*EI/L**3, -6*EI/L**2],
        [  6*EI/L**2,   2*EI/L  ,  -6*EI/L**2,   4*EI/L  ],
    ]).evalf(3)

# === OPCIÓN 2: MATRIZ LOCAL PARA PÓRTICO 2D (6×6) ===
def matriz_portico(E, I, A, L, Theta_deg):
    """
    Genera la matriz de rigidez local en coordenadas globales para un pórtico 2D.
    Theta_deg: Ángulo en grados (convertido internamente a radianes)
    """
    Theta = math.radians(Theta_deg)
    lmbda = sp.cos(Theta)
    mu = sp.sin(Theta)

    EA_L = E*A/L
    EI_L = E*I/L
    EI_L2 = E*I/L**2
    EI_L3 = E*I/L**3

    matriz = sp.Matrix([
        [ EA_L*lmbda**2 + 12*EI_L3*mu**2,    (EA_L - 12*EI_L3)*lmbda*mu,         -6*EI_L2*mu,     -EA_L*lmbda**2 - 12*EI_L3*mu**2,   -(EA_L - 12*EI_L3)*lmbda*mu,      -6*EI_L2*mu ],
        [ (EA_L - 12*EI_L3)*lmbda*mu,        EA_L*mu**2 + 12*EI_L3*lmbda**2,      6*EI_L2*lmbda,   -(EA_L - 12*EI_L3)*lmbda*mu,      -EA_L*mu**2 - 12*EI_L3*lmbda**2,   6*EI_L2*lmbda ],
        [ -6*EI_L2*mu,                       6*EI_L2*lmbda,                      4*EI_L,          6*EI_L2*mu,                        -6*EI_L2*lmbda,                    2*EI_L ],
        [ -EA_L*lmbda**2 - 12*EI_L3*mu**2,   -(EA_L - 12*EI_L3)*lmbda*mu,         6*EI_L2*mu,      EA_L*lmbda**2 + 12*EI_L3*mu**2,   (EA_L - 12*EI_L3)*lmbda*mu,        6*EI_L2*mu ],
        [ -(EA_L - 12*EI_L3)*lmbda*mu,       -EA_L*mu**2 - 12*EI_L3*lmbda**2,     -6*EI_L2*lmbda,   (EA_L - 12*EI_L3)*lmbda*mu,      EA_L*mu**2 + 12*EI_L3*lmbda**2,   -6*EI_L2*lmbda ],
        [ -6*EI_L2*mu,                       6*EI_L2*lmbda,                      2*EI_L,          6*EI_L2*mu,                        -6*EI_L2*lmbda,                    4*EI_L ]
    ])
    return matriz.evalf(3)

# === APP PRINCIPAL ===
def main():
    st.title("🏗️ Generador de Matrices de Rigidez (Viga / Pórtico)")

    st.write(
        "Selecciona el tipo de elemento estructural que deseas analizar y "
        "proporciona los parámetros necesarios. El resultado se mostrará en formato matemático (LaTeX)."
    )

    # Selector de modo
    modo = st.radio(
        "Selecciona el tipo de matriz a generar:",
        ("Matriz local 4×4 de Viga", "Matriz local 6×6 de Pórtico 2D")
    )

    # --- OPCIÓN 1: MATRIZ DE VIGA ---
    if modo == "Matriz local 4×4 de Viga":
        st.subheader("Parámetros de la viga")
        L = st.number_input("Longitud (L)", min_value=0.1, value=10.0)
        if st.button("Generar matriz de viga"):
            K = matriz_viga_4x4(L)
            st.markdown("### 🧮 Matriz local 4×4 de viga")
            st.markdown(f"$$ 1/EI {sp.latex(K)} $$")
            st.caption("EI se considera constante.")

    # --- OPCIÓN 2: MATRIZ DE PÓRTICO ---
    elif modo == "Matriz local 6×6 de Pórtico 2D":
        st.subheader("Parámetros del pórtico 2D")
        E = st.number_input("Módulo de Elasticidad (E)", min_value=0.0, value=20000000.0)
        I = st.number_input("Momento de Inercia (I)", min_value=0.0, value=5000.0)
        A = st.number_input("Área de la Sección (A)", min_value=0.0, value=0.3)
        L = st.number_input("Longitud (L)", min_value=0.1, value=6.0)
        Theta_deg = st.number_input("Ángulo Θ (en grados)", min_value=0.0, max_value=360.0, value=0.0)

        if st.button("Generar matriz del pórtico"):
            K = matriz_portico(E, I, A, L, Theta_deg)
            st.markdown("### 🧮 Matriz local 6×6 del pórtico 2D")
            st.markdown(f"$$ {sp.latex(K)} $$")

if __name__ == "__main__":
    main()
