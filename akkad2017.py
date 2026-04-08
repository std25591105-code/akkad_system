import streamlit as st
from supabase import create_client, Client

# --- إعدادات فخمة لشركة رؤيا ---
st.set_page_config(page_title="شركة رؤيا للتوظيف", page_icon="👁️", layout="wide")

# --- تحسين التصميم ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1E88E5; color: white; border: none; font-weight: bold; }
    .job-card { padding: 20px; border-radius: 15px; background: white; border-right: 6px solid #1E88E5; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- الاتصال بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try:
        return create_client(st.secrets["URL"], st.secrets["KEY"])
    except:
        return None

supabase = init_connection()

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>رؤيا للتوظيف 👁️</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "📝 تقديم طلب", "💼 الوظائف المتاحة", "📊 لوحة التحكم"]
    choice = st.radio("انتقل إلى:", menu)

# --- 1. الرئيسية ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>مرحباً بك في شركة رؤيا</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1521737711867-e3b97375f902?ixlib=rb-4.0.3", use_container_width=True)
    st.info("نحن هنا لنرسم رؤية جديدة لمستقبلك المهني.")

# --- 2. تقديم طلب (يرتبط بجدول application) ---
elif choice == "📝 تقديم طلب":
    st.title("📝 استمارة التقديم الإلكترونية")
    with st.form("apply_form"):
        name = st.text_input("الاسم الرباعي")
        phone = st.text_input("رقم الهاتف")
        skills = st.text_area("الخبرات والمهارات")
        submit = st.form_submit_button("إرسال الطلب")
        
        if submit and name and phone:
            try:
                # هنا استخدمنا اسم الجدول اللي أنت سويته
                supabase.table("application").insert({"name": name, "phone": phone, "skills": skills}).execute()
                st.balloons()
                st.success(f"تم استلام طلبك بنجاح يا {name}")
            except Exception as e:
                st.error(f"تأكد أن الجدول باسم application وبدون حماية RLS. الخطأ: {e}")

# --- 3. الوظائف المتاحة (يرتبط بجدول Jobs) ---
elif choice == "💼 الوظائف المتاحة":
    st.title("💼 الفرص الوظيفية الحالية")
    try:
        # هنا استخدمنا اسم الجدول اللي أنت سويته
        res = supabase.table("Jobs").select("*").execute()
        if res.data:
            for job in res.data:
                st.markdown(f"<div class='job-card'><h3>{job.get('title', 'وظيفة')}</h3><p>{job.get('company', 'شركة')} - {job.get('salary', 'راتب')}</p></div>", unsafe_allow_html=True)
        else:
            st.info("لا توجد وظائف معروضة حالياً.")
    except Exception as e:
        st.warning(f"تأكد أن الجدول باسم Jobs وبدون حماية RLS. الخطأ: {e}")

# --- 4. لوحة التحكم ---
elif choice == "📊 لوحة التحكم":
    st.title("📊 إدارة المتقدمين")
    try:
        res = supabase.table("application").select("*").execute()
        st.dataframe(res.data, use_container_width=True)
    except:
        st.error("لا يمكن الوصول للبيانات حالياً.")
