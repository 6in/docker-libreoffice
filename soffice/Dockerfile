#ubuntuの18.04の最小イメージから構築
#まっさらな状態からの場合はscratchとする
FROM ubuntu
#イメージ作成時にRUNで事前にコマンドラインを実行できる
#パッケージリストを更新
RUN apt update
RUN apt upgrade -y
#日本語化パッケージリストをインストール
RUN apt install -y language-pack-ja-base language-pack-ja locales
#localeを日本語設定に変更
RUN locale-gen ja_JP.UTF-8
#言語を日本語に設定
ENV LANG ja_JP.UTF-8

# Libreofficeをインストール
RUN apt -y install libreoffice 
RUN apt -y install libreoffice-l10n-ja 
RUN apt -y install libreoffice-dmaths 
RUN apt -y install libreoffice-ogltrans 
RUN apt -y install libreoffice-writer2xhtml 
RUN apt -y install libreoffice-pdfimport 
RUN apt -y install libreoffice-help-ja

# Pythonをインストール
RUN apt -y install python3

# 作業用フォルダを作成
RUN mkdir /root/work
RUN chmod 777 /root/work

# フォントをインストール
RUN apt -y install fonts-ipafont

# PDFを画像に変換するツール(pdftoppm/pdftotext)
RUN apt -y install poppler-utils

# 画像変換を行う
RUN apt -y install imagemagick

# PIPをインストール
RUN apt -y install python3-pip

# 形態素解析
RUN pip3 install mecab-python3
RUN pip3 install unidic

# FastAPI
RUN apt -y install uvicorn
RUN pip3 install fastapi

# よく使うコマンド①
RUN apt -y install curl zip unzip

RUN pip3 install unotools
RUN pip3 install pyyaml
