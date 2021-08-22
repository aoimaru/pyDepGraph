- PIPで管理されているライブラリの依存関係を取得

```bash
#イメージのビルド Dockerfileがあるディレクトリで実行してください
#ビルドに失敗した場合は, submit:0.1を0.2などに変更して, 再度ビルドしてください
$ docker build -t submit:0.1 .

#コンテナの起動
$ docker run --name ["コンテナ名] -p 8050:8050 ["イメージ名":"タグ名"]
$ docker run --name demo -p 8050:8050 submit:0.1

#ブラウザでのアクセス
http://0.0.0.0:8050/ にアクセスしてください

# [ramdom, grid, circle, concentric, breadthfirst, cose]の6種類の形で確認することができます.

#コンテナの削除
$ docker rm demo

#イメージの削除
$ docker rmi submit:0.1
```
