import streamlit as st
import base64
from PIL import Image
from  chain_openai import generate_output

st.markdown("""
    <style>
    body {
        color: #000000;
        background-color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

logo = Image.open('Images/E4I4_logo.png')

PATENT_CATEGORIES = ['선택','A - 생활필수품','B - 처리조작;운수','C - 화학;야금','D - 섬유;지류','E - 고정구조물','F - 기계공학;조명;가열;무기;폭파','G - 물리학','H - 전기']

class User_Input:
    def __init__(self, patent_title, patent_category, tech_description,claim, designs_info, design_files):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description
        self.claim = claim
        self.designs_info = designs_info
        self.designs_files = design_files

def get_pdf_download_link(file_name):
    with open(file_name, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{file_name}">PDF 다운로드</a>'
    return href

def download_page():
    st.title("Preview:")
    show_pdf('모범 명세서.pdf')
    st.markdown(get_pdf_download_link('모범 명세서.pdf'), unsafe_allow_html = True)
    backbutton = st.button(label="뒤로가기")
    if backbutton:
        st.session_state.page = 'combined'

def design_count_page():
    with st.form(key='count_form'):
        
        st.title("도면도 개수")
        design_num = st.number_input('도면 개수를 입력하세요.', min_value = 1, value = 1, step = 1)
    
        count_submit_button = st.form_submit_button(label='다음')
        backbutton = st.form_submit_button(label="뒤로가기")
        if count_submit_button:
            st.session_state.page = 'design_input'
            st.session_state.design_num = design_num
        elif backbutton:
            st.session_state.page = 'main'

def design_input_page():
    with st.form(key='design_input_form'):
        st.title("도면도 첨부")
        st.write("도면도 PDF 파일은 아래에 첨부해주세요")
        designs = []
        design_files = []
        for i in range(st.session_state.design_num):
                design_file = st.file_uploader(f"도면도 {i+1} - pdf", type=['pdf'], key=f"design_file_{i}")
                design_description = st.text_area(f'도면도 {i+1}에 대한 설명', key=f"design_description_{i}")
                designs.append(design_description)
                design_files.append(design_file)

        design_submit_button = st.form_submit_button(label="다음")
        backbutton = st.form_submit_button(label="뒤로가기")
        if design_submit_button:
            st.session_state.designs_info = designs
            st.session_state.designs_files = design_files
            st.session_state.page = 'combined' 

        elif backbutton:
            st.session_state.page = 'count'


def combined_page():
    title = st.session_state.patent_title
    category = st.session_state.patent_category
    description = st.session_state.tech_description
    claim = st.session_state.claim
    designs_info = st.session_state.designs_info
    designs_files = st.session_state.designs_files
    input = User_Input(title, category, description, claim, designs_info, designs_files)
    output_dic = generate_output(input)
    with st.form(key='combined_form'):

        st.title("Output 수정")

        sum_result2 = output_dic.abstract
        user_sum2 = st.text_area("요약을 원하시는대로 수정해주세요", value=sum_result2)
        
        claims_result2 = "수정 가능한 청구범위입니다"
        user_claims2 = st.text_area("청구범위를 원하시는대로 수정해주세요", value=claims_result2)

        domain_result2 = "수정 가능한 기술분야입니다"
        user_domain2 = st.text_area("기술분야를 원하시는대로 수정해주세요", value=domain_result2)

        background_result2 = "수정 가능한 배경기술 입니다"
        user_background2 = st.text_area("배경기술을 원하시는대로 수정해주세요", value=background_result2)
        
        todo_result2 = "수정 가능한 해결하려는 과제입니다"
        user_todo2 = st.text_area("해결하려는 과제 결과물을 원하시는대로 수정해주세요", value = todo_result2)

        method_result2 = "수정 가능한 해결수단입니다"
        user_method2 = st.text_area("해결수단을 원하시는대로 수정해주세요", value=method_result2)
        
        effect_result2 = "수정 가능한 발명의 효과입니다"
        user_effect2 = st.text_area("발명의 효과를 원하시는대로 수정해주세요", value=effect_result2)
        
    #----1을 넣고 gpt로 돌린 다음 ----2를 output으로 보여주는 작업 필요함
        combined_submit_button = st.form_submit_button(label='제출')
        backbutton = st.form_submit_button(label="뒤로가기")
        if combined_submit_button:
            st.session_state.sum_result2 = user_sum2
            st.session_state.claims_result2 = user_claims2
            st.session_state.domain_result2 = user_domain2
            st.session_state.background_result2 = user_background2
            st.session_state.todo_result2 = user_todo2
            st.session_state.method_result2 = user_method2
            st.session_state.effect_result2 = user_effect2
            st.session_state.page = 'download'
        elif backbutton:
            st.session_state.page = 'design_input'

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.image(logo)
    st.title('Ez Patent AI')
    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        claim = st.text_area('청구항')
        tech_description = st.text_area('발명 내용')
        submit_button = st.form_submit_button(label='다음')

        if submit_button:
            st.session_state.previous_page = st.session_state.page
            st.session_state.page = 'count'
            st.session_state.patent_title = patent_title
            st.session_state.patent_category = patent_category
            st.session_state.claim = claim
            st.session_state.tech_description = tech_description

if __name__ == "__main__":
    if "page" in st.session_state:
        st.session_state.previous_page = st.session_state.page
    if "page" not in st.session_state:
        st.session_state.page = "main"
        st.session_state.previous_page = None

    if st.session_state.page == "main":
        main()
    elif st.session_state.page == "count":
        design_count_page()
    elif st.session_state.page == "design_input":
        design_input_page()
    elif st.session_state.page == "combined":
        print("Generate Output")
        combined_page()
    elif st.session_state.page == "download":
        download_page()
