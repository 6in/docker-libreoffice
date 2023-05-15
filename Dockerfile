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