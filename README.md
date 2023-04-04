# TGLE MKGROUP

## 概要

バックエンドからREST APIにて、教員および学生のキーワードを取得し、教員および学生のキーワードのペアをSimilarity計算サービスにRequestし、ResponseとしてペアとなるキーワードのSimilarityを得ます。実装はSimilarityマトリックスを操作するためにNumPyライブラリを前提としたことからPythonとし、フレームワークとしてFlaskを用いています。

![TGLEシステム構成図](TGLE.jpg)

