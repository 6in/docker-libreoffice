DSTPATH=/root/work/output
SRCPATH=/root/work/input/sample.pptx
docker-compose exec office /bin/bash -c "cd /root/work && python3 scripts/pdf_to_zip.py"