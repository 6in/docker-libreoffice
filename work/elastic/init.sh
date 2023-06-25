# delete index
curl -k -u elastic:espass \
  -H 'Content-type: application/json' \
  -XDELETE https://localhost:9200/my_index

# create index
curl -k -u elastic:espass \
  -H 'Content-type: application/json' \
  -XPUT https://localhost:9200/my_index \
  -d '@work/elastic/mapping.json'

# create index alias
curl -k -u elastic:espass \
  -H 'Content-type: application/json' \
  -XPOST https://localhost:9200/_aliases \
  -d '@work/elastic/alias.json'
