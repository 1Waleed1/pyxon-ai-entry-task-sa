import sys


__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import streamlit as st
import os
from document_parser import DocumentParser
from vector_store import VectorManager

# 1. UI Configuration: Setting the page title and icon for a professional look
st.set_page_config(page_title="مساعدي الذكي", page_icon="🤖", layout="centered")

# 2. Resource Management: Using cache to load models once to save memory and time
@st.cache_resource
def load_managers():
    return DocumentParser(), VectorManager()

parser, v_db = load_managers()

# 3. Header Section: Clear instructions for the user
st.title("🤖 مساعدك الذكي لتحليل المستندات")
st.write("ارفع سيرتك الذاتية أو أي تقرير، واسألني أي سؤال عنه!")

# 4. File Upload Section: Handling user input and temporary storage
uploaded_file = st.file_uploader("ارفع ملف PDF أو Word هنا", type=["pdf", "docx"])

if uploaded_file is not None:
    # Saving the uploaded file temporarily to the local directory for processing
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"تم رفع الملف: {uploaded_file.name} بنجاح! ✅")

    # 5. Processing Logic: Triggering text extraction and vector storage
    if st.button("تحليل وحفظ الملف في قاعدة البيانات ⚙️"):
        with st.spinner("جاري قراءة وتقطيع الملف... ⏳"):
            raw_text = parser.read_file(file_path)
            chunks = parser.create_chunks(raw_text)
            
            st.info(f"تم تقطيع الملف إلى {len(chunks)} قطعة. جاري الحفظ...")
            v_db.add_chunks_to_db(chunks)
            st.success("تم تجهيز الملف وهو جاهز للبحث! 🚀")

# 6. Query Section: Implementing semantic search functionality
st.divider() # Visual separator for better UX
question = st.text_input("📝 اكتب سؤالك هنا:")

if st.button("ابحث 🔍"):
    if question:
        with st.spinner("جاري البحث في المستند.🕵️‍♂️"):
            # Performing semantic search to find the most relevant document segments
            results = v_db.search(question)
            
            st.subheader("💡 الإجابات المستخرجة:")
            # Displaying retrieved chunks in expandable sections for a clean UI
            for i, res in enumerate(results):
                with st.expander(f"نتيجة {i+1}", expanded=True):
                    st.write(res)
    else:
        st.warning("الرجاء كتابة سؤال أولاً في المربع أعلاه!")