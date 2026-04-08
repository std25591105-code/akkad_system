import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="شركة رؤيا للتوظيف الذكي", page_icon="👁️", layout="wide")

# --- تنسيق الألوان والكتابة (حل مشكلة الكتابة الماتبين) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    /* جعل الخلفية فاتحة والنص غامق لضمان الوضوح التام */
    .stApp { background-color: #f0f2f6; color: #1e1e1e; }
    
    /* كرت الوظيفة المطور */
    .job-card {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 10px solid #004aad; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px; color: #1e1e1e;
    }
    
    /* أزرار واضحة وقوية */
    .stButton>button {
        width: 100%; border-radius: 10px; background: #004aad;
        color: white !important; font-weight: bold; border: none; padding: 12px;
    }
    
    /* صناديق الإحصائيات */
    .stat-box {
        background: white; padding: 20px; border-radius: 15px;
        text-align: center; border-bottom: 5px solid #00d4ff;
        font-weight: bold; color: #004aad;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الربط بقاعدة البيانات (استخدام المفتاح الصحيح) ---
@st.cache_resource
def init_connection():
    try:
        # استخدم مفتاح anon public اللي يبدأ بـ eyJh...
        return create_client(st.secrets["URL"], st.secrets["KEY"])
    except:
        return None

supabase = init_connection()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #004aad;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "🔍 بحث عن وظيفة", "📝 تقديم طلب", "🏢 إضافة وظيفة (للشركات)", "🔐 الإدارة"]
    choice = st.sidebar.radio("القائمة", menu)

# --- 1. الرئيسية (إحصائيات) ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center;'>منصة رؤيا لتوظيف الكفاءات</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="stat-box"><h3>+150</h3><p>وظيفة منشورة</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="stat-box"><h3>+2000</h3><p>متقدم نشط</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="stat-box"><h3>24/7</h3><p>دعم فني</p></div>', unsafe_allow_html=True)
    st.write("---")
    st.success("💡 نصيحة: تأكد من كتابة مهاراتك بشكل مفصل لزيادة فرص قبولك.")

# --- 2. بحث عن وظيفة (نظام السيرش) ---
elif choice == "🔍 بحث عن وظيفة":
    st.title("🔍 محرك البحث عن الوظائف")
    search = st.text_input("ابحث بالعنوان الوظيفي أو اسم الشركة...")
    
    if supabase:
        try:
            res = supabase.table("Jobs").select("*").execute()
            if res.data:
                filtered_jobs = [j for j in res.data if search.lower() in j['title'].lower() or search.lower() in j['company'].lower()] if search else res.data
                for job in filtered_jobs:
                    st.markdown(f"""
                    <div class="job-card">
                        <h2 style='color: #004aad;'>{job['title']}</h2>
                        <p><b>🏢 الشركة:</b> {job['company']} | <b>💰 الراتب:</b> {job['salary']}</p>
                        <p>{job['details']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else: st.info("لا توجد وظائف حالياً.")
        except: st.error("تأكد من إعداد جدول Jobs وإيقاف RLS.")

# --- 3. تقديم طلب (إضافة الجنس) ---
elif choice == "📝 تقديم طلب":
    st.title("📝 استمارة التقديم الذكية")
    with st.form("apply_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الكامل")
        phone = col2.text_input("رقم الهاتف")
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
        edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "أخرى"])
        skills = st.text_area("تكلم عن خبراتك ومهاراتك")
        
        if st.form_submit_button("إرسال الطلب"):
            if name and phone:
                try:
                    # تم تعديل اسم الجدول إلى application ليتطابق مع ما أنشأته
                    supabase.table("application").insert({
                        "name": name, "phone": phone, 
                        "skills": f"[{gender}] [{edu}] {skills}"
                    }).execute()
                    st.balloons()
                    st.success("تم الإرسال بنجاح!")
                except: st.error("خطأ في الربط. تأكد من جدول application.")

# --- 4. إضافة وظيفة ---
elif choice == "🏢 إضافة وظيفة (للشركات)":
    st.title("🏢 بوابة أصحاب العمل")
    with st.form("add_job"):
        t = st.text_input("عنوان الوظيفة")
        c = st.text_input("اسم الشركة")
        s = st.text_input("الراتب")
        d = st.text_area("الوصف الوظيفي")
        if st.form_submit_button("نشر الوظيفة"):
            try:
                supabase.table("Jobs").insert({"title": t, "company": c, "salary": s, "details": d}).execute()
                st.success("تم النشر!")
            except: st.error("تأكد من جدول Jobs.")

# --- 5. الإدارة ---
elif choice == "🔐 الإدارة":
    if st.text_input("رمز الدخول", type="password") == "roya2026":
        try:
            res = supabase.table("application").select("*").execute()
            st.write("### قائمة المتقدمين")
            st.dataframe(pd.DataFrame(res.data))
        except: st.warning("لا توجد بيانات حالياً.")
