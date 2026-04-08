import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="شركة رؤيا للتوظيف الذكي", page_icon="👁️", layout="wide")

# --- لمسات جمالية احترافية (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    
    .main { background-color: #f0f4f8; }
    
    /* كرت الوظيفة المطور */
    .job-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 10px solid #004aad;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        transition: 0.4s ease;
    }
    .job-card:hover { transform: scale(1.02); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
    
    /* تصميم الأزرار الفخم */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(135deg, #004aad 0%, #00d4ff 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        font-size: 18px;
    }
    
    /* تصميم الـ Sidebar */
    [data-testid="stSidebar"] { background-color: #ffffff; border-left: 1px solid #ddd; }
    
    /* صناديق الإحصائيات */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 5px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الربط بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try:
        return create_client(st.secrets["URL"], st.secrets["KEY"])
    except:
        return None

supabase = init_connection()

# --- القائمة الجانبية المحدثة ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #004aad;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "💼 الوظائف المتاحة", "📝 التقديم الإلكتروني", "🏢 للشركات (إضافة وظيفة)", "🔐 لوحة التحكم"]
    choice = st.radio("القائمة الرئيسية", menu)
    st.write("---")
    st.info("💡 شركة رؤيا: طريقك الأسرع للوظيفة المثالية في العراق.")

# --- 1. الرئيسية (جماليات وإحصائيات) ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #004aad;'>مرحباً بك في مستقبل التوظيف</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="stat-card"><h2>+1.2k</h2><p>باحث عن عمل</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="stat-card"><h2>85</h2><p>وظيفة جديدة</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="stat-card"><h2>24/7</h2><p>دعم فني</p></div>', unsafe_allow_html=True)
    col4.markdown('<div class="stat-card"><h2>بابل</h2><p>المقر الرئيسي</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### ✨ مميزات منصة رؤيا الجديدة")
    st.write("1. **سرعة الاستجابة:** ربط مباشر مع أصحاب العمل.")
    st.write("2. **سهولة التقديم:** استمارة ذكية لا تستغرق دقيقة.")
    st.write("3. **الخصوصية:** بياناتك محمية بأعلى معايير التشفير.")

# --- 2. الوظائف (عرض Jobs) ---
elif choice == "💼 الوظائف المتاحة":
    st.title("💼 اكتشف مستقبلك هنا")
    if supabase:
        try:
            res = supabase.table("Jobs").select("*").execute()
            if res.data:
                for job in res.data:
                    st.markdown(f"""
                    <div class="job-card">
                        <h2 style='color: #004aad; margin-bottom:5px;'>{job.get('title', 'وظيفة غير مسمى')}</h2>
                        <p style='font-size: 18px;'><b>🏢 الشركة:</b> {job.get('company', 'شركة غير محددة')} | <b>📍 الموقع:</b> العراق</p>
                        <p style='color: #28a745; font-weight: bold;'>💰 الراتب: {job.get('salary', 'حسب المقابلة')}</p>
                        <hr>
                        <p>{job.get('details', 'لا توجد تفاصيل حالية.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"تفعيل تقديم سريع على {job.get('title')}", key=job.get('id')):
                        st.session_state.target_job = job.get('title')
                        st.success(f"تم اختيار {job.get('title')}. اذهب لقسم التقديم.")
            else:
                st.warning("لا توجد وظائف متاحة حالياً.")
        except:
            st.error("يرجى التأكد من إعداد جدول Jobs في سوبابيس.")

# --- 3. التقديم الإلكتروني (application) ---
elif choice == "📝 التقديم الإلكتروني":
    st.title("📝 استمارة التقديم الرسمية")
    
    # ميزة معاينة الاستمارة قبل الإرسال
    with st.expander("👁️ زر فتح ومعاينة الاستمارة (تأكد من بياناتك)"):
        st.write("هكذا ستظهر بياناتك لمدير التوظيف في شركة رؤيا:")
        st.info("الاسم: [سيظهر هنا] | الهاتف: [سيظهر هنا] | المهارات: [ستظهر هنا]")

    with st.form("main_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("الاسم الكامل")
        phone = c2.text_input("رقم الهاتف")
        edu = st.selectbox("التحصيل الدراسي", ["بكالوريوس", "دبلوم", "إعدادية", "أخرى"])
        skills = st.text_area("تكلم عن مهاراتك (ماذا تجيد؟)")
        
        btn = st.form_submit_button("إرسال الطلب الآن")
        if btn and name and phone:
            try:
                supabase.table("application").insert({"name": name, "phone": phone, "skills": f"[{edu}] {skills}"}).execute()
                st.balloons()
                st.success(f"تم الإرسال بنجاح يا {name}. سنتصل بك قريباً!")
            except:
                st.error("فشل الإرسال. تأكد من جدول application.")

# --- 4. إضافة وظيفة (للشركات) ---
elif choice == "🏢 للشركات (إضافة وظيفة)":
    st.title("🏢 بوابة أصحاب العمل")
    st.markdown("انشر وظيفتك الآن لتصل لآلاف الباحثين عن عمل في بابل.")
    
    with st.form("job_form"):
        title = st.text_input("العنوان الوظيفي (مثلاً: مندوب مبيعات)")
        company = st.text_input("اسم الشركة أو المحل")
        salary = st.text_input("الراتب المتوقع")
        details = st.text_area("وصف الوظيفة وشروطها")
        
        if st.form_submit_button("نشر الوظيفة في المنصة"):
            if title and company:
                try:
                    supabase.table("Jobs").insert({"title": title, "company": company, "salary": salary, "details": details}).execute()
                    st.success("🎉 تم نشر الوظيفة بنجاح! ستظهر فوراً في قسم الوظائف.")
                except:
                    st.error("تأكد من جدول Jobs.")

# --- 5. لوحة التحكم (🔐) ---
elif choice == "🔐 لوحة التحكم":
    st.title("🔐 الإدارة")
    pwd = st.text_input("رمز الدخول الآمن", type="password")
    if pwd == "roya2026":
        tab1, tab2 = st.tabs(["👥 المتقدمين", "💼 الوظائف المنشورة"])
        with tab1:
            try:
                data = supabase.table("application").select("*").execute()
                st.table(pd.DataFrame(data.data))
            except: st.write("لا توجد بيانات متقدمين.")
        with tab2:
            try:
                data_j = supabase.table("Jobs").select("*").execute()
                st.table(pd.DataFrame(data_j.data))
            except: st.write("لا توجد وظائف.")
