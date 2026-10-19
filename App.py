import streamlit as st
import math
import time
import random

st.set_page_config(page_title="Jaspal Gupta Prime Protocol", page_icon="🔐", layout="centered")
st.title("🔐 Local Prime Coordinate Locking Protocol")
st.write("An Absolute Algebraic Verification Method by **Jaspal Gupta**")
st.write("---")

def jaspal_gupta_finder(N):
    start_time = time.perf_counter()
    d = math.floor(math.sqrt(N)) + 1
    sieve = [True] * (d + 1)
    for p in range(2, int(math.sqrt(d)) + 1):
        if sieve[p]:
            for i in range(p*p, d + 1, p):
                sieve[i] = False
    small_primes = [p for p in range(2, d + 1) if sieve[p]]
    p_core = []
    p_free = {}
    for p in small_primes:
        remainder = N % p
        if remainder == 0:
            p_core.append(p)
        else:
            p_free[p] = remainder
    locked_x = None
    for x in range(1, d + 1):
        is_locked = True
        for c in p_core:
            if x % c == 0:
                is_locked = False
                break
        if not is_locked: continue
        for p, r_p in p_free.items():
            if x % p == (p - r_p):
                is_locked = False
                break
        if is_locked:
            locked_x = x
            break
    end_time = time.perf_counter()
    return N + locked_x, locked_x, (end_time - start_time) * 1000

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

anchor_input = st.number_input("यहाँ कोई भी बड़ा ईवन नंबर (Even Anchor N) डालें:", min_value=100, max_value=1000000000000, value=100000000, step=2)

if st.button("🔴 लाइव टेस्ट मुकाबला शुरू करें"):
    if anchor_input % 2 != 0:
        st.error("कृपया केवल सम संख्या (Even Number) ही डालें!")
    else:
        with st.spinner('गणना की जा रही है...'):
            prime_gupta, offset_x, time_gupta = jaspal_gupta_finder(anchor_input)
            prime_miller, time_miller = miller_rabin_finder(anchor_input)
            st.success(f"🎯 शुद्ध प्राइम नंबर खोजा गया: **{prime_gupta}** (कोऑर्डिनेट Offset x = {offset_x})")
            st.write("### ⏱️ गति का मुकाबला (Speed Comparison)")
            col1, col2 = st.columns(2)
            with col1: st.metric("जसपाल गुप्ता थ्योरम", f"{time_gupta:.4f} ms", "100% अचूक")
            with col2: st.metric("मिलर-रैबिन टेस्ट", f"{time_miller:.4f} ms", "संभावित")
            st.write("---")
            if time_gupta < time_miller:
                time_saved = time_miller - time_gupta
                percent_saved = (time_saved / time_miller) * 100
                st.balloons()
                st.info(f"🏆 **परिणाम:** जसपाल गुप्ता थ्योरम ने मिलर-रैबिन से **{time_saved:.4f} मिलीसेकंड ({percent_saved:.2f}%) कम समय लिया!**")
            else:
                st.warning("इस रेंज पर मिलर-रैबिन की गति अधिक रही, परन्तु जसपाल गुप्ता प्रोटोकॉल 100% सटीक (Deterministic) रहा।")

st.write("---")
st.caption("🇮🇳 भारत सरकार पेटेंट पावती रसीद द्वारा संरक्षित | प्रोविशनल पेटेंट दर्ज")
