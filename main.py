#사용자가 사용하게될 메인 페이지
#여기서 백엔드팀이 사용자의 input을 받아와 chain.py에 적은 function들을 사용해서 OPENAI한테 받은 답변을 Display하는 공간
#실행방법: Terminal을 키고 streamlit run main.py 

import streamlit as st
import base64
from PIL import Image
from chain2 import generate_output

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
    def __init__(self, patent_title, patent_category, tech_description, designs):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description
        self.designs = designs

def about_page():
    st.sidebar.title("About")
    st.write("명세서 작성에 도움을 주는 ai입니다. 사용 방법은 blahblah")

def howtouse_page():
    st.sidebar.title("How to use")
    st.write("AI 사용방법. 사진첨부 혹은 @@ ")

example_1 = Image.open('example1.jpg')

def input_example_page():
    st.sidebar.title("Input Example")
    st.image(example_1, caption='Example 1')

def download_page():
    st.title("다운로드 페이지")
    show_pdf('./data/모범 명세서.pdf')
    st.write("완성된 명세서를 다운로드 하세요")
    st.button('PDF 다운로드')

    if st.button('뒤로 가기'):
        st.session_state.page = 'main'

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def ezpatent_ai_page():
    st.sidebar.title("ezPatent AI")
    st.title('ezPatent AI')

    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        tech_description = st.text_area('발명의 구체적 설명')

        indep_num = st.number_input('독립항 개수', min_value=1, value=1, step=1)
        for i in range(indep_num):
            indep_description = st.text_area(f'독립항 {i+1}에 대한 내용', key=f"indep_description_{i}")
            dept_keywords = st.text_area(f'독립항 {i+1}의 종속항)', key=f"dept_keywords_{i}")


        designs = []
        design_num = st.number_input('도면 개수', min_value=1, value=1, step=1)
        for i in range(design_num):
            design_file = st.file_uploader(f"도면도 {i+1} - pdf", type=['pdf'], key=f"design_file_{i}")
            design_description = st.text_area(f'도면도 {i+1}에 대한 설명', key=f"design_description_{i}")
            designs.append(design_description)

        user_input = User_Input(patent_title, patent_category, tech_description, designs)

        submit_button = st.form_submit_button(label='제출')
    
    
    if submit_button:
        output = generate_output(user_input)
     

        st.subheader("Generated Patent:")
        st.write("Title: ", user_input.patent_title)
        st.write("Abstract: ", output.abstract)
        st.write("Background: ", output.background)
        st.write("Technology Description: ", output.tech_description)
        st.write("Claims: ", output.claims)
        st.session_state.page = 'download'

    if "page" not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        main()
    elif st.session_state.page == "download":
        download_page()

def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Choose a page:", ["About", "ezPatent AI", "Input Example"])

    if page == "About":
        about_page()
    elif page == "ezPatent AI":
        ezpatent_ai_page()
    elif page == "Input Example":
        input_example_page()

if __name__ == "__main__":
    main()