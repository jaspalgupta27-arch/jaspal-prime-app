import streamlit as st
import math
import time
import random

st.set_page_config(page_title="Jaspal Gupta Prime Protocol", page_icon="🔐", layout="centered")

st.title("🔐 Local Prime Coordinate Locking Protocol")
st.write("An Absolute Algebraic Verification Method by **Jaspal Gupta**")
st.write("---")

# ==========================================
# 1. शुद्ध जसपाल गुप्ता थ्योरम (नो सीव, नो मेमोरी एरर)
# ==========================================
def jaspal_gupta_finder(N):
    start_time = time.perf_counter()
    d = math.isqrt(N) + 1
    
    locked_x = None
    for x in range(1, d + 1):
        candidate = N + x
        is_pure_prime = True
        
        if candidate % 2 == 0:
            if candidate != 2:
                is_pure_prime = False
        else:
            max_check = math.isqrt(candidate)
            for p in range(3, max_check + 1, 2):
                if candidate % p == 0:
                    is_pure_prime = False
                    break
                    
        if is_pure_prime:
            locked_x = x
            break
            
    end_time = time.perf_counter()
    return N + locked_x, locked_x, d, (end_time - start_time) * 1000

# ==========================================
# 2. मिलर-रैबिन टेस्ट (समान संख्या पर जांच हेतु)
# ==========================================
def miller_rabin_check(n, k=40):
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def miller_rabin_finder(N):
    start_time = time.perf_counter()
    candidate = N + 1
    while True:
        if miller_rabin_check(candidate):
            end_time = time.perf_counter()
            return candidate, (end_time - start_time) * 1000
        candidate += 1

# ==========================================
# मोबाइल यूआई (User Interface)
# ==========================================

anchor_str = st.text_input("यहाँ कोई भी बड़ा ईवन नंबर (Even Anchor N) डालें:", value="50000000000000000")

if st.button("🔴 लाइव टेस्ट मुकाबला शुरू करें"):
    try:
        anchor_input = int(anchor_str.strip())
        if anchor_input <= 2:
            st.error("कृपया 2 से बड़ी संख्या डालें!")
        elif anchor_input % 2 != 0:
            st.error("कृपया केवल सम संख्या (Even Number) ही डालें!")
        else:
            with st.spinner('ग्रिड पर लाइव मुकाबला चल रहा है...'):
                pure_prime, offset_x, boundary_d, time_gupta = jaspal_gupta_finder(anchor_input)
                _, time_miller = miller_rabin_finder(anchor_input)
                
                st.success(f"🎯 शुद्ध प्राइम नंबर खोजा गया: **{pure_prime}** (कोऑर्डिनेट Offset x = {offset_x})")
                
                st.write("### ⏱ *गति का मुकाबला (Speed Comparison)*")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("जसपाल गुप्ता थ्योरम", f"{time_gupta:.4f} ms", "100% अचूक")
                with col2:
                    st.metric("मिलर-रैबिन टेस्ट", f"{time_miller:.4f} ms", "संभावित")
                
                st.write("---")
                if time_gupta < time_miller:
                    time_saved = time_miller - time_gupta
                    percent_saved = (time_saved / time_miller) * 100
                    st.balloons()
                    st.info(f"🏆 **परिणाम:** जसपाल गुप्ता थ्योरम ने मिलर-रैबिन से **{time_saved:.4f} मिलीसेकंड ({percent_saved:.2f}%) कम समय लिया!**")
                else:
                    time_diff = time_gupta - time_miller
                    st.warning(f"इस विशिष्ट मान पर मिलर-रैबिन {time_diff:.4f} ms तेज़ रहा, परन्तु जसपाल गुप्ता प्रोटोकॉल 100% सटीक (Deterministic) साबित हुआ।")
                    
    except ValueError:
        st.error("कृपया केवल वैध अंक (Numbers) ही टाइप करें!")

st.write("---")
st.caption("🇮🇳 भारत सरकार पेटेंट पावती रसीद द्वारा संरक्षित | प्रोविशनल पेटेंट दर्ज")
