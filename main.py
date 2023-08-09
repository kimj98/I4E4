import streamlit as st

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

class GPT_Output:
    def __init__(self, patent_title, abstract, background, tech_description, claims):
        self.patent_title = patent_title
        self.abstract = abstract
        self.background = background
        self.tech_description = tech_description
        self.claims = claims

def download_page():
    st.title("완성!")
    st.write("다운로드 하세요")
    st.button('PDF 다운로드')

def main():
    st.title('명세서 작성 ai')

    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        tech_description = st.text_area('발명의 구체적 설명')

        designs = []
        design_num = st.number_input('도면 개수', min_value=1, value=1, step=1)
        for i in range(design_num):
            design_file = st.file_uploader(f"도면도 {i+1} - pdf", type=['pdf'], key=f"design_file_{i}")
            design_description = st.text_area(f'도면도 {i+1}에 대한 설명', key=f"design_description_{i}")
            designs.append(design_description)

        user_input = User_Input(patent_title, patent_category, tech_description, designs)

        submit_button = st.form_submit_button(label='제출')

    if submit_button:
        gpt_output = GPT_Output(
            patent_title = "Generated Patent Title",
            abstract = "Generated Abstract",
            background = "Generated Background",
            tech_description = "Generated Technology Description",
            claims = "Generated Claims"
        )

        st.subheader("Generated Patent:")
        st.write("Title: ", gpt_output.patent_title)
        st.write("Abstract: ", gpt_output.abstract)
        st.write("Background: ", gpt_output.background)
        st.write("Technology Description: ", gpt_output.tech_description)
        st.write("Claims: ", gpt_output.claims)
        st.session_state.page = 'download'

if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        main()
    elif st.session_state.page == "download":
        download_page()

    #123123
