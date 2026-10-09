import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for UI/UX replication & responsiveness
st.markdown("""
<style>
    /* App background */
    .stApp {
        background-color: #F4F6F9;
    }
    
    /* Center container max width */
    .block-container {
        max-width: 440px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Calculator card container */
    .calc-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }

    /* Display box */
    .calc-display {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: right;
        margin-bottom: 20px;
    }

    .calc-history {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 14px;
        color: #64748B;
        min-height: 20px;
        word-break: break-all;
    }

    .calc-result {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 32px;
        font-weight: bold;
        color: #1E293B;
        word-break: break-all;
    }

    .calc-error {
        color: #E11D48 !important;
    }

    /* Base button styling */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        height: 52px;
        border: none;
        box-shadow: none;
        transition: background-color 0.15s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_input" not in st.session_state:
    st.session_state.current_input = "0"
if "previous_value" not in st.session_state:
    st.session_state.previous_value = None
if "operator" not in st.session_state:
    st.session_state.operator = None
if "reset_screen" not in st.session_state:
    st.session_state.reset_screen = False
if "history_text" not in st.session_state:
    st.session_state.history_text = ""
if "error_state" not in st.session_state:
    st.session_state.error_state = False

def format_number(num):
    if num is None:
        return "0"
    if num == int(num) and not (isinstance(num, float) and abs(num) > 1e15):
        val_str = str(int(num))
    else:
        val_str = f"{num:.10g}"
    return val_str

def get_display_string():
    display_str = st.session_state.current_input
    if len(display_str) > 12:
        try:
            f_val = float(display_str)
            display_str = f"{f_val:.6e}"
        except Exception:
            display_str = display_str[:12]
    return display_str

def clear_all():
    st.session_state.current_input = "0"
    st.session_state.previous_value = None
    st.session_state.operator = None
    st.session_state.reset_screen = False
    st.session_state.history_text = ""
    st.session_state.error_state = False

def calculate(intermediate=False):
    try:
        current_value = float(st.session_state.current_input)
        result = 0.0

        if st.session_state.operator == "+":
            result = st.session_state.previous_value + current_value
        elif st.session_state.operator == "-":
            result = st.session_state.previous_value - current_value
        elif st.session_state.operator == "*":
            result = st.session_state.previous_value * current_value
        elif st.session_state.operator == "/":
            if current_value == 0:
                show_for_error("Division by zero")
                return
            result = st.session_state.previous_value / current_value

        st.session_state.current_input = format_number(result)

        if intermediate:
            st.session_state.previous_value = result
        else:
            st.session_state.previous_value = None

    except ZeroDivisionError:
        show_for_error("Division by zero")
    except Exception:
        show_for_error("Error")

def show_for_error(message):
    st.session_state.error_state = True
    st.session_state.current_input = message
    st.session_state.history_text = ""

def on_button_click(char):
    if char == "C":
        clear_all()
        return

    if st.session_state.error_state:
        return

    if char in "0123456789":
        if st.session_state.reset_screen:
            st.session_state.current_input = char
            st.session_state.reset_screen = False
        else:
            if st.session_state.current_input == "0":
                st.session_state.current_input = char
            else:
                if len(st.session_state.current_input) < 14:
                    st.session_state.current_input += char

    elif char == ".":
        if st.session_state.reset_screen:
            st.session_state.current_input = "0."
            st.session_state.reset_screen = False
        elif "." not in st.session_state.current_input:
            st.session_state.current_input += "."

    elif char in "+-*/":
        if st.session_state.operator and not st.session_state.reset_screen:
            calculate(intermediate=True)
        else:
            try:
                st.session_state.previous_value = float(st.session_state.current_input)
            except ValueError:
                st.session_state.previous_value = 0.0
        
        st.session_state.operator = char
        st.session_state.reset_screen = True
        
        prev_str = format_number(st.session_state.previous_value)
        st.session_state.history_text = f"{prev_str} {st.session_state.operator}"

    elif char == "=":
        if st.session_state.operator and st.session_state.previous_value is not None:
            calculate(intermediate=False)
            st.session_state.operator = None
            st.session_state.history_text = ""
            st.session_state.reset_screen = True

# Main Calculator UI Layout inside card
st.markdown('<div class="calc-card">', unsafe_allow_html=True)

# Display Screen
display_text = get_display_string()
history_display = st.session_state.history_text
error_class = " calc-error" if st.session_state.error_state else ""

st.markdown(f"""
<div class="calc-display">
    <div class="calc-history">{history_display}</div>
    <div class="calc-result{error_class}">{display_text}</div>
</div>
""", unsafe_allow_html=True)

# Button grid definition
# Row 1: C (span 2), /, *
r1_c1, r1_c2, r1_c3 = st.columns([2, 1, 1])
with r1_c1:
    if st.button("C", key="btn_C", use_container_width=True):
        on_button_click("C")
        st.rerun()
with r1_c2:
    if st.button("/", key="btn_div", use_container_width=True):
        on_button_click("/")
        st.rerun()
with r1_c3:
    if st.button("*", key="btn_mul", use_container_width=True):
        on_button_click("*")
        st.rerun()

# Row 2: 7, 8, 9, -
r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1:
    if st.button("7", key="btn_7", use_container_width=True):
        on_button_click("7")
        st.rerun()
with r2_c2:
    if st.button("8", key="btn_8", use_container_width=True):
        on_button_click("8")
        st.rerun()
with r2_c3:
    if st.button("9", key="btn_9", use_container_width=True):
        on_button_click("9")
        st.rerun()
with r2_c4:
    if st.button("-", key="btn_sub", use_container_width=True):
        on_button_click("-")
        st.rerun()

# Row 3: 4, 5, 6, +
r3_c1, r3_c2, r3_c3, r3_c4 = st.columns(4)
with r3_c1:
    if st.button("4", key="btn_4", use_container_width=True):
        on_button_click("4")
        st.rerun()
with r3_c2:
    if st.button("5", key="btn_5", use_container_width=True):
        on_button_click("5")
        st.rerun()
with r3_c3:
    if st.button("6", key="btn_6", use_container_width=True):
        on_button_click("6")
        st.rerun()
with r3_c4:
    if st.button("+", key="btn_add", use_container_width=True):
        on_button_click("+")
        st.rerun()

# Row 4: 1, 2, 3, =
r4_c1, r4_c2, r4_c3, r4_c4 = st.columns(4)
with r4_c1:
    if st.button("1", key="btn_1", use_container_width=True):
        on_button_click("1")
        st.rerun()
with r4_c2:
    if st.button("2", key="btn_2", use_container_width=True):
        on_button_click("2")
        st.rerun()
with r4_c3:
    if st.button("3", key="btn_3", use_container_width=True):
        on_button_click("3")
        st.rerun()
with r4_c4:
    if st.button("=", key="btn_eq", use_container_width=True):
        on_button_click("=")
        st.rerun()

# Row 5: 0 (span 2), .
r5_c1, r5_c2, r5_c3 = st.columns([2, 1, 1])
with r5_c1:
    if st.button("0", key="btn_0", use_container_width=True):
        on_button_click("0")
        st.rerun()
with r5_c2:
    if st.button(".", key="btn_dot", use_container_width=True):
        on_button_click(".")
        st.rerun()
with r5_c3:
    # Empty placeholder to align grid correctly
    st.markdown("")

st.markdown('</div>', unsafe_allow_html=True)
