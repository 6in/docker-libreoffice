import subprocess
import re


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
    command = f'pdfinfo {pdf_file}'  # ここに実行したいコマンドを入力します。
    result = run_bash_command(command)
    param = text_to_map(result)
    print(param)
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
    command = "".join(f""" 
    /usr/bin/soffice --nolockcheck --nologo --headless --norestore
             --language=ja --nofirststartwizard --convert-to pdf
             --outdir "{output_dir}" "{input_file}"
    """.split("\n"))
    print(command)
    run_bash_command(command)


def pdf_to_png(input_pdf):
    command = f"""
    pdftoppm -png {input_pdf} {input_pdf}
    """
    run_bash_command(command)


ppt_file = "input/sample.pptx"
pdf_file = "output/sample.pdf"

doc_to_pdf(ppt_file, "output/")
pdf_to_png(pdf_file)
pdf_to_text(pdf_file)
