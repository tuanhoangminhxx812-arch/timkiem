import streamlit as st
import glob
import csv
import re

def remove_vietnamese_accents(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ÙÚỤỦŨƯỪỨỰỬỮ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đđ]', 'd', s)
    return s

@st.cache_data
def load_data():
    questions = []
    
    csv_files = glob.glob("*.csv")
    for file_path in csv_files:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            type_col = -1
            content_col = -1
            correct_col = -1
            
            current_q = None
            current_ans = []
            
            for row in reader:
                # find header
                if type_col == -1:
                    for i, cell in enumerate(row):
                        c = str(cell).replace("\n", " ").strip().lower()
                        if c == "phân loại":
                            type_col = i
                        elif c in ["câu hỏi", "nội dung câu hỏi"]:
                            content_col = i
                        elif c in ["đáp án", "đáp án đúng"]:
                            correct_col = i
                    continue # Skip the header row itself for parsing
                
                if type_col != -1 and content_col != -1 and correct_col != -1:
                    # process data rows
                    if len(row) > type_col:
                        row_type = str(row[type_col]).strip().upper()
                        if row_type == "Q":
                            if current_q is not None and current_q != "":
                                questions.append({"question": current_q, "answer": "\n".join(current_ans), "source": file_path})
                            if len(row) > content_col:
                                current_q = str(row[content_col]).strip()
                            else:
                                current_q = ""
                            current_ans = []
                        elif row_type == "A":
                            if len(row) > content_col:
                                ans_text = str(row[content_col]).strip()
                                is_correct = False
                                if len(row) > correct_col:
                                    if str(row[correct_col]).strip().upper() in ["X", "V"]:
                                        is_correct = True
                                if is_correct:
                                    current_ans.append(ans_text)
            
            if current_q is not None and current_q != "":
                 questions.append({"question": current_q, "answer": "\n".join(current_ans), "source": file_path})
                 
    return questions

def main():
    st.set_page_config(page_title="Tìm Kiếm Câu Hỏi & Đáp Án", layout="wide", page_icon="🔍")
    
    # Custom CSS for a beautiful, modern design
    st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stTextInput > div > div > input {
            font-size: 20px !important;
            padding: 15px !important;
            border-radius: 10px;
            border: 2px solid #4e73df;
        }
        .q-container {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            border-left: 6px solid #4e73df;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .q-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        }
        .q-title {
            font-size: 24px;
            font-weight: 700;
            color: #2e59d9;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .a-text {
            font-size: 22px;
            color: #0f6848;
            font-weight: 600;
            padding: 15px;
            background-color: #e3fdf4;
            border-radius: 8px;
            border-left: 5px solid #1cc88a;
            white-space: pre-wrap;
        }
        .src-text {
            font-size: 14px;
            color: #858796;
            margin-top: 15px;
            font-style: italic;
            text-align: right;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔍 Công Cụ Tìm Kiếm Nhanh")
    st.markdown("##### 💡 Chỉ cần nhập từ khóa vào ô bên dưới, hệ thống sẽ hiển thị câu hỏi và đáp án đúng dành cho bạn.")
    
    questions = load_data()
    
    if not questions:
        st.error("Không tìm thấy dữ liệu từ các file CSV. Vui lòng kiểm tra lại.")
        return
    
    search_query = st.text_input("", placeholder="Nhập nội dung cần tìm kiếm tại đây (ví dụ: hợp đồng trọn gói)...")
    
    if search_query:
        query_normalized = remove_vietnamese_accents(search_query.lower())
        query_words = [w for w in query_normalized.split() if w.strip()]
        
        # Filter questions based on query (fuzzy match: ignores accents and word order)
        results = []
        for q in questions:
            q_normalized = remove_vietnamese_accents(q["question"].lower())
            # Match if all typed words are found anywhere in the question
            if all(word in q_normalized for word in query_words):
                results.append(q)
                
        if results:
            st.success(f"✨ Tìm thấy **{len(results)}** câu hỏi phù hợp.")
            for q in results:
                # Clean source name by removing .csv
                src_name = q["source"].replace(".xlsx.csv", ".xlsx").replace(".xls.csv", ".xls")
                
                # Handling empty answer cases
                ans_display = q["answer"] if q["answer"] else "⚠️ Không tìm thấy đáp án đúng (không có dấu X) trong file gốc."
                
                # HTML block for rendering
                st.markdown(f'''
                <div class="q-container">
                    <div class="q-title">Q: {q["question"]}</div>
                    <div class="a-text">A: {ans_display}</div>
                    <div class="src-text">Tài liệu: {src_name}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning(f"😔 Không có câu hỏi nào chứa từ khóa '{search_query}'. Vui lòng thử một từ khóa khác!")

if __name__ == "__main__":
    main()
