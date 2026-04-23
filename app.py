import streamlit as st
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="Apple Tracker Pro", page_icon="🍎", layout="wide")

# --- UI Styling (Contrast Fix) ---
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #0B1E3E;
        color: #FFFFFF;
    }
    
    /* Metrics Styling - အပြာပေါ်မှာ အဖြူ / အဝါပေါ်မှာ အနက် */
    [data-testid="stMetric"] {
        background-color: #162B4E;
        border: 2px solid #FFD700;
        padding: 20px;
        border-radius: 15px;
    }
    [data-testid="stMetricLabel"] {
        color: #FFD700 !important; /* Label ကို အဝါရောင် */
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important; /* ကိန်းဂဏန်းကို အဖြူရောင် */
    }

    /* Info & Success Boxes */
    .stAlert {
        background-color: #FFD700 !important; /* အဝါရောင်နောက်ခံ */
        color: #000000 !important; /* အနက်ရောင်စာသား */
    }

    /* Input Labels */
    label, p, span {
        color: #FFFFFF !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border-radius: 10px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper Function: Time Conversion ---
def convert_to_time(remaining_apples):
    if remaining_apples <= 0: return "ရည်မှန်းချက်ပြည့်သွားပါပြီ"
    days = int(remaining_apples)
    years = days // 365
    months = (days % 365) // 30
    final_days = (days % 365) % 30
    res = []
    if years: res.append(f"{years} နှစ်")
    if months: res.append(f"{months} လ")
    if final_days: res.append(f"{final_days} ရက်")
    return " ".join(res)

st.title("🍎 ပန်းသီးစုဆောင်းမှု တွက်ချက်ခြင်းစနစ် (Final Logic)")

# --- ၁။ Inputs Section ---
with st.container():
    target = st.number_input("စုစုပေါင်း ရည်မှန်းချက် (Target)", value=3650)
    col1, col2, col3 = st.columns(3)
    with col1:
        f1_s = st.date_input("ပထမခြံ စတင်ရက်", datetime(2024, 1, 1), key="f1s")
        f1_e = st.date_input("ပထမခြံ ပြီးဆုံးရက်", datetime(2024, 2, 1), key="f1e")
    with col2:
        f2_s = st.date_input("ဒုတိယခြံ စတင်ရက်", datetime(2024, 6, 1), key="f2s")
        f2_e = st.date_input("ဒုတိယခြံ ပြီးဆုံးရက်", datetime(2024, 12, 31), key="f2e")
    with col3:
        f3_s = st.date_input("တတိယခြံ စတင်ရက်", datetime(2025, 1, 1), key="f3s")
        f3_e = st.date_input("တတိယခြံ ပြီးဆုံးရက်", datetime(2025, 3, 1), key="f3e")

# --- ၂။ Lucky Draws ---
st.markdown("### 🎡 ကံစမ်းမဲရက်စွဲများ")
if 'lucky_draws' not in st.session_state:
    st.session_state.lucky_draws = []

col_b1, col_b2 = st.columns([1, 5])
with col_b1:
    if st.button("➕ ရက်စွဲသစ်"): st.session_state.lucky_draws.append({"date": datetime.now().date(), "type": "မူလရည်မှန်းချက်၏ ၁/၄"})
with col_b2:
    if st.button("🗑️ အားလုံးဖျက်"): st.session_state.lucky_draws = []

lucky_data_map = {}
for i, ld in enumerate(st.session_state.lucky_draws):
    c1, c2 = st.columns([1, 2])
    with c1:
        new_date = st.date_input(f"ရက်စွဲ {i+1}", value=ld['date'], key=f"ld_date_{i}")
    with c2:
        new_type = st.selectbox(f"အမျိုးအစား {i+1}", ["မူလရည်မှန်းချက်၏ ၁/၄", "မူလရည်မှန်းချက်၏ ၁/၆", "ကျန်ရှိသောပမာဏ၏ ၁/၄", "ကျန်ရှိသောပမာဏ၏ ၁/၆"], key=f"ld_type_{i}")
    lucky_data_map[new_date.strftime('%Y-%m-%d')] = new_type

# --- ၃။ Calculation Logic (With Stage Logic restored) ---
if st.button("ရလဒ်များကို တွက်ချက်မည်", use_container_width=True):
    total = 0
    breakdown_notes = []
    
    # Farm 1
    f1_res = (f1_e - f1_s).days + 1
    total += f1_res
    
    # Bonus/Stage Setup
    stage_info = {'bonus_start': f2_s if 1 <= f2_s.day <= 7 else f2_s + timedelta(days=90), 'stage': 0, 'days_counter': 0}
    
    # Farm 2 Logic
    curr = f2_s
    while curr <= f2_e:
        total += 1
        d_str = curr.strftime('%Y-%m-%d')
        
        # Lucky Draw logic
        if d_str in lucky_data_map:
            l_type = lucky_data_map[d_str]
            current_rem = max(0, target - total)
            added = 0
            if l_type == "မူလရည်မှန်းချက်၏ ၁/၄": added = target / 4
            elif l_type == "မူလရည်မှန်းချက်၏ ၁/၆": added = target / 6
            elif l_type == "ကျန်ရှိသောပမာဏ၏ ၁/၄": added = current_rem / 4
            elif l_type == "ကျန်ရှိသောပမာဏ၏ ၁/၆": added = current_rem / 6
            total += added
            breakdown_notes.append(f"🎡 **{d_str}** - {l_type} အရ ({round(added, 2)} လုံး) ပေါင်းထည့်ခဲ့သည်။ (ထိုစဉ်က ကျန်ရှိပမာဏ: {round(current_rem, 2)})")

        # Regular Bonuses
        if (curr + timedelta(days=1)).month != curr.month and curr.month != f2_s.month: total += 4
        if curr > f2_s and curr.month == f2_s.month and curr.day == f2_s.day: total += 15
        
        # Quarterly Bonus Logic (RESTORED)
        if curr >= stage_info['bonus_start']:
            if stage_info['days_counter'] == 0:
                stage_info['stage'] += 1
                b_amt = 11 if stage_info['stage'] == 1 else (20 if stage_info['stage'] == 2 else 29)
                total += b_amt
                breakdown_notes.append(f"📅 **{d_str}** - ၃ လပတ်အပိုဆု (Stage {stage_info['stage']}) အဖြစ် **{b_amt} လုံး** ရရှိသည်။")
            stage_info['days_counter'] = (stage_info['days_counter'] + 1) % 90
            
        if total >= target: break
        curr += timedelta(days=1)

    # Farm 3 Logic
    if total < target:
        total += 5
        curr = f3_s
        while curr <= f3_e:
            total += 1
            d_str = curr.strftime('%Y-%m-%d')
            if d_str in lucky_data_map:
                l_type = lucky_data_map[d_str]
                current_rem = max(0, target - total)
                added = (target/4 if l_type=="မူလရည်မှန်းချက်၏ ၁/၄" else target/6 if l_type=="မူလရည်မှန်းချက်၏ ၁/၆" else current_rem/4 if l_type=="ကျန်ရှိသောပမာဏ၏ ၁/၄" else current_rem/6)
                total += added
                breakdown_notes.append(f"🎡 **{d_str}** - {l_type} အရ ({round(added, 2)} လုံး) ပေါင်းထည့်ခဲ့သည်။")
            
            # Continue Quarterly Bonus in Farm 3
            if curr >= stage_info['bonus_start']:
                if stage_info['days_counter'] == 0:
                    stage_info['stage'] += 1
                    b_amt = 11 if stage_info['stage'] == 1 else (20 if stage_info['stage'] == 2 else 29)
                    total += b_amt
                    breakdown_notes.append(f"📅 **{d_str}** - ၃ လပတ်အပိုဆု (Stage {stage_info['stage']}) အဖြစ် **{b_amt} လုံး** ရရှိသည်။")
                stage_info['days_counter'] = (stage_info['days_counter'] + 1) % 90
            if total >= target: break
            curr += timedelta(days=1)

    # --- Results Display ---
    st.markdown("---")
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.metric("စုစုပေါင်းရရှိပြီး", f"{round(total, 2)} လုံး")
    with c_res2:
        st.metric("လိုအပ်ချက်", f"{max(0, round(target - total, 2))} လုံး")
    
    st.success(f"⏳ **ကျန်ရှိချိန်ခန့်မှန်းခြေ:** {convert_to_time(target - total)}")
    st.progress(min(1.0, total/target))

    # --- ၄။ Detailed Breakdown (Updated) ---
    st.markdown("### 🔍 တွက်ချက်မှုဆိုင်ရာ အသေးစိတ်မှတ်ချက်")
    with st.container():
        st.write(f"✅ **နေ့စဉ်စုဆောင်းမှု:** ပထမခြံတွင် **{f1_res}** လုံး ရရှိခဲ့သည်။")
        if total >= target + 5 or f3_s:
            st.write(f"✅ **ခြံအကူးအပြောင်း:** တတိယခြံသို့ ရောက်ရှိသဖြင့် အပိုဆု **၅ လုံး** ပေါင်းထည့်ထားသည်။")
        
        st.write("✅ **အပိုဆုနှင့် ကံစမ်းမဲများ တွက်ချက်ပုံ:**")
        for note in breakdown_notes:
            st.write(f"- {note}")
        
        st.markdown(f"""
        > **တွက်ချက်ပုံ ရှင်းလင်းချက်:**
        > * **ကျန်ရှိသောပမာဏ၏ ၁/၄ သို့မဟုတ် ၁/၆:** တွက်ချက်သည့်ရက်စွဲတွင် (Target {target} - ထိုနေ့အထိရရှိထားသော ပမာဏ) ကို ရှာဖွေပြီး ၄ သို့မဟုတ် ၆ နှင့် စားခြင်းဖြစ်ပါသည်။
        > * **Stage Bonus (၃ လပတ်):** ဒုတိယခြံစတင်ချိန်မှ ရက်ပေါင်း ၉၀ တိုင်းတွင် Stage အလိုက် (၁၁၊ ၂၀၊ ၂၉) လုံး ပေါင်းထည့်ပါသည်။ (လက်ရှိ Stage {stage_info['stage']} အထိ တွက်ချက်ပြီး)
        """)