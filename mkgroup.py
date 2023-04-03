import base64
import os

from flask import *
import json
import numpy as np
import requests

# url = "http://192.168.1.105:5555/openai"
# url = "http://192.168.1.105:5555/similarity"
url =os.getenv('TGLE_SIMILARITY_SERVER')

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
            sim_g.append(sim_kw)
        sim.append(sim_g)

    len_i = len(sim)
    len_j = len(sim[0])

    gkey = [[] for j in range(len_j)]
    assign = {}
    similarity_max = [[0 for i in range(len_j)] for j in range(len_i)]

    for i in range(len_i):
        for j in range(len_j):
            similarity_max[i][j] = max(sim[i][j])

    len_g = len(gkey)
    group = [[] for i in range(len_g)]
    nps = np.array(similarity_max)
    count = 0
    flag = False
    while True:
        nps_copy = np.copy(nps)
        for i in range(len_g):
            u, s = np.unravel_index(np.argmax(nps_copy), nps_copy.shape)

            # jsonifyのjson.dumpsはnumpy.int型を処理できないので、item()を用いてintにcastする。
            # 参考　https://qiita.com/exp/items/2253e32c22e81e688ef4
            gkey[s].append(u.item())
            assign[str(u.item())] = s.item()  # key: ポストされたユーザ番号(0〜)　value: アサインされたグループ

            # print(gkey)
            nps_copy[u] = -1  # similarityが最大であったユーザ行を対象外(-1)にする。
            nps[u] = -1  # similarityが最大であったユーザ行を対象外(-1)にする。
            nps_copy[:, s] = -1  # 教員のKeyword列を対象外(-1)にする。
            count += 1
            if count == len_u:
                flag = True
                break
        if flag:
            break
    print(gkey)
    for k,v in assign.items():
        print(k,v)

    return jsonify(json.dumps(assign)), 200

@app.route('/postdata', methods=['POST'])
def postdata():
    # 配列のPostを受信する　参考　https://ichi.pro/python-to-flask-o-shiyoshite-restfulapi-o-sakuseisuru-1325060478315
    # Postmanで送られたJSONはget_data()にて取得する。その際、型がByteとなるため、decodeで文字列に変換する。
    gdata = request.get_data().decode('utf-8')
    # JSONはダブルクォーテーション "　を使うため、postmanのjsonデータの設定に注意すること 2022/4/8
    jdata = json.loads(gdata)  # JSON文字列を辞書に変換する
    # 部分的な取り出しはkeyを利用する。
    print(jdata['groupKeyword'])

    for i in range(len(jdata['student'])):
        print(jdata['student'][i])

    return jsonify({"result": 'Success'}), 200


if __name__ == "__main__":
    app.run(debug=True)
