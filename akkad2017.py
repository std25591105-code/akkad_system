import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="منصة رؤيا للتوظيف الدولية", page_icon="💎", layout="wide")

# --- تصميم الفخامة المطلقة (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    .stApp { background: #f4f7f6; }
    
    /* تصميم الكروت الملكية */
    .card {
        background: white; padding: 25px; border-radius: 20px;
        border-right: 12px solid #002d62; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 25px; transition: 0.4s;
    }
    .card:hover { transform: scale(1.01); border-right: 12px solid #d4af37; }
    
    /* أزرار فخمة جداً */
    .stButton>button {
        width: 100%; border-radius: 15px; background: linear-gradient(90deg, #002d62, #0056b3);
        color: #fff !important; font-weight: bold; border: none; padding: 15px; font-size: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* العناوين */
    h1, h2, h3 { color: #002d62; font-weight: 900; }
    
    /* شريط التجانب */
    .stat-box {
        background: white; padding: 20px; border-radius: 15px; text-align: center;
        border-bottom: 5px solid #d4af37; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- الربط الذكي بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try: return create_client(st.secrets["URL"], st.secrets["KEY"])
    except: return None

supabase = init_connection()

# --- القائمة الجانبية (أكثر من 10 أقسام ذكية) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #002d62;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = [
        "🌐 بوابة القيادة", 
        "🔍 البحث المتقدم", 
        "📝 تقديم طلب احترافي", 
        "🏢 إضافة وظيفة (للشركات)", 
        "📊 مركز البيانات الإداري",
        "⚖️ شروط الاستخدام"
    ]
    choice = st.radio("اختر الوجهة:", menu)
    st.write("---")
    st.info("🕒 نظام رؤيا الموحد - بابل 2026")

# --- 1. بوابة القيادة (الرئيسية) ---
if choice == "🌐 بوابة القيادة":
    st.markdown("<h1 style='text-align: center;'>المنصة الوطنية للتوظيف الذكي</h1>", unsafe_allow_html=True)
    
    # إحصائيات حية من الداتابيس
    try:
        j_data = len(supabase.table("Jobs").select("id").execute().data)
        a_data = len(supabase.table("application").select("id").execute().data)
    except: j_data, a_data = 0, 0

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="stat-box"><h2>{j_data}</h2><p>فرصة متاحة</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="stat-box"><h2>{a_data}</h2><p>باحث عن عمل</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="stat-box"><h2>بابل</h2><p>المقر الرئيسي</p></div>', unsafe_allow_html=True)
    col4.markdown('<div class="stat-box"><h2>100%</h2><p>آمن وموثوق</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("📢 وظائف عاجلة ومميزة")
    c_a, c_b = st.columns(2)
    c_a.markdown('<div class="card"><h3>مدير مبيعات</h3><p>شركة بابل القابضة | الراتب: 2 مليون</p></div>', unsafe_allow_html=True)
    c_b.markdown('<div class="card"><h3>محاسب مالي</h3><p>مكتب الرواد | الراتب: 800 ألف</p></div>', unsafe_allow_html=True)

# --- 2. البحث المتقدم (فلاتر ذكية) ---
elif choice == "🔍 البحث المتقدم":
    st.title("🔍 ابحث بذكاء عن مستقبلك")
    q = st.text_input("ادخل المسمى الوظيفي أو اسم الشركة...")
    type_work = st.multiselect("تصنيف العمل", ["دوام كامل", "دوام جزئي", "عن بعد", "عقود"])
    
    if supabase:
        res = supabase.table("Jobs").select("*").execute()
        if res.data:
            data = [j for j in res.data if q.lower() in j['title'].lower()] if q else res.data
            for j in data:
                st.markdown(f"""
                <div class="card">
                    <h2>{j['title']}</h2>
                    <p><b>🏢 الشركة:</b> {j['company']} | <b>💰 الراتب:</b> {j['salary']}</p>
                    <p><b>📜 التفاصيل:</b> {j['details']}</p>
                </div>
                """, unsafe_allow_html=True)

# --- 3. تقديم طلب احترافي (إضافات Gender/Age/City) ---
elif choice == "📝 تقديم طلب احترافي":
    st.title("📝 استمارة التوظيف الإلكترونية")
    with st.form("main_apply", clear_on_submit=True):
        st.subheader("📌 المعلومات الأساسية")
        f1, f2 = st.columns(2)
        name = f1.text_input("الأسم الرباعي")
        phone = f2.text_input("رقم الهاتف")
        
        st.subheader("👥 التفاصيل الشخصية")
        g1, g2, g3 = st.columns(3)
        gender = g1.selectbox("الجنس", ["ذكر", "أنثى"])
        age = g2.number_input("العمر", 18, 65)
        city = g3.text_input("منطقة السكن")
        
        st.subheader("🎓 المؤهلات والخبرات")
        edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "ماجستير/دكتوراه"])
        exp = st.text_area("تكلم عن مهاراتك وسنوات خبرتك بالتفصيل")
        
        if st.form_submit_button("إرسال الطلب رسمياً"):
            if name and phone:
                try:
                    full_skills = f"الجنس: {gender} | العمر: {age} | السكن: {city} | التعليم: {edu} | الخبرة: {exp}"
                    supabase.table("application").insert({"name": name, "phone": phone, "skills": full_skills}).execute()
                    st.balloons()
                    st.success("تم تسجيل طلبك بنجاح في قاعدة بيانات شركة رؤيا.")
                except: st.error("تأكد من إعدادات سوبابيس (Disable RLS)")

# --- 4. إضافة وظيفة (بوابة الشركات) ---
elif choice == "🏢 إضافة وظيفة (للشركات)":
    st.title("🏢 بوابة أصحاب الشركات والمكاتب")
    with st.form("add_job"):
        t = st.text_input("عنوان الوظيفة")
        c = st.text_input("اسم شركتك")
        s = st.text_input("الراتب")
        d = st.text_area("الشروط والمؤهلات المطلوبة")
        if st.form_submit_button("نشر الوظيفة الآن"):
            supabase.table("Jobs").insert({"title": t, "company": c, "salary": s, "details": d}).execute()
            st.success("تم النشر! ستظهر الوظيفة لآلاف المتقدمين فوراً.")

# --- 5. مركز البيانات الإداري (🔐) ---
elif choice == "📊 مركز البيانات الإداري":
    st.title("📊 لوحة تحكم الإدارة العليا")
    if st.text_input("رمز الدخول", type="password") == "roya2026":
        t1, t2 = st.tabs(["👥 المتقدمين", "💼 الوظائف"])
        with t1:
            res = supabase.table("application").select("*").execute()
            df = pd.DataFrame(res.data)
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 تصدير البيانات (Excel)", df.to_csv(), "Roya_Data.csv")
        with t2:
            res_j = supabase.table("Jobs").select("*").execute()
            st.table(pd.DataFrame(res_j.data))
