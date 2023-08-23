#사용자가 사용하게될 메인 페이지
#여기서 백엔드팀이 사용자의 input을 받아와 chain.py에 적은 function들을 사용해서 OPENAI한테 받은 답변을 Display하는 공간
#실행방법: Terminal을 키고 streamlit run main.py 

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
    def __init__(self, patent_title, patent_category, tech_description, designs, claim, design_num, method_result, todo_result, background_result):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description
        self.claim = claim
        self.designs = designs
        self.design_num = design_num
        self.method_result = method_result
        self.todo_result = todo_result
        self.background_result = background_result

        
class GPT_Output:
    def __init__(self, patent_title, abstract, background, tech_description, claims, design_num, method_result, todo_result, background_result):
        self.patent_title = patent_title
        self.abstract = abstract
        self.background = background
        self.tech_description = tech_description
        self.claims = claims
        self.design_num = design_num
        self.method_result = method_result
        self.todo_result = todo_result
        self.background_result = background_result

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
    with st.form(key='count_form'):
        
        st.title("도면도 개수")

        design_num = st.number_input('도면 개수를 입력하세요.', min_value = 1, value = 1, step = 1)
        

        count_submit_button = st.form_submit_button(label='제출')
        if count_submit_button:
            st.session_state.page = 'design_input'
            st.session_state.design_num = design_num
    if st.button('뒤로가기'):
        go_back()


def design_input_page():
    with st.form(key='design_input_form'):
        st.title("도면도 첨부")
        st.write("도면도 PDF 파일은 아래에 첨부해주세요")
        designs = []
        for i in range(st.session_state.design_num):
                design_file = st.file_uploader(f"도면도 {i+1} - pdf", type=['pdf'], key=f"design_file_{i}")
                design_description = st.text_area(f'도면도 {i+1}에 대한 설명', key=f"design_description_{i}")
                designs.append(design_description)


        design_submit_button = st.form_submit_button(label="제출")
        if design_submit_button:
            st.session_state.page = 'background' # 수정요함


def background_output_page(background_result):
    background_result = "배경기술 완성본 수정 가능" #assign to gpt outputed 배경기술
    with st.form(key='background_output_form'):
        st.title("배경기술 결과물")
        user_background = st.text_area("배경기술을 원하시는대로 수정해주세요", value=background_result)
        
        background_submit_button = st.form_submit_button(label='제출')
        if background_submit_button:
            background_result = user_background
            st.session_state.page = 'todo'
    return background_result

def todo_page():
    todo_result = "수정 가능한 해결하려는 과제 결과물 입니다" #assign to gpt outputed 해결하려는 과제 결과물
    with st.form(key='todo_form'):
        st.title("해결하려는 과제 결과물")
        user_todo = st.text_area("해결하려는 과제 결과물을 원하시는대로 수정해주세요", value = todo_result)
        todo_submit_button = st.form_submit_button(label='제출')
        if todo_submit_button:
            todo_result = user_todo
            st.session_state.page = 'method'
    return todo_result

def method_page():
    method_result = "수정가능한 과제해결의 수단입니다"  #assign to gpt outputed 과제해결의 수단
    with st.form(key='method_form'):
        st.title("과제 해결의 수단")
        user_method = st.text_area("해결하려는 과제 결과물을 원하시는대로 수정해주세요", value=method_result)
        
        method_submit_button = st.form_submit_button(label='제출')
        if method_submit_button:
            method_result = user_method
            st.session_state.page = 'download'
    return method_result


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# def add_pdf_page():
#     st.title("참고용 PDF")
#     st.write("추가적으로 제출할 참고용 PDF를 첨부하세요.(최대 10개)")
#     uploaded_files = []
    
#     for i in range(10):
#         file = st.file_uploader(f"PDF 파일 {i+1} 첨부", type=["pdf"], key=f"pdf_{i+1}")
#         if file:
#             uploaded_files.append(file)
    
#     if uploaded_files:
#         st.write(f"You have uploaded {len(uploaded_files)} files.")
    
#     if st.button("다음"):
#         st.session_state.previous_page = st.session_state.page
#         st.session_state.page = "download"
#     if st.button('뒤로가기'):
#         go_back()



def main():
    st.title('명세서 작성 ai')

    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        claim = st.text_area('청구항')
        tech_description = st.text_area('발명 내용')
        design_num = 0
        todo_result = ""
        background_result = ""
        method_result = ""


        submit_button = st.form_submit_button(label='다음')

    if submit_button:
        st.session_state.previous_page = st.session_state.page
        st.session_state.page = 'count'
        st.session_state.todo_result = todo_result
        st.session_state.method_result = method_result

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
        
    elif st.session_state.page == "background":
        background_result = ""  # Initialize with default value
        background_result = background_output_page(background_result)
    elif st.session_state.page == "todo":
        todo_page()
    elif st.session_state.page == "method":
        method_page()
    elif st.session_state.page == "download":
        download_page()

