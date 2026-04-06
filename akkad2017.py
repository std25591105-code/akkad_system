import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# --- إعدادات الربط مالتك من الصور ---
URL = "https://kemyohayjryswwtwtyfo.supabase.co"
KEY = "sb_publishable_nCM_0PuIjQeR0i0lXbkdrA_qn_o6" # تأكد إنك تنسخ المفتاح كامل من صفحة API Keys

# إنشاء الاتصال بالسحابة
supabase = create_client(URL, KEY)
st.set_page_config(page_title="بوابة أكد | Akkad Portal", layout="wide", page_icon="🏢")

# --- دوال الربط مع السحاب ---
def get_data(table):
    res = supabase.table(table).select("*").execute()
    return pd.DataFrame(res.data)

# --- نظام الحماية وتسجيل الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏢 نظام بوابة أكد الذكي</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            tab_login, tab_reg = st.tabs(["🔑 دخول الموظفين", "📩 طلب انضمام"])
            with tab_login:
                u = st.text_input("اسم المستخدم", key="u_login")
                p = st.text_input("كلمة المرور", type="password", key="p_login")
                if st.button("تسجيل الدخول", use_container_width=True):
                    res = supabase.table("users").select("*").eq("username", u).eq("password", p).eq("active", 1).execute()
                    if res.data:
                        st.session_state.auth, st.session_state.user = True, u
                        st.session_state.role = res.data[0]['role']
                        st.rerun()
                    else: st.error("عذراً، البيانات غير صحيحة أو الحساب غير نشط")
            with tab_reg:
                new_u = st.text_input("اسم مستخدم مقترح")
                new_p = st.text_input("كلمة مرور قوية", type="password")
                if st.button("إرسال طلب للمدير", use_container_width=True):
                    try:
                        supabase.table("users").insert({"username": new_u, "password": new_p, "role": "staff", "active": 0}).execute()
                        st.success("تم الإرسال بنجاح، انتظر تفعيل الإدارة")
                    except: st.error("الاسم محجوز مسبقاً")
    st.stop()

# --- لوحة التحكم الرئيسية (Dashboard) ---
st.markdown(f"### 🗓️ {datetime.now().strftime('%Y-%m-%d')} | مرحباً بك، {st.session_state.user} 👋")

# إحصائيات سريعة (للمظهر الفخم)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("إجمالي الوظائف", len(get_data("jobs")))
with c2: st.metric("طلبات التوظيف", len(get_data("submissions")))
with c3: st.metric("الموظفون النشطون", len(get_data("users")[get_data("users")['active']==1]))
with c4: st.metric("فرع الشركة", "بابل / المركز")

st.divider()

# --- القائمة الجانبية ---
menu = st.sidebar.selectbox("🎯 التنقل السريع", ["لوحة التحكم المركزية", "إدارة الإرساليات", "شؤون الموظفين (Admin)"])

# --- 1. لوحة التحكم المركزية (الوظائف) ---
if menu == "لوحة التحكم المركزية":
    st.subheader("📋 إدارة الفرص الوظيفية")
    
    if st.session_state.role == "admin":
        with st.expander("➕ إضافة وظيفة جديدة (صلاحية مدير)"):
            col_a, col_b = st.columns(2)
            jid = col_a.text_input("كود الوظيفة (مثلاً: AK-101)")
            jtitle = col_b.text_input("المسمى الوظيفي")
            if st.button("اعتماد ونشر الوظيفة"):
                supabase.table("jobs").insert({"job_id": jid, "title": jtitle, "added_by": st.session_state.user, "date_added": str(datetime.now().date())}).execute()
                st.success("تم النشر بنجاح")
                st.rerun()

    jobs_df = get_data("jobs")
    if not jobs_df.empty:
        for idx, row in jobs_df.iterrows():
            with st.container(border=True):
                col_i, col_t, col_d, col_b = st.columns([1, 3, 2, 1])
                col_i.info(f"🆔 {row['job_id']}")
                col_t.markdown(f"**{row['title']}**")
                col_d.caption(f"📅 نُشرت في: {row['date_added']}")
                if st.session_state.role == "admin":
                    if col_b.button("🗑️ حذف", key=f"del_{row['job_id']}"):
                        supabase.table("jobs").delete().eq("job_id", row['job_id']).execute()
                        st.rerun()
    else: st.warning("لا توجد وظائف معروضة حالياً")

# --- 2. إدارة الإرساليات (سجل المتقدمين) ---
elif menu == "إدارة الإرساليات":
    st.subheader("📩 سجل المتقدمين والنتائج")
    
    with st.expander("📝 تسجيل إرسالية مرشح جديد"):
        all_jobs = get_data("jobs")
        if not all_jobs.empty:
            with st.form("sub_form"):
                target = st.selectbox("الوظيفة المستهدفة", all_jobs['job_id'].tolist())
                name = st.text_input("اسم المرشح الثلاثي")
                phone = st.text_input("رقم الهاتف (واتساب)")
                note = st.text_area("ملاحظات أولية")
                if st.form_submit_button("حفظ وإرسال"):
                    supabase.table("submissions").insert({
                        "job_id": target, "name": name, "phone": phone, "emp": st.session_state.user,
                        "status": "قيد المراجعة", "result_note": note, "date": str(datetime.now().date())
                    }).execute()
                    st.success("تم الحفظ بنجاح")
                    st.rerun()
        else: st.error("لا يمكن الإضافة، لا توجد وظائف متاحة")

    # عرض الإرساليات مع فلاتر
    subs_df = get_data("submissions")
    if not subs_df.empty:
        st.dataframe(subs_df, use_container_width=True)
        
        if st.session_state.role == "admin":
            st.divider()
            st.subheader("🛠️ تحديث النتائج (للمدير)")
            sub_to_edit = st.selectbox("اختر الرقم التسلسلي للإرسالية (ID)", subs_df['id'].tolist())
            new_status = st.select_slider("تغيير الحالة", options=["قيد المراجعة", "انتظار", "مرفوض", "مقبول"])
            final_note = st.text_input("ملاحظة نهائية (مثلاً: باشر العمل، أو لم يجب على الهاتف)")
            if st.button("تحديث الحالة النهائية"):
                supabase.table("submissions").update({"status": new_status, "result_note": final_note}).eq("id", sub_to_edit).execute()
                st.success("تم التحديث")
                st.rerun()

# --- 3. شؤون الموظفين (إدارة الحسابات) ---
elif menu == "شؤون الموظفين (Admin)":
    if st.session_state.role != "admin":
        st.error("❌ هذه المنطقة محظورة! صلاحية المدير فقط.")
    else:
        st.subheader("👥 إدارة طاقم العمل")
        u_df = get_data("users")
        
        # تفعيل الحسابات الجديدة
        pending = u_df[u_df['active'] == 0]
        st.write(f"طلبات معلقة: {len(pending)}")
        for _, r in pending.iterrows():
            col_un, col_act = st.columns([3, 1])
            col_un.write(f"طلب من: **{r['username']}**")
            if col_act.button("تفعيل ✅", key=f"act_{r['username']}"):
                supabase.table("users").update({"active": 1}).eq("username", r['username']).execute()
                st.rerun()
        
        st.divider()
        # قائمة الموظفين الحاليين
        st.write("📋 قائمة الموظفين النشطين")
        st.table(u_df[u_df['active'] == 1][['username', 'role']])

# --- تذييل الصفحة ---
st.sidebar.divider()
if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
    st.session_state.auth = False
    st.rerun()
st.sidebar.caption("نظام أكد السحابي v3.0 | 2026")