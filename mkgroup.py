import base64

from flask import *
import json
import numpy as np
import requests

url = "http://192.168.1.105:5555/similarity"

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route('/mkgroup', methods=['POST'])
def mkgroup():

    # Postmanで送られたJSONはget_data()にて取得する。その際、型がByteとなるため、decodeで文字列に変換する。
    gdata = request.get_data().decode('utf-8')
    # JSONはダブルクォーテーション "　を使うため、postmanのjsonデータの設定に注意すること 2022/4/8
    jdata = json.loads(gdata)  # JSON文字列を辞書に変換する
    # 部分的な取り出しはkeyを利用する。
    groupKeyword = jdata['groupKeyword']
    keyword = jdata['student']

    len_u = len(keyword)
    len_g = len(groupKeyword)

    sim = []
    for i in range(len_u):
        sim_g = []
        for j in range(len_g):
            sim_kw = []
            for kw in keyword[i]:
                data = {"word1": groupKeyword[j], "word2": kw}
                jsonData = requests.get(url, params=data).json()
                sim_kw.append(round(jsonData["similarity"], 3))
            # print(sim_kw)
            sim_g.append(sim_kw)
        print(sim_g)
        sim.append(sim_g)
    #print(sim)

    len_i = len(sim)  # 7
    len_j = len(sim[0])  # 3

    gkey = [[] for j in range(len_j)]
    similarity_max = [[0 for i in range(len_j)] for j in range(len_i)]  # 初期化

    for i in range(len_i):
        for j in range(len_j):
            similarity_max[i][j] = max(sim[i][j])
        # print(similarity_max[i])

    len_g = len(gkey)  # 3  行数：教員のグループキーワード数
    # len_gu = len(gkey[0])   # 7　列数：Similarityの高いユーザID順
    group = [[] for i in range(len_g)]  # 初期化
    nps = np.array(similarity_max)
    # print(nps)
    # print(nps_copy)
    count = 0
    flag = False
    while True:
        nps_copy = np.copy(nps)
        # print(nps_copy)
        for i in range(len_g):
            u, s = np.unravel_index(np.argmax(nps_copy), nps_copy.shape)

            # jsonifyのjson.dumpsはnumpy.int型を処理できないので、intにcaskする。
            # 参考　https://qiita.com/exp/items/2253e32c22e81e688ef4
            gkey[s].append(u.item())

            # gkey[s].append(u)
            # print(gkey)
            nps_copy[u] = -1  # similarityが最大であったユーザ行を対象外(-1)にする。
            nps[u] = -1  # similarityが最大であったユーザ行を対象外(-1)にする。
            nps_copy[:, s] = -1  # 教員のKeyword列を対象外(-1)にする。
            count += 1
            #        print(count)
            # print(nps_copy)
            if count == len_u:
                flag = True
                break
        if flag:
            break
    print('Result:',gkey)

    # print(type(gkey))
    # for g in gkey:
    #     print(g)
    #     print(type(g[0]))

#    return jsonify({"result":"gkey"}), 200
    return jsonify(json.dumps(gkey)), 200


@app.route('/postdata', methods=['POST'])
def postdata():
    # 配列のPostを受信する　参考　https://ichi.pro/python-to-flask-o-shiyoshite-restfulapi-o-sakuseisuru-1325060478315
    # Postmanで送られたJSONはget_data()にて取得する。その際、型がByteとなるため、decodeで文字列に変換する。
    gdata = request.get_data().decode('utf-8')
    # JSONはダブルクォーテーション "　を使うため、postmanのjsonデータの設定に注意すること 2022/4/8
    jdata = json.loads(gdata)  # JSON文字列を辞書に変換する
    # print(jdata)
    # 部分的な取り出しはkeyを利用する。
    print(jdata['groupKeyword'])

    for i in range(len(jdata['student'])):
        print(jdata['student'][i])

    #
    # ここでw2vを呼び出す
    #

    return jsonify({"result": 'Success'}), 200

@app.route('/mkgroup0', methods=['POST'])
def mkgroup0():
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

if __name__ == "__main__":
    app.run(debug=True)
