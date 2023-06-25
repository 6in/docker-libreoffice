curl -k -u elastic:espass \
  -H 'Content-type: application/json' \
  -XGET https://localhost:9200/my_index/_search