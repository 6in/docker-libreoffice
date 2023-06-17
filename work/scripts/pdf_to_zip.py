import subprocess
import re
import os
import zipfile


def run_bash_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f'Error: {error}')
    else:
        return output.decode('utf-8')


def text_to_map(text):
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


def pdf_to_text(pdf_file):
    print(f"pdf_to_text({pdf_file})")

    command = f'pdfinfo {pdf_file}'
    result = run_bash_command(command)
    param = text_to_map(result)
    for x in range(1, int(param["Pages"])+1):
        output_file = f"{pdf_file}-%02d.txt" % x
        command = f"pdftotext -f %d -l %d {pdf_file} {output_file}" % (x, x)
        run_bash_command(command)

        text = ""
        with open(output_file, "r") as f:
            text = f.read()
        with open(output_file, "w") as f:
            f.write(re.sub(r"\s+", " ", text))


def doc_to_pdf(input_file, output_dir):
    print(f"doc_to_pdf({input_file},{output_dir})")

    command = "".join(f""" 
    /usr/bin/soffice --nolockcheck --nologo --headless --norestore
             --language=ja --nofirststartwizard --convert-to pdf
             --outdir "{output_dir}" "{input_file}"
    """.split("\n"))
    run_bash_command(command)


def pdf_to_png(input_pdf):
    print(f"pdf_to_png({input_pdf})")

    command = f"""
    pdftoppm -png {input_pdf} {input_pdf}
    """
    run_bash_command(command)


def out_to_zip(folder_path, output_path):
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


def main(input_file, work_dir):

    (_, file) = os.path.split(input_file)
    (file_wo_ext, ext) = os.path.splitext(file)
    pdf_file = f"{work_dir}/{file_wo_ext}.pdf"
    zip_file = f"output/{file_wo_ext}.zip"

    os.makedirs(work_dir, exist_ok=True)
    doc_to_pdf(input_file, work_dir)
    pdf_to_png(pdf_file)
    pdf_to_text(pdf_file)
    out_to_zip(work_dir, zip_file)


if __name__ == '__main__':
    input_file = "input/sample.pptx"
    main(input_file, "work4")
