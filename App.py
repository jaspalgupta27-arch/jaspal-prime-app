import streamlit as st
import math
import time

st.set_page_config(page_title="Jaspal Gupta Prime Protocol", page_icon="🔐", layout="centered")

st.title("🔐 Local Prime Coordinate Locking Protocol")
st.write("An Absolute Algebraic Verification Method by **Jaspal Gupta**")
st.write("---")

# ==========================================
# शुद्ध जसपाल गुप्ता थ्योरम (बिना किसी सीव/मेमोरी ऐरे के)
# ==========================================
def jaspal_gupta_finder(N):
    start_time = time.perf_counter()
    
    # रेडिकल बाउंड्री
    d = math.isqrt(N) + 1
    
    locked_x = None
    # बिना किसी सीव ऐरे के सीधे लोकल कोऑर्डिनेट लॉक की जांच
    for x in range(1, d + 1):
        candidate = N + x
        is_pure_prime = True
        
        if candidate % 2 == 0:
            if candidate != 2:
                is_pure_prime = False
        else:
            # सीधे बाउंड्री चेकिंग बिना मेमोरी स्टोर किए
            max_check = math.isqrt(candidate)
            for p in range(3, max_check + 1, 2):
                if candidate % p == 0:
                    is_pure_prime = False
                    break
                    
        if is_pure_prime:
            locked_x = x
            break
            
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    return N + locked_x, locked_x, d, execution_time

# ==========================================
# मोबाइल यूआई (User Interface)
# ==========================================

anchor_str = st.text_input("यहाँ कोई भी बड़ा ईवन नंबर (Even Anchor N) डालें:", value="100000000")

if st.button("🔴 शुद्ध प्राइम नंबर खोजें"):
    try:
        anchor_input = int(anchor_str.strip())
        if anchor_input <= 2:
            st.error("कृपया 2 से बड़ी संख्या डालें!")
        elif anchor_input % 2 != 0:
            st.error("कृपया केवल सम संख्या (Even Number) ही डालें!")
        else:
            with st.spinner('लोकल ग्रिड पर गणना की जा रही है...'):
                pure_prime, offset_x, boundary_d, speed = jaspal_gupta_finder(anchor_input)
                
                st.success(f"🎯 शुद्ध प्राइम नंबर खोजा गया: **{pure_prime}**")
                
                st.write("### 📊 थ्योरम गणना विवरण (Technical Details)")
                st.info(f"✨ **उत्पन्न परिणाम:** यह संख्या 100% गारंटी के साथ एक शुद्ध अभाज्य (Pure Prime) संख्या है।")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("لॉक्ड कोऑर्डिनेट (Offset x)", f"{offset_x}")
                with col2:
                    st.metric("रेडिकल बाउंड्री (d)", f"{boundary_d}")
                    st.metric("गणना का समय (Speed)", f"{speed:.4f} ms")
                    
    except ValueError:
        st.error("कृपया केवल वैध अंक (Numbers) ही टाइप करें!")

st.write("---")
st.caption("🇮🇳 भारत सरकार पेटेंट पावती रसीद द्वारा संरक्षित | प्रोविशनल पेटेंट दर्ज")
