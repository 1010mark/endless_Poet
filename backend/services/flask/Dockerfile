FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを/apiに設定
WORKDIR /api

# 現在のディレクトリの内容をコンテナ内の/apiにコピー
COPY ./services/flask /api
COPY ./tools /api/tools

# requirements.txtで指定された必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ポートの公開
EXPOSE 5001

# コンテナ起動時にapp.pyを実行
CMD ["python", "app.py"]