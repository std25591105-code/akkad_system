import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(page_title="منصة رؤيا للتوظيف الذكي", page_icon="👁️", layout="wide")

# --- نظام التصميم المتقدم (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background: #f8f9fa; }
    
    /* تصميم الكروت */
    .job-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #004aad; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px; transition: 0.3s;
    }
    .job-card:hover { transform: translateY(-5px); }
    
    /* أزرار فخمة */
    .stButton>button {
        width: 100%; border-radius: 10px; background: linear-gradient(90deg, #004aad, #007bff);
        color: white; font-weight: bold; border: none; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الاتصال بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try:
        # تأكد من استخدام مفتاح anon (Legacy) اللي يبدأ بـ eyJh...
        return create_client(st.secrets["URL"], st.secrets["KEY"])
    except:
        return None

supabase = init_connection()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "🔍 استكشاف الوظائف", "📝 تقديم طلب توظيف", "🏢 إضافة وظيفة (للمكاتب)", "📊 الإدارة"]
    choice = st.radio("انتقل إلى:", menu)

# --- 1. الرئيسية ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في شركة رؤيا</h1>", unsafe_allow_html=True)
    st.info("نحن نربط الكفاءات العراقية بأفضل فرص العمل في بابل وجميع المحافظات.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("الوظائف النشطة", "45+")
    with col2:
        st.metric("المتقدمين هذا الشهر", "1200+")

# --- 2. استكشاف الوظائف (نظام بحث متطور) ---
elif choice == "🔍 استكشاف الوظائف":
    st.title("🔍 ابحث عن وظيفتك المستقبلية")
    
    search_query = st.text_input("🔍 ابحث بالعنوان الوظيفي أو اسم الشركة...")
    
    if supabase:
        try:
            res = supabase.table("Jobs").select("*").execute()
            if res.data:
                df = pd.DataFrame(res.data)
                # نظام فلاتر البحث
                if search_query:
                    df = df[df['title'].str.contains(search_query, na=False) | df['company'].str.contains(search_query, na=False)]
                
                for _, job in df.iterrows():
                    st.markdown(f"""
                    <div class="job-card">
                        <h3>{job['title']}</h3>
                        <p><b>🏢 الشركة:</b> {job['company']} | <b>💰 الراتب:</b> {job['salary']}</p>
                        <p>{job['details']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("لا توجد وظائف منشورة حالياً.")
        except:
            st.error("تأكد من إعداد جدول Jobs وإيقاف الـ RLS.")

# --- 3. تقديم طلب (إضافة الجنس) ---
elif choice == "📝 تقديم طلب توظيف":
    st.title("📝 استمارة التقديم")
    with st.form("apply_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الكامل")
        phone = col2.text_input("رقم الهاتف")
        
        gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)
        edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "ماجستير/دكتوراه"])
        skills = st.text_area("المهارات والخبرات")
        
        if st.form_submit_button("إرسال الطلب"):
            if name and phone and supabase:
                try:
                    supabase.table("application").insert({
                        "name": name, "phone": phone, 
                        "skills": f"[{gender}] - {edu}: {skills}"
                    }).execute()
                    st.balloons()
                    st.success("✅ تم استلام طلبك بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

# --- 4. إضافة وظيفة (للمكاتب) ---
elif choice == "🏢 إضافة وظيفة (للمكاتب)":
    st.title("🏢 بوابة أصحاب العمل")
    with st.form("job_form"):
        t = st.text_input("عنوان الوظيفة")
        c = st.text_input("اسم الشركة/المكتب")
        s = st.text_input("الراتب")
        d = st.text_area("التفاصيل والشروط")
        if st.form_submit_button("نشر الوظيفة"):
            if t and c and supabase:
                try:
                    supabase.table("Jobs").insert({"title": t, "company": c, "salary": s, "details": d}).execute()
                    st.success("🎉 تم النشر بنجاح!")
                except:
                    st.error("تأكد من إعدادات الجدول.")

# --- 5. الإدارة ---
elif choice == "📊 الإدارة":
    if st.text_input("رمز الدخول", type="password") == "roya2026":
        try:
            apps = supabase.table("application").select("*").execute()
            st.write("### قائمة المتقدمين")
            st.dataframe(pd.DataFrame(apps.data))
        except:
            st.warning("لا توجد بيانات.")
