import streamlit as st
from supabase import create_client, Client

# --- إعدادات الصفحة ---
st.set_page_config(page_title="شركة رؤيا للتوظيف", page_icon="👁️", layout="wide")

# --- الاتصال بقاعدة البيانات (Supabase) ---
@st.cache_resource
def init_connection():
    url = st.secrets["URL"]
    key = st.secrets["KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- القائمة الجانبية (Navigation) ---
st.sidebar.markdown("<h1 style='text-align: center; color: #1E88E5;'>شركة رؤيا 👁️</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>خيارك الأمثل لإيجاد الوظيفة المناسبة</p>", unsafe_allow_html=True)
st.sidebar.write("---")
menu = ["الرئيسية 🏠", "إضافة وظيفة ➕", "الوظائف المتاحة 💼", "تسجيل باحث عن عمل 📝", "بيانات المتقدمين 👥"]
choice = st.sidebar.radio("انتقل إلى:", menu)

# --- 1. الصفحة الرئيسية ---
if choice == "الرئيسية 🏠":
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في شركة رؤيا للتوظيف 👁️</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?ixlib=rb-4.0.3", use_container_width=True)
    st.info("نحن هنا لنكون الجسر بينك وبين مستقبلك المهني. استخدم القائمة الجانبية للبدء.")

# --- 2. إضافة وظيفة ---
elif choice == "إضافة وظيفة ➕":
    st.title("نشر فرصة عمل جديدة")
    with st.form("job_form", clear_on_submit=True):
        job_title = st.text_input("المسمى الوظيفي")
        company_name = st.text_input("اسم الشركة")
        salary = st.text_input("الراتب")
        details = st.text_area("تفاصيل الوظيفة")
        submit_job = st.form_submit_button("نشر الوظيفة في رؤيا")
        
        if submit_job:
            if job_title and company_name:
                try:
                    supabase.table("jobs").insert({
                        "title": job_title,
                        "company": company_name,
                        "salary": salary,
                        "details": details
                    }).execute()
                    st.success("✅ تم نشر الوظيفة بنجاح في نظام رؤيا!")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

# --- 3. عرض الوظائف ---
elif choice == "الوظائف المتاحة 💼":
    st.title("استكشف الفرص المتاحة حالياً")
    try:
        response = supabase.table("jobs").select("*").execute()
        jobs_data = response.data
        if jobs_data:
            for job in jobs_data:
                with st.expander(f"💼 {job.get('title')} - {job.get('company')}"):
                    st.write(f"**الراتب:** {job.get('salary')}")
                    st.write(f"**التفاصيل:** {job.get('details')}")
        else:
            st.info("لا توجد وظائف معروضة حالياً.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")

# --- 4. تسجيل باحث عن عمل ---
elif choice == "تسجيل باحث عن عمل 📝":
    st.markdown("<h2 style='text-align: center;'>استمارة التقديم الإلكترونية - شركة رؤيا</h2>", unsafe_allow_html=True)
    
    with st.form("applicant_form", clear_on_submit=False):
        full_name = st.text_input("الاسم الرباعي")
        phone = st.text_input("رقم الهاتف")
        skills = st.text_area("الخبرات والمهارات")
        
        st.write("---")
        personal_photo = st.file_uploader("ارفق صورتك الشخصية 📸", type=['jpg', 'jpeg', 'png'])
        documents = st.file_uploader("ارفق صورة الهوية/المستمسكات 📄", type=['jpg', 'jpeg', 'png'])
        
        submit_applicant = st.form_submit_button("إرسال الطلب وإصدار الاستمارة")
        
    if submit_applicant:
        if full_name and phone:
            try:
                # حفظ في قاعدة البيانات
                supabase.table("applicants").insert({
                    "name": full_name, "phone": phone, "skills": skills
                }).execute()
                
                st.balloons()
                st.markdown("<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #1E88E5;'>", unsafe_allow_html=True)
                st.markdown("<h2 style='text-align: center; color: #1E88E5;'>📋 استمارة تقديم - شركة رؤيا للتوظيف</h2>", unsafe_allow_html=True)
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**الاسم الكامل:** {full_name}")
                    st.write(f"**رقم الهاتف:** {phone}")
                    st.write(f"**المهارات:** {skills}")
                with c2:
                    if personal_photo:
                        st.image(personal_photo, width=150)
                
                if documents:
                    st.write("**المرفقات الرسمية:**")
                    st.image(documents, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.info("⚠️ يرجى تصوير الشاشة للاحتفاظ بالاستمارة.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# --- 5. بيانات المتقدمين ---
elif choice == "بيانات المتقدمين 👥":
    st.title("إدارة المتقدمين (خاص بالشركة)")
    try:
        response = supabase.table("applicants").select("*").execute()
        applicants_data = response.data
        if applicants_data:
            st.dataframe(applicants_data, use_container_width=True)
        else:
            st.info("لا توجد طلبات تقديم حتى الآن.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
