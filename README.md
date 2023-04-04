# TGLE MKGROUP

## 概要

バックエンドからREST APIにて、教員および学生のキーワードを取得し、教員および学生のキーワードのペアをSimilarity計算サービスにRequestし、ResponseとしてペアとなるキーワードのSimilarityを得ます。実装はSimilarityマトリックスを操作するためにNumPyライブラリを前提としたことからPythonとし、フレームワークとしてFlaskを用いています。

![TGLEシステム構成図](TGLE.jpg)

## Flask起動

次のコマンドで起動します。
tgle-be からは、ポート 9700　にてアクセスします。 
```
% sudo FLASK_APP=mkgroup.py flask run --debugger --reload --port 9700 --host 0.0.0.0
```
