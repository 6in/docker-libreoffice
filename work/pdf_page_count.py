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


pdf_file = "output/sample.pdf"
pdf_to_text(pdf_file)
