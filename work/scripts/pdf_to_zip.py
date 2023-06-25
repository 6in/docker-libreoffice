import subprocess
import re
import os
import zipfile
import shutil
import yaml
from PIL import Image


def run_bash_command(command: str):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f'Error: {error}')
    else:
        return output.decode('utf-8')


def text_to_map(text: str):
    ret = {}
    lines = text.split("\n")
    for line in lines:
        tokens = line.split(": ")
        if len(tokens) != 2:
            continue
        key = tokens[0]
        val = tokens[1].strip()
        ret[key] = val
    return ret


def pdf_to_text(pdf_file: str, output_dir: str) -> dict[str, object]:
    print(f"pdf_to_text({pdf_file})")

    command = f'pdfinfo {pdf_file}'
    result = run_bash_command(command)
    param = text_to_map(result)
    param['Pages'] = int(param["Pages"])
    param["page_sizes"] = []

    for x in range(1, param["Pages"]+1):
        output_file = f"{output_dir}/text-%02d.txt" % x
        command = f"pdftotext -f %d -l %d {pdf_file} {output_file}" % (x, x)
        run_bash_command(command)

        # テキストのスペースを最適化
        text = ""
        with open(output_file, "r") as f:
            text = f.read()
        with open(output_file, "w") as f:
            f.write(re.sub(r"\s+", " ", text))

        file = f"{output_dir}/image-%02d.png" % x
        w, h = get_image_size(file)
        param["page_sizes"].append(dict(page=x, width=w, height=h))

    with open(f"{output_dir}/pdf_info.yml", "w") as f:
        yaml.dump(param, f)

    return param


def doc_to_pdf(input_file: str, output_dir: str):
    print(f"doc_to_pdf({input_file},{output_dir})")

    command = "".join(f""" 
    /usr/bin/soffice --nolockcheck --nologo --headless --norestore
             --language=ja --nofirststartwizard --convert-to pdf
             --outdir "{output_dir}" "{input_file}"
    """.split("\n"))
    run_bash_command(command)


def pdf_to_png(input_pdf: str, output_dir):
    print(f"pdf_to_png({input_pdf})")
    command = f"""
    pdftoppm -png {input_pdf} {output_dir}/image
    """
    run_bash_command(command)


def png_size(param, output_dir):
    maxPages = param["Pages"] + 1
    for i in range(1..maxPages):
        file = f"{output_dir}/image-%02d" % i
        w, h = get_image_size(file)


def get_image_size(file_path):
    # 画像ファイルを開く
    with Image.open(file_path) as img:
        # 幅と高さを取得
        width, height = img.size
    return width, height


def out_to_zip(folder_path: str, output_path: str):
    print(f"out_to_zip({folder_path},{output_path})")

    # ファイルが存在したら削除する
    if os.path.exists(output_path):
        os.remove(output_path)

    # Zip化する
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                print(f"{file}")
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(
                    file_path, folder_path))


def main(input_file: str, work_dir: str):

    (_, file) = os.path.split(input_file)
    (file_wo_ext, ext) = os.path.splitext(file)
    pdf_file = f"{work_dir}/{file_wo_ext}.pdf"
    zip_file = f"output/{work_dir}.zip"

    os.makedirs(work_dir, exist_ok=True)
    doc_to_pdf(input_file, work_dir)
    pdf_to_png(pdf_file, work_dir)
    param = pdf_to_text(pdf_file, work_dir)
    os.remove(pdf_file)
    out_to_zip(work_dir, zip_file)
    shutil.rmtree(work_dir)


if __name__ == '__main__':
    input_file = "input/sample.pptx"
    main(input_file, "6c7135ef-87e3-4fc0-90ad-887200e8838e")
