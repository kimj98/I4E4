import pdfkit
def get_pdf_download_link(pdf_bytes, filename):
    """Generates a link allowing the pdf to be downloaded"""
    import base64
    pdf_base64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:file/pdf;base64,{pdf_base64}" download="{filename}">Download PDF</a>'
    return href

def generate_pdf(output_dic):
    html_content = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Patent Document</title>
        </head>
        <body>
            <h1>Patent Document</h1>
            
            <h2>요약</h2>
            <p>{abstract}</p>

            <h2>청구범위</h2>
            <p>{claims}</p>

            <h2>기술분야</h2>
            <p>{domain}</p>

            <h2>배경기술</h2>
            <p>{background}</p>

            <h2>해결하려는 과제</h2>
            <p>{problem}</p>

            <h2>과제 해결수단</h2>
            <p>{stepstosolve}</p>

            <h2>발명의 효과</h2>
            <p>{effect}</p>
        </body>
    </html>
    """.format(
        abstract=output_dic.abstract,
        claims=output_dic.claims,
        domain=output_dic.domain,
        background=output_dic.background,
        problem=output_dic.problem,
        stepstosolve=output_dic.stepstosolve,
        effect=output_dic.effect,
    )

    return pdfkit.from_string(html_content, False, options={
    'encoding': "UTF-8"})


