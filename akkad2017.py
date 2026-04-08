import streamlit as st
from supabase import create_client, Client

# --- إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="رؤيا للتوظيف | Roya Hire", page_icon="👁️", layout="wide")

# --- نظام التصميم المتقدم (CSS) ---
st.markdown("""
    <style>
    /* تغيير الخط والخلفية */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .main { background-color: #f4f7f9; }
    
    /* تصميم كرت الوظيفة */
    .job-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 8px solid #004aad;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .job-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    
    /* تصميم الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #004aad, #007bff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    
    /* إحصائيات علوية */
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 4px solid #004aad;
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

# --- القائمة الجانبية بتصميم نظيف ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #004aad;'>رؤيــــا 👁️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>الجيل الجديد للتوظيف</p>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "💼 استكشاف الوظائف", "📝 التقديم الإلكتروني", "📊 لوحة الإدارة"]
    choice = st.radio("انتقل إلى", menu)
    st.write("---")
    st.caption("حقوق الطبع محفوظة لشركة رؤيا 2026")

# --- 1. الصفحة الرئيسية (بدون صورة وبإحصائيات) ---
if choice == "🏠 الرئيسية":
    st.markdown("<h1 style='text-align: center;'>منصة رؤيا للتوظيف الذكي</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>نربط الطموح بالفرصة المناسبة</p>", unsafe_allow_html=True)
    
    # قسم الإحصائيات الفخم
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-box"><h3>+500</h3><p>متقدم نشط</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><h3>+120</h3><p>شركة شريكة</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box"><h3>+45</h3><p>وظيفة شاغرة</p></div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown("### لماذا شركة رؤيا؟")
    st.info("نقدم لك نظاماً متكاملاً لإدارة السير الذاتية وتسهيل الوصول لأصحاب العمل في بابل وكافة أنحاء العراق.")

# --- 2. استكشاف الوظائف (بجدول Jobs) ---
elif choice == "💼 استكشاف الوظائف":
    st.title("💼 الفرص المتاحة حالياً")
    if supabase:
        try:
            res = supabase.table("Jobs").select("*").execute()
            if res.data:
                for job in res.data:
                    with st.container():
                        st.markdown(f"""
                        <div class="job-card">
                            <h2 style='color: #004aad;'>{job.get('title', 'عنوان الوظيفة')}</h2>
                            <p><b>🏢 الشركة:</b> {job.get('company', 'غير محدد')} | <b>💰 الراتب:</b> {job.get('salary', 'يحدد لاحقاً')}</p>
                            <p style='color: #666;'>{job.get('details', 'لا توجد تفاصيل إضافية')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"التقديم على {job.get('title')}", key=job.get('id')):
                            st.toast("يرجى الانتقال لقسم التقديم الإلكتروني")
            else:
                st.info("لا توجد وظائف معروضة حالياً.")
        except:
            st.error("فشل في جلب البيانات. تأكد من إعداد جدول Jobs.")

# --- 3. التقديم الإلكتروني (بجدول application) ---
elif choice == "📝 التقديم الإلكتروني":
    st.title("📝 استمارة التقديم الذكية")
    st.markdown("ملء هذه الاستمارة هو خطوتك الأولى نحو النجاح.")
    
    with st.form("pro_apply", clear_on_submit=True):
        t1, t2 = st.columns(2)
        name = t1.text_input("الاسم الكامل (الرباعي)")
        phone = t2.text_input("رقم الهاتف (واتساب)")
        
        edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "ماجستير", "دكتوراه"])
        skills = st.text_area("المهارات والخبرات السابقة")
        
        submitted = st.form_submit_button("إرسال الطلب رسمياً")
        
        if submitted:
            if name and phone:
                try:
                    supabase.table("application").insert({
                        "name": name, 
                        "phone": phone, 
                        "skills": f"[{edu}] {skills}"
                    }).execute()
                    st.balloons()
                    st.success("✅ تم حفظ بياناتك في قاعدة بيانات رؤيا بنجاح!")
                except:
                    st.error("حدث خلل في الإرسال. تأكد من إعدادات سوبابيس.")

# --- 4. لوحة الإدارة ---
elif choice == "📊 لوحة الإدارة":
    st.title("📊 نظام إدارة البيانات")
    pw = st.text_input("أدخل رمز الدخول للإدارة", type="password")
    if pw == "roya2026": # رمز بسيط للحماية
        try:
            res = supabase.table("application").select("*").execute()
            st.dataframe(res.data, use_container_width=True)
        except:
            st.warning("لا توجد بيانات متاحة حالياً.")
    elif pw:
        st.error("الرمز غير صحيح")
