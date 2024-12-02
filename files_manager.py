import shutil
from pypdf import PdfReader
import requests
import os
import mammoth
import json
import pypandoc
from pdfminer.high_level import extract_text as fallback_text_extraction


def manage_pdf(file_content):
    query_parameters = {"downloadformat": "pdf"}
    response = requests.get(file_content.download_url, params=query_parameters)
    with open(file_content.name, mode="wb") as file:
        file.write(response.content)
    file.close()
    text = ""
    try:
        reader = PdfReader(file_content.name)
        for page in reader.pages:
            page_text = page.extract_text()
            text = text + page_text + "\n"
        reader.close()
    except Exception:
        try:
            text = fallback_text_extraction(file_content.name)
        except Exception:
            text = ""
    os.remove(file_content.name)
    return text


def manage_word(file_content):
    query_parameters = {"downloadformat": "docx"}
    response = requests.get(file_content.download_url, params=query_parameters)
    with open(file_content.name, mode="wb") as file:
        file.write(response.content)
    file.close()
    with open(file_content.name, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
    docx_file.close()
    os.remove(file_content.name)
    return result


def manage_json(file_content):
    query_parameters = {"downloadformat": "json"}
    response = requests.get(file_content.download_url, params=query_parameters)
    result = pypandoc.convert_text(json.dumps(response.content.decode("utf-8")), 'json', 'md')
    return result


def run(github_access):
    fic = github_access.get_organization("FAIRiCUBE")
    files = 0
    for repo in fic.get_repos():
        path = 'repos/' + repo.name + '/files/'
        if not os.path.exists(path):
            os.makedirs(path)
        # print('\n')
        # print('--------------------------------------')
        # print(repo.name)
        # print('--------------------------------------')
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                try:
                    ext = file_content.name.split('.')
                    if len(ext) < 2:
                        continue
                    ext = file_content.name.split('.')[1]

                    # PDF
                    if ext == 'pdf':
                        text = manage_pdf(file_content)
                        f = open(path + file_content.name.split('.')[0] + '.md', 'w', encoding="utf-8")
                        f.write(text)
                        f.close()
                        files += 1

                    # MARKDOWN
                    elif ext == 'md':
                        f = open(path + file_content.name, 'wb')
                        f.write(file_content.decoded_content)
                        f.close()
                        files += 1

                    # TXT
                    elif ext == 'txt':
                        f = open(path + file_content.name.split('.')[0] + '.md', 'wb')
                        f.write(file_content.decoded_content)
                        f.close()
                        files += 1

                    # WORD
                    elif ext == 'docx':
                        result = manage_word(file_content)
                        with open(path + file_content.name.split('.')[0] + '.md', "w", encoding="utf-8") as markdown_file:
                            markdown_file.write(result.value)
                        markdown_file.close()
                        files += 1

                    # JSON
                    elif ext == 'json':
                        result = manage_json(file_content)
                        with open(path + file_content.name.split('.')[0] + '.md', "w", encoding="utf-8") as markdown_file:
                            markdown_file.write(result)
                        markdown_file.close()
                        files += 1
                except Exception:
                    print(Exception)
                    print(file_content.name)
                    continue

        if len(os.listdir(path)) == 0:
            shutil.rmtree(path)
    return files
