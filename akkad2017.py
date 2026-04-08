import streamlit as st
from supabase import create_client, Client

# --- إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="شركة رؤيا للتوظيف | Roya Hire", page_icon="👁️", layout="wide")

# --- تحسين المظهر بـ CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #1E88E5; color: white; border: none; height: 3em; transition: 0.3s; }
    .stButton>button:hover { background-color: #1565C0; transform: scale(1.02); }
    .job-card { padding: 20px; border-radius: 15px; background: white; border-left: 5px solid #1E88E5; box-shadow: 2px 2px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- الاتصال الآمن بقاعدة البيانات ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["URL"]
        key = st.secrets["KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error("⚠️ خطأ في مفاتيح الربط. تأكد من إعداد Secrets بشكل صحيح.")
        return None

supabase = init_connection()

# --- القائمة الجانبية بتصميم عصري ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222800.png", width=100)
    st.markdown("<h2 style='text-align: center;'>رؤيا للتوظيف</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = ["🏠 الرئيسية", "💼 الوظائف المتاحة", "📝 تقديم طلب جديد", "➕ إضافة وظيفة (للشركات)", "📊 لوحة التحكم"]
    choice = st.radio("القائمة الرئيسية", menu)

# --- 1. الرئيسية ---
if choice == "🏠 الرئيسية":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h1 style='color: #1E88E5;'>مستقبلك يبدأ برؤية واضحة.. 👁️</h1>", unsafe_allow_html=True)
        st.write("شركة رؤيا توفر لك منصة ذكية لربط الكفاءات بأفضل الشركات في العراق.")
        st.button("استكشف الوظائف الآن")
    with col2:
        st.image("https://images.unsplash.com/photo-1521737711867-e3b97375f902?ixlib=rb-4.0.3", use_container_width=True)

# --- 2. عرض الوظائف (تصميم كروت) ---
elif choice == "💼 الوظائف المتاحة":
    st.title("💼 الفرص الوظيفية الحالية")
    if supabase:
        res = supabase.table("jobs").select("*").execute()
        if res.data:
            for job in res.data:
                st.markdown(f"""
                <div class="job-card">
                    <h3>{job['title']}</h3>
                    <p><b>🏢 الشركة:</b> {job['company']} | <b>💰 الراتب:</b> {job['salary']}</p>
                    <p>{job['details']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"التقديم على وظيفة {job['title']}", key=job['id']):
                    st.info("انتقل إلى قسم 'تقديم طلب جديد' لإكمال بياناتك.")
        else:
            st.info("لا توجد وظائف معروضة حالياً.")

# --- 3. تقديم طلب جديد (الاستمارة الفخمة) ---
elif choice == "📝 تقديم طلب جديد":
    st.title("📝 استمارة التقديم الإلكترونية")
    with st.container():
        with st.form("pro_form", clear_on_submit=False):
            c1, c2 = st.columns(2)
            name = c1.text_input("الاسم الكامل")
            phone = c2.text_input("رقم الهاتف")
            edu = st.selectbox("التحصيل الدراسي", ["إعدادية", "دبلوم", "بكالوريوس", "ماجستير/دكتوراه"])
            skills = st.text_area("المهارات والخبرات")
            
            st.write("---")
            f1, f2 = st.columns(2)
            pic = f1.file_uploader("الصورة الشخصية", type=['jpg','png'])
            doc = f2.file_uploader("المستمسكات الرسمية", type=['jpg','png'])
            
            submit = st.form_submit_button("إرسال الطلب وحفظ الاستمارة")
            
            if submit and name and phone:
                if supabase:
                    supabase.table("applicants").insert({"name": name, "phone": phone, "skills": f"{edu} - {skills}"}).execute()
                    st.success("✅ تم حفظ بياناتك بنجاح في نظام رؤيا!")
                    st.balloons()
                    
                    # عرض الاستمارة كأنها مطبوعة
                    st.markdown("<div style='border: 2px dashed #1E88E5; padding: 20px;'>", unsafe_allow_html=True)
                    st.subheader("📋 وصل تقديم طلب - شركة رؤيا")
                    st.write(f"**رقم القيد:** ROYA-{phone[-4:]}")
                    st.write(f"**الاسم:** {name} | **التخصص:** {edu}")
                    if pic: st.image(pic, width=100)
                    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. إضافة وظيفة ---
elif choice == "➕ إضافة وظيفة (للشركات)":
    st.title("➕ نشر فرصة عمل")
    with st.form("add_job"):
        t = st.text_input("العنوان الوظيفي")
        c = st.text_input("اسم الشركة")
        s = st.text_input("الراتب")
        d = st.text_area("وصف العمل")
        if st.form_submit_button("نشر الآن"):
            if supabase:
                supabase.table("jobs").insert({"title": t, "company": c, "salary": s, "details": d}).execute()
                st.success("تم النشر بنجاح!")

# --- 5. لوحة التحكم ---
elif choice == "📊 لوحة التحكم":
    st.title("📊 إدارة البيانات")
    if supabase:
        tab1, tab2 = st.tabs(["المتقدمين", "الوظائف المنشورة"])
        with tab1:
            data = supabase.table("applicants").select("*").execute()
            st.dataframe(data.data, use_container_width=True)
        with tab2:
            jobs = supabase.table("jobs").select("*").execute()
            st.table(jobs.data)
