# endless_Poet

本リポジトリは[生成詩人A](https://boundless-voice-poet.com/)のリポジトリサンプルです。
実際に運用されている環境とは異なるため、参考程度にご覧ください。

## 使用技術

- Next.js（フロントエンド）
- Flask（バックエンド）
- redis
- AWS
- Docker
- nginx
- ChatGPT-1o-mini
- Ableton
- letsencrypt

## 構成

### フロントエンド
- Next.js を使用。
- バックエンドにポーリングして音声を取得。
- Google Analytics で分析。

### バックエンド
- Flaskを使用。
- 定期的に音声を更新・生成するコンテナとポーリングを対応するコンテナの2つ。

## 注意
[voicevox_Engine](https://github.com/VOICEVOX/voicevox_engine)を用いています。