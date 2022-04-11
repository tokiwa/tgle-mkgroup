import base64

from flask import *
# import gensim
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
# save_word2vec_format で保存したモデル
# word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('model/entity_vector.model.bin', binary=True) #東北大

@app.route('/getjdata', methods=['POST'])
def getjdata():

    # Postmanで送られたJSONはget_data()にて取得する。その際、型がByteとなるため、decodeで文字列に変換する。
    gdata = request.get_data().decode('utf-8')
    # JSONはダブルクォーテーション "　を使うため、postmanのjsonデータの設定に注意すること 2022/4/8
    jdata = json.loads(gdata)  # JSON文字列を辞書に変換する
    print(jdata)
    # 部分的な取り出しはkeyを利用する。
    print(jdata['group'])

    for i in range(len(jdata['student'])):
        print(jdata['student'][i]['name'],jdata['student'][i]['kw'])

    #
    # ここでw2vを呼び出す
    #

    return jsonify({"result": 'Success'}), 200

@app.route('/template')
def template():
    group = ['個人情報','プライバシ','セキュリティ']
#    group = []
#    group = request.args.get('group', '')
#    keyword = request.args.get('keyword', '')
#    print(type(group), len(group))
    return jsonify({"result": group}), 200

# 配列のPostを受信する　参考　https://ichi.pro/python-to-flask-o-shiyoshite-restfulapi-o-sakuseisuru-1325060478315
@app.route('/mkgroup', methods=['POST'])
def mkgroup():
#    group = ['個人情報','プライバシ','セキュリティ']
#    group = []
    jdata = {
        'group': ['g1', 'g2', 'g3'],
        'student': [
        {'name': 'u1', 'kw': ['kw1', 'kw2', 'kw3']},
        {'name': 'u2', 'kw': ['kw1', 'kw2', 'kw3']},
        {'name': 'u3', 'kw': ['kw1', 'kw2', 'kw3']}
    ]
    }

#OK  値だけの取り出し
#    for value in jdata.values():
#        print(value)

#OK    for key in jdata['student']:
#OK        print(key)
#OK    print(jdata['group'])
#OK    print(jdata['student'][0]['name'],jdata['student'][0]['kw'])

#NOK    data = json.loads(jdata,object_hook=ObjectLike)
#NOK    print(data.group)

#    group = request.args.get('group', '')
    keyword = request.args.get('keyword', '')
#    print(type(group), len(group))
#OK    return jsonify({"result": jdata['group'][0]}), 200
    return jsonify({"result": jdata['group']}), 200

# @app.get('/knownword')
# def knownword():
# # Check keyword id known in entity_vector
#
#     word = request.args.get('word','')
# # ord2vec_model.wv works by gensim 3.8 not 4.0
#     if word in word2vec_model.wv:
#         return jsonify({"knownword": True}),200
#     else:
#         return jsonify({"knownword": False}),400
#
# @app.get('/similarity')
# def similarity():
#     word1 = request.args.get('word1', '')
#     word2 = request.args.get('word2', '')
#
#     similarity = word2vec_model.similarity(word1, word2)
#     return jsonify({"similarity": float(similarity)}), 200

if __name__ == "__main__":
    app.run(debug=True)
