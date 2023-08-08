#사용자가 사용하게될 메인 페이지
#여기서 백엔드팀이 사용자의 input을 받아와 chain.py에 적은 function들을 사용해서 OPENAI한테 받은 답변을 Display하는 공간
#실행방법: Terminal을 키고 streamlit run main.py 


import streamlit as st
from PiorArtSearch import retrieve

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
    def __init__(self, patent_title, patent_category, tech_description):
        self.patent_title = patent_title
        self.patent_category = patent_category
        self.tech_description = tech_description


def main():
    st.title('명세서 작성 ai')

    with st.form(key='my_form'):
        patent_title = st.text_input('특허품 명칭')
        patent_category = st.selectbox('특허의 분류', PATENT_CATEGORIES)
        tech_description = st.text_area('발명의 구체적 설명')
        user_input = User_Input(patent_title, patent_category, tech_description)

        if tech_description:
            output = retrieve(tech_description)
            st.write(output)

        

if __name__ == "__main__":
    main()
