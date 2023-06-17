DSTPATH=/root/work/output
SRCPATH=/root/work/input/sample.pptx
docker-compose run office /usr/bin/soffice --nolockcheck --nologo --headless --norestore \
                 --language=ja --nofirststartwizard --convert-to pdf \
                 --outdir "${DSTPATH}" "${SRCPATH}"
