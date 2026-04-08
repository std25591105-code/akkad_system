import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="شركة رؤيا للتوظيف الذكي", page_icon="👁️", layout="wide")

# --- تحسينات بصرية (CSS) لحل مشكلة الأزرار الفارغة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* تنسيق الأزرار لجعلها واضحة */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: #004aad;
        color: white !important;
        font-weight: bold;
        border: 2px solid #00d4ff;
        padding: 15px;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* تصميم كرت الوظيفة المطور */
    .job-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 10px solid #004aad;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* صناديق الإحصائيات مع أيقونات */
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border-top: 5px solid #00d4ff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- الربط الآمن بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try:
        return create_client(st.secrets["URL"], st.secrets["KEY"])
    except:
        return None

supabase = init_connection()

# --- القائمة الجانبية الملونة ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #004aad;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = {
        "🏠 الرئيسية": "home",
        "💼 الوظائف المتاحة": "jobs",
        "📝 التقديم الإلكتروني": "apply",
        "🏢 إضافة وظيفة (للشركات)": "add_job",
        "🔐 لوحة التحكم": "admin"
    }
    choice = st.radio("القائمة الرئيسية", list(menu.keys()))
    st.write("---")
    st.success("النسخة المطورة 2.0")

# --- 1. الرئيسية (إحصائيات ذكية) ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #004aad;'>مرحباً بك في منصة رؤيا</h1>", unsafe_allow_html=True)
    
    # محاولة جلب أرقام حقيقية
    try:
        jobs_count = len(supabase.table("Jobs").select("id").execute().data)
        app_count = len(supabase.table("application").select("id").execute().data)
    except:
        jobs_count, app_count = 0, 0

    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="stat-card"><h3>👥 {app_count}</h3><p>متقدم للعمل</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="stat-card"><h3>💼 {jobs_count}</h3><p>وظيفة منشورة</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="stat-card"><h3>📍 بابل</h3><p>المقر الرئيسي</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🔔 آخر الأخبار")
    st.info("نبحث حالياً عن مناديب مبيعات لشركة مواد غذائية في الحلة، التقديم عبر قسم الوظائف.")
    
    if st.button("🚀 افتح استمارة التقديم السريع الآن"):
        st.warning("يرجى الانتقال لقسم 'التقديم الإلكتروني' من اليمين")

# --- 2. الوظائف (عرض Jobs) ---
elif choice == "💼 الوظائف المتاحة":
    st.title("💼 الفرص الوظيفية الحالية")
    if supabase:
        try:
            res = supabase.table("Jobs").select("*").execute()
            if res.data:
                for job in res.data:
                    st.markdown(f"""
                    <div class="job-card">
                        <h2 style='color: #004aad;'>{job.get('title')}</h2>
                        <p><b>🏢 الشركة:</b> {job.get('company')} | <b>💰 الراتب:</b> {job.get('salary')}</p>
                        <p>{job.get('details')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("حالياً لا توجد وظائف، ضيف وحدة من قسم الشركات حتى تظهر هنا!")
        except: st.error("تأكد من وجود جدول باسم Jobs")

# --- 3. التقديم الإلكتروني (application) ---
elif choice == "📝 التقديم الإلكتروني":
    st.title("📝 تقديم طلب توظيف")
    with st.form("apply_form", clear_on_submit=True):
        n = st.text_input("الأسم الكامل")
        p = st.text_input("رقم الواتساب")
        s = st.text_area("الخبرات السابقة")
        if st.form_submit_button("إرسال الطلب وحفظه"):
            if n and p:
                supabase.table("application").insert({"name": n, "phone": p, "skills": s}).execute()
                st.balloons()
                st.success("تم الحفظ بنجاح!")

# --- 4. إضافة وظيفة (لأصحاب العمل) ---
elif choice == "🏢 إضافة وظيفة (للشركات)":
    st.title("🏢 بوابة أصحاب العمل")
    with st.form("add_job_form"):
        t = st.text_input("العنوان الوظيفي")
        c = st.text_input("اسم الشركة")
        s = st.text_input("الراتب")
        d = st.text_area("تفاصيل الوظيفة")
        if st.form_submit_button("نشر الوظيفة فوراً"):
            supabase.table("Jobs").insert({"title": t, "company": c, "salary": s, "details": d}).execute()
            st.success("تم النشر!")

# --- 5. لوحة التحكم ---
elif choice == "🔐 لوحة التحكم":
    st.title("📊 الإدارة")
    if st.text_input("رمز الدخول", type="password") == "roya2026":
        data = supabase.table("application").select("*").execute()
        st.dataframe(pd.DataFrame(data.data), use_container_width=True)
