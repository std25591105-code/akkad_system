import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="منصة رؤيا برو 2026", page_icon="💎", layout="wide")

# --- نظام التصميم Ultra Clear (حل مشكلة وضوح الكتابة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    /* خلفية داكنة فخمة مع نص أبيض ناصع للوضوح العالي */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* كروت الوظائف بتباين عالي جداً */
    .card {
        background: #1d2129; padding: 25px; border-radius: 15px;
        border-right: 8px solid #d4af37; /* لمسة ذهبية */
        box-shadow: 0 4px 20px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    
    /* جعل العناوين واضحة جداً */
    h1, h2, h3 { color: #d4af37 !important; font-weight: 900; }
    p, b, span { color: #e0e0e0 !important; font-size: 18px; }
    
    /* الأزرار - لون ذهبي ملكي ونص أسود للوضوح */
    .stButton>button {
        width: 100%; border-radius: 12px; background: #d4af37;
        color: #000000 !important; font-weight: bold; border: none; 
        padding: 15px; font-size: 20px; transition: 0.3s;
    }
    .stButton>button:hover { background: #fff; color: #000; transform: translateY(-3px); }

    /* صناديق الإحصائيات */
    .stat-box {
        background: #1d2129; padding: 20px; border-radius: 15px;
        text-align: center; border: 1px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الربط الذكي بالداتابيس ---
@st.cache_resource
def init_connection():
    try: return create_client(st.secrets["URL"], st.secrets["KEY"])
    except: return None

supabase = init_connection()

# --- القائمة الجانبية (إضافات ذكية 100%) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = [
        "🏠 الواجهة الذهبية", 
        "🔍 البحث الذكي المطور", 
        "📝 استمارة التقديم (ذكور/إناث)", 
        "🏢 إضافة عرض عمل للشركات", 
        "📊 الإحصائيات الحية",
        "🔐 لوحة تحكم المدير"
    ]
    choice = st.radio("القائمة الإدارية:", menu)
    st.write("---")
    st.markdown("📍 **الموقع:** العراق - بابل")

# --- 1. الواجهة الذهبية ---
if choice == "🏠 الواجهة الذهبية":
    st.markdown("<h1 style='text-align: center;'>مستقبل التوظيف بين يديك</h1>", unsafe_allow_html=True)
    
    # جلب الأرقام الحقيقية
    try:
        j_n = len(supabase.table("Jobs").select("id").execute().data)
        a_n = len(supabase.table("application").select("id").execute().data)
    except: j_n, a_n = 0, 0

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-box"><h3>💼 {j_n}</h3><p>وظيفة منشورة</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><h3>👥 {a_n}</h3><p>باحث عن عمل</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="stat-box"><h3>⭐ 100%</h3><p>ثقة وأمان</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("🔥 آخر الفرص العاجلة")
    col_a, col_b = st.columns(2)
    col_a.markdown('<div class="card"><h3>مدير تسويق</h3><p>شركة الفارس | الراتب: 1,200,000 د.ع</p></div>', unsafe_allow_html=True)
    col_b.markdown('<div class="card"><h3>مندوب مبيعات</h3><p>مكتب بابل | الراتب: 750,000 د.ع</p></div>', unsafe_allow_html=True)

# --- 2. البحث الذكي (محرك بحث قوي) ---
elif choice == "🔍 البحث الذكي المطور":
    st.title("🔍 ابحث عن حلمك")
    search = st.text_input("ابحث بالعنوان، اسم الشركة، أو الراتب...")
    
    if supabase:
        res = supabase.table("Jobs").select("*").execute()
        if res.data:
            # فلترة فورية
            df = pd.DataFrame(res.data)
            filtered = [j for j in res.data if search.lower() in j['title'].lower() or search.lower() in j['company'].lower()] if search else res.data
            
            for job in filtered:
                st.markdown(f"""
                <div class="card">
                    <h2>{job['title']}</h2>
                    <p>🏢 <b>الشركة:</b> {job['company']} | 💰 <b>الراتب:</b> {job['salary']}</p>
                    <p>📝 <b>المتطلبات:</b> {job['details']}</p>
                </div>
                """, unsafe_allow_html=True)

# --- 3. استمارة التقديم (إضافة الجنس والعمر والسكن) ---
elif choice == "📝 استمارة التقديم (ذكور/إناث)":
    st.title("📝 استمارة التوظيف الرسمية")
    with st.form("apply_pro"):
        c1, c2 = st.columns(2)
        name = c1.text_input("الأسم الرباعي")
        phone = c2.text_input("رقم الهاتف")
        
        g1, g2, g3 = st.columns(3)
        gender = g1.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
        age = g2.number_input("العمر", 18, 60)
        city = g3.text_input("منطقة السكن")
        
        edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "ماجستير/دكتوراه"])
        skills = st.text_area("تكلم عن خبراتك ومهاراتك")
        
        if st.form_submit_button("إرسال الطلب الآن"):
            if name and phone:
                try:
                    full_data = f"الجنس: {gender} | العمر: {age} | السكن: {city} | التعليم: {edu} | الخبرة: {skills}"
                    supabase.table("application").insert({"name": name, "phone": phone, "skills": full_data}).execute()
                    st.balloons()
                    st.success("تم إرسال طلبك بنجاح!")
                except: st.error("تأكد من إعدادات الجدول (RLS disabled)")

# --- 4. لوحة التحكم (إدارة ذكية) ---
elif choice == "🔐 لوحة تحكم المدير":
    if st.text_input("أدخل الرمز السري", type="password") == "roya2026":
        st.write("### 👥 قائمة المتقدمين")
        apps = supabase.table("application").select("*").execute()
        st.dataframe(pd.DataFrame(apps.data), use_container_width=True)
        
        st.write("---")
        st.write("### 💼 إدارة الوظائف")
        jobs = supabase.table("Jobs").select("*").execute()
        st.table(pd.DataFrame(jobs.data))
