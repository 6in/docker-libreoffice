curl -k -u elastic:espass \
  -H 'Content-type: application/json' \
  -XPOST https://localhost:9200/my_index/_doc \
  -d '@work/elastic/data.json'