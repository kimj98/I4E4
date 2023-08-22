import streamlit as st
import base64

st.markdown("""
    <style>
    body {
        color: #000000;
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

PATENT_CATEGORIES = ['선택','A - 생활필수품','B - 처리조작;운수','C - 화학;야금','D - 섬유;지류','E - 고정구조물','F - 기계공학;조명;가열;무기;폭파','G - 물리학','H - 전기']

class User_Input:
    def __init__(self, patent_title, patent_category, tech_description, designs, claim):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description
        self.claim = claim
        self.designs = designs

class GPT_Output:
    def __init__(self, patent_title, abstract, background, tech_description, claims):
        self.patent_title = patent_title
        self.abstract = abstract
        self.background = background
        self.tech_description = tech_description
        self.claims = claims

def go_back():
    if st.session_state.previous_page:
        st.session_state.page = st.session_state.previous_page
    else:
        st.session_state.page = "main"

def get_pdf_download_link(file_name):
    with open(file_name, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{file_name}">PDF 다운로드</a>'
    return href

def download_page():
    st.title("Preview:")
    show_pdf('모범 명세서.pdf')
    st.markdown(get_pdf_download_link('모범 명세서.pdf'), unsafe_allow_html = True)
    if st.button('뒤로가기'):
        go_back()

def design_count_page():
    st.title("도면도 개수")
    st.write("도면도 개수를 입력하세요")
    
    with st.form(key ='design_count_form'):
        designs = []
        design_num = st.number_input('도면 개수', min_value = 1, value = 1, step = 1)
        for i in range(design_num):
                design_file = st.file_uploader(f"도면도 {i+1} - pdf", type=['pdf'], key=f"design_file_{i}")
                design_description = st.text_area(f'도면도 {i+1}에 대한 설명', key=f"design_description_{i}")
                designs.append(design_description)

        submit = st.form_submit_button("다음")

        if submit:
            st.session_state.previous_page = st.session_state.page
            st.session_state.page = "add_pdf"
    
    if st.button('뒤로가기'):
        go_back()


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def add_pdf_page():
    st.title("참고용 PDF")
    st.write("추가적으로 제출할 참고용 PDF를 첨부하세요.(최대 10개)")
    uploaded_files = []
    
    for i in range(10):
        file = st.file_uploader(f"PDF 파일 {i+1} 첨부", type=["pdf"], key=f"pdf_{i+1}")
        if file:
            uploaded_files.append(file)
    
    if uploaded_files:
        st.write(f"You have uploaded {len(uploaded_files)} files.")
    
    if st.button("다음"):
        st.session_state.previous_page = st.session_state.page
        st.session_state.page = "download"
    if st.button('뒤로가기'):
        go_back()

def main():
    st.title('명세서 작성 ai')

    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        claim = st.text_area('청구항')
        tech_description = st.text_area('발명 내용')

        user_input = User_Input(patent_title, patent_category, claim, tech_description, [])

        submit_button = st.form_submit_button(label='다음')

    if submit_button:
        st.session_state.previous_page = st.session_state.page
        st.session_state.page = 'count'



if __name__ == "__main__":
    if "page" in st.session_state:
        st.session_state.previous_page = st.session_state.page

    if "page" not in st.session_state:
        st.session_state.page = "main"
        st.session_state.previous_page = None

    if st.session_state.page == "main":
        main()
    elif st.session_state.page == "download":
        download_page()
    elif st.session_state.page == "count":
        design_count_page()
    elif st.session_state.page == "add_pdf":
        add_pdf_page()
