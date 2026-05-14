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
        border: 2px solid #008000;
        padding: 20px;
        border-radius: 15px;
    }
    [data-testid="stMetricLabel"] {
        color: #008000 !important; /* Label ကို အဝါရောင် */
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        color: #008000 !important; /* ကိန်းဂဏန်းကို အဖြူရောင် */
    }

    /* Info & Success Boxes */
    .stAlert {
        background-color: #008000 !important; /* အစိမ်းရောင်နောက်ခံ */
        color: #000000 !important; /* အနက်ရောင်စာသား */
    }

    /* Input Labels */
    label, p, span {
        color: #FFFFFF !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #008000 !important;
        color: #000000 !important;
        border-radius: 10px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper Function: Time Conversion ---
def convert_to_time(remaining_apples):
    if remaining_apples <= 0: return "သင်ဟာ လွတ်မြောက်ပါပြီ"
    days = int(remaining_apples)
    years = days // 365
    months = (days % 365) // 30
    final_days = (days % 365) % 30
    res = []
    if years: res.append(f"{years} နှစ်")
    if months: res.append(f"{months} လ")
    if final_days: res.append(f"{final_days} ရက်")
    return " ".join(res)

st.title("🍎 အကျဉ်းသားပြစ်ဒဏ်ကျခံမှု လွတ်မြောက်မည့်ရက်တွက်ချက်ခြင်းစနစ် (Final Logic)")

# --- ၁။ Inputs Section ---
with st.container():
    target = st.number_input("စုစုပေါင်း ကျခံရမည့်ပြစ်ဒဏ် (Target)", value=3650)
    col1, col2, col3 = st.columns(3)
    with col1:
        f1_s = st.date_input("အချုပ်တွင်ပြစ်ဒဏ်စတင်ကျခံသည့်ရက်စွဲ", datetime(2024, 1, 1), key="f1s")
        f1_e = st.date_input("	အချုပ်တွင်ပြစ်ဒဏ်ကျခံမှု ပြီးဆုံးသည့်ရက်စွဲ", datetime(2024, 2, 1), key="f1e")
    with col2:
        f2_s = st.date_input("‌ထောင်တွင်ပြစ်ဒဏ်စတင်ကျခံသည့်ရက်စွဲ", datetime(2024, 6, 1), key="f2s")
        f2_e = st.date_input("‌ထောင်တွင်ပြစ်ဒဏ်ကျခံမှု ပြီးဆုံးသည့်ရက်စွဲ", datetime(2024, 12, 31), key="f2e")
    with col3:
        f3_s = st.date_input("ရဲဘက်စခန်းတွင် ပြစ်ဒဏ်စတင်ကျခံသည့် ရက်စွဲ", datetime(2025, 1, 1), key="f3s")
        f3_e = st.date_input("ရဲဘက်စခန်းတွင် ပြစ်ဒဏ်ကျခံမှု ပြီးဆုံးသည့်ရက်စွဲ", datetime(2025, 3, 1), key="f3e")

# --- ၂။ Lucky Draws ---
st.markdown("### 🎡 လွတ်ငြိမ်းသက်သာမှုပေးသည့်ရက်စွဲများ")
if 'lucky_draws' not in st.session_state:
    st.session_state.lucky_draws = []

col_b1, col_b2 = st.columns([1, 5])
with col_b1:
    if st.button("➕ လွတ်ငြိမ်းချမ်းသာပေးသည့်ရက်စွဲထည့်ပါ"): st.session_state.lucky_draws.append({"date": datetime.now().date(), "type": "မူလပြစ်ဒဏ်၏ ၁/၄"})
with col_b2:
    if st.button("🗑️ ပြန်လည်တွက်ချက်မည်"): st.session_state.lucky_draws = []

lucky_data_map = {}
for i, ld in enumerate(st.session_state.lucky_draws):
    c1, c2 = st.columns([1, 2])
    with c1:
        new_date = st.date_input(f"ရက်စွဲ {i+1}", value=ld['date'], key=f"ld_date_{i}")
    with c2:
        new_type = st.selectbox(f"အမျိုးအစား {i+1}", ["မူလပြစ်ဒဏ်၏ ၁/၄", "မူလပြစ်ဒဏ်၏ ၁/၆", "ကျန်ရှိသောပြစ်ဒဏ်၏ ၁/၄", "ကျန်ရှိသောပြစ်ဒဏ်၏ ၁/၆"], key=f"ld_type_{i}")
    lucky_data_map[new_date.strftime('%Y-%m-%d')] = new_type

# --- ၃။ Calculation Logic ---
if st.button("အတည်ပြုပါသည်။ တွက်ချက်မည်။", use_container_width=True):
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
            if l_type == "မူလပြစ်ဒဏ်၏ ၁/၄": added = target / 4
            elif l_type == "မူလပြစ်ဒဏ်၏ ၁/၆": added = target / 6
            elif l_type == "ကျန်ရှိသောပြစ်ဒဏ်၏ ၁/၄": added = current_rem / 4
            elif l_type == "ကျန်ရှိသောပြစ်ဒဏ်၏ ၁/၆": added = current_rem / 6
            total += added
            breakdown_notes.append(f"🎡 **{d_str}** - {l_type} အရ ({round(added, 2)} ရက်) ပေါင်းထည့်ခဲ့သည်။")

        # Regular Bonuses
        if (curr + timedelta(days=1)).month != curr.month and curr.month != f2_s.month: total += 4
        if curr > f2_s and curr.month == f2_s.month and curr.day == f2_s.day: total += 15
        
        # Quarterly Bonus Logic
        if curr >= stage_info['bonus_start']:
            if stage_info['days_counter'] == 0:
                stage_info['stage'] += 1
                b_amt = 11 if stage_info['stage'] == 1 else (20 if stage_info['stage'] == 2 else 29)
                total += b_amt
                breakdown_notes.append(f"📅 **{d_str}** - ၃ လပတ်အပိုဆု (Stage {stage_info['stage']}) အဖြစ် **{b_amt} ရက်** ရရှိသည်။")
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
            
            # Lucky Draw logic (Sync with UI strings)
            if d_str in lucky_data_map:
                l_type = lucky_data_map[d_str]
                current_rem = max(0, target - total)
                added = (target/4 if l_type=="မူလပြစ်ဒဏ်၏ ၁/၄" else target/6 if l_type=="မူလပြစ်ဒဏ်၏ ၁/၆" else current_rem/4 if l_type=="ကျန်ရှိသောပြစ်ဒဏ်၏ ၁/၄" else current_rem/6)
                total += added
                breakdown_notes.append(f"🎡 **{d_str}** - {l_type} အရ ({round(added, 2)} ရက်) ပေါင်းထည့်ခဲ့သည်။")
            
            # Monthly Bonus for Farm 3 (ရောက်တဲ့လကစပြီး ၅ ရက်ပေးရန် ပြင်ဆင်ထားသည်)
            if (curr + timedelta(days=1)).month != curr.month:
                total += 5
                breakdown_notes.append(f"📅 **{d_str}** - ရဲဘက်စခန်း လစဉ်လျှော့ရက် ၅ ရက် ရရှိသည်။")

            # Continue Quarterly Bonus in Farm 3
            if curr >= stage_info['bonus_start']:
                if stage_info['days_counter'] == 0:
                    stage_info['stage'] += 1
                    b_amt = 11 if stage_info['stage'] == 1 else (20 if stage_info['stage'] == 2 else 29)
                    total += b_amt
                    breakdown_notes.append(f"📅 **{d_str}** - ၃ လပတ်အပိုဆု (Stage {stage_info['stage']}) အဖြစ် **{b_amt} ရက်** ရရှိသည်။")
                stage_info['days_counter'] = (stage_info['days_counter'] + 1) % 90
            
            if total >= target: break
            curr += timedelta(days=1)

    # --- Results Display ---
    st.markdown("---")
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.metric("စုစုပေါင်းရရှိပြီး", f"{round(total, 2)} ရက်")
    with c_res2:
        st.metric("လိုအပ်ချက်", f"{max(0, round(target - total, 2))} ရက်")
    
    st.success(f"⏳ **ကျန်ရှိချိန်ခန့်မှန်းခြေ:** {convert_to_time(target - total)}")
    st.progress(min(1.0, total/target))

    # --- ၄။ Detailed Breakdown ---
    st.markdown("### 🔍 တွက်ချက်မှုဆိုင်ရာ အသေးစိတ်မှတ်ချက်")
    with st.container():
        st.write(f"✅ **နေ့စဉ်ပြစ်ဒဏ်ကျခံခြင်း:** အချုပ်တွင် **{f1_res}** ရက် ရရှိခဲ့သည်။")
        if f3_s:
            st.write(f"✅ **နေရာအကူးအပြောင်း:** ရဲဘက်စခန်းသို့ ရောက်ရှိသဖြင့် အပိုဆု **၅ ရက်** ပေါင်းထည့်ထားသည်။")
        
        st.write("✅ **အပိုဆုနှင့် လျှော့ရက်များနှင့် လွတ်ငြိမ်းချမ်းသာပေးသည့်ရက်စွဲများ တွက်ချက်ပုံ:**")
        for note in breakdown_notes:
            st.write(f"- {note}")
