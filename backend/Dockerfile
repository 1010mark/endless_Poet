# 親イメージはpython。voicevoxと揃えてUbuntuを導入することも考慮したが、余計な圧迫を避けた。
FROM python:3.11

# 作業ディレクトリを/appに設定
WORKDIR /api

# 現在のディレクトリの内容をコンテナ内の/appにコピー
COPY . /api

# requirements.txtで指定された必要なパッケージをインストール
RUN pip install -r requirements.txt

# ポートの公開
EXPOSE 8080

# コンテナ起動時にapp.pyを実行
CMD ["python", "app.py"]