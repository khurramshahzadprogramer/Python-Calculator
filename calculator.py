import streamlit as st

# Page Configuration
st.set_page_config(page_title="Modern Pro Calculator", page_icon="🧮", layout="centered")

# Custom Dark Theme CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #0F172A;
    }
    .stButton>button {
        width: 100%;
        height: 55px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        color: white;
        background-color: #334155;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #475569;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #F8FAFC;'>🧮 Modern Pro Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>A sleek and responsive calculator built with Python & Streamlit</p>", unsafe_allow_html=True)

# Session state to store input expression
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Display screen
display_val = st.session_state.expression if st.session_state.expression else "0"
st.text_input("Display", value=display_val, disabled=True, label_visibility="collapsed")

# Button click handler
def add_to_expression(val):
    st.session_state.expression += str(val)

def clear_expression():
    st.session_state.expression = ""

def calculate_result():
    try:
        # Safe evaluation of mathematical expression
        result = eval(st.session_state.expression)
        st.session_state.expression = str(result)
    except ZeroDivisionError:
        st.session_state.expression = "Math Error"
    except Exception:
        st.session_state.expression = "Error"

# Calculator Keypad Layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("C", use_container_width=True):
        clear_expression()
        st.rerun()
    if st.button("7", use_container_width=True):
        add_to_expression("7")
        st.rerun()
    if st.button("4", use_container_width=True):
        add_to_expression("4")
        st.rerun()
    if st.button("1", use_container_width=True):
        add_to_expression("1")
        st.rerun()
    if st.button("0", use_container_width=True):
        add_to_expression("0")
        st.rerun()

with col2:
    if st.button("⌫", use_container_width=True):
        st.session_state.expression = st.session_state.expression[:-1]
        st.rerun()
    if st.button("8", use_container_width=True):
        add_to_expression("8")
        st.rerun()
    if st.button("5", use_container_width=True):
        add_to_expression("5")
        st.rerun()
    if st.button("2", use_container_width=True):
        add_to_expression("2")
        st.rerun()
    if st.button(".", use_container_width=True):
        add_to_expression(".")
        st.rerun()

with col3:
    if st.button("/", use_container_width=True):
        add_to_expression("/")
        st.rerun()
    if st.button("9", use_container_width=True):
        add_to_expression("9")
        st.rerun()
    if st.button("6", use_container_width=True):
        add_to_expression("6")
        st.rerun()
    if st.button("3", use_container_width=True):
        add_to_expression("3")
        st.rerun()
    if st.button("=", use_container_width=True):
        calculate_result()
        st.rerun()

with col4:
    if st.button("*", use_container_width=True):
        add_to_expression("*")
        st.rerun()
    if st.button("-", use_container_width=True):
        add_to_expression("-")
        st.rerun()
    if st.button("+", use_container_width=True):
        add_to_expression("+")
        st.rerun()