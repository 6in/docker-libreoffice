import yaml
from elasticsearch import Elasticsearch, helpers
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


# BASIC認証のユーザ名とパスワード
user = 'elastic'
password = 'espass'


def connect_es() -> Elasticsearch:
    # Elasticsearchクライアントを初期化します。
    return Elasticsearch("https://localhost:9200",
                         basic_auth=(user, password),
                         verify_certs=False
                         )


def add_document(es: Elasticsearch,  doc: dict):
    path_hash = doc["path_hash"]
    # 削除する
    delete_doc(es, path_hash=path_hash)

    # 登録
    return es.index(index="doc-search-alias", document=doc)


def add_documents(es: Elasticsearch, doc_list: list[dict]) -> dict:
    path_hash = doc_list[0]["path_hash"]
    # 削除する
    delete_doc(es, path_hash=path_hash)

    actions = [{"_index": "doc-search-alias", "_source": x} for x in doc_list]
    # dump(actions)
    return helpers.bulk(es, actions)


def search_by_dict(es: Elasticsearch,  param: dict, mode: str = "should") -> object:
    query = {
        "bool": {
            mode: [{"match": {key: param[key]}} for key in param.keys()]
        }
    }

    dump(query)
    return es.search(index="doc-search-alias",
                     query=query)


def delete_doc(es: Elasticsearch, path_hash: str):
    # 削除する
    return es.delete_by_query(index="doc-search-alias",
                              query={"match": {"path_hash": path_hash}})


def dump(res: dict):
    print(yaml.dump(res, allow_unicode=True))


doc = [
    dict(
        path_hash="abc",
        text_content="おはようございます",
        file_path="ファイルパス",
        file_type="xlsx",
        page_no=1,
        width=1000,
        height=200,
    ),
    dict(
        path_hash="abc",
        text_content="こんばんは、月が綺麗ですね",
        file_path="ファイルパス",
        file_type="pptx",
        page_no=2,
        width=1100,
        height=200,
    )
]

# Elasticsearchクライアントを初期化します。
with connect_es() as es:

    # ドキュメントの登録
    # res = add_document(es, doc[0])
    res = add_documents(es, doc)
    dump(res)

    query_param = dict(
        file_type="pptx",
        text_content="です"
    )
    res = search_by_dict(es, query_param, "must")
    # res = search_by_page_width(es, 2, 1100, "must")
    dump(res['hits']['hits'])
