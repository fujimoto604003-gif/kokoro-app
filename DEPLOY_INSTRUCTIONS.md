# デプロイ手順書 (Firebase Hosting + Cloud Run)

お使いの環境には `Node.js (Firebase CLI)` と `Google Cloud SDK (gcloud)` がインストールされていないようです。
以下の手順に従ってツールをインストールし、デプロイを行ってください。

## 1. ツールのインストール

### A. Firebase CLI のインストール
Node.js がないため、Windows用のスタンドアロンバイナリを使用します。
1.  [こちらをクリックしてインストーラをダウンロード](https://firebase.tools/bin/win/latest) (firebase-tools-instant-win.exe)
2.  ダウンロードしたファイルを実行して、ターミナル（コマンドプロンプト）で `firebase` コマンドが使えるようにします。

### B. Google Cloud SDK のインストール
1.  [Google Cloud SDK インストーラ](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe) をダウンロードして実行します。
2.  インストール完了後、ターミナルを再起動します。

---

## 2. デプロイの実行

ターミナル（PowerShell または Command Prompt）を新しく開き、プロジェクトフォルダ (`c:\Users\kido-\OneDrive\デスクトップ\VARY app`) に移動して、以下のコマンドを順番に実行してください。

### 手順 1: Google Cloud へのログインと設定
```powershell
# Google Cloudにログイン
gcloud auth login

# プロジェクトIDを設定 (作成したプロジェクトIDに置き換えてください)
# 例: kokoro-app-12345
gcloud config set project [YOUR_PROJECT_ID]
```

### 手順 2: Cloud Run へアプリをデプロイ
このコマンドで、DockerコンテナをビルドしてCloud Runにデプロイします。
```powershell
# サービス名: kokoro-app-service, 地域: asia-northeast1 (東京)
gcloud run deploy kokoro-app-service --source . --region asia-northeast1 --allow-unauthenticated
```
※ 途中で「APIを有効にしますか？」と聞かれたら `y` (Yes) を押してください。
※ 完了すると `Service URL: https://...` が表示されますが、まだアクセスしません。

### 手順 3: Firebase Hosting の設定とデプロイ
```powershell
# Firebaseにログイン
firebase login

# プロジェクトの選択（リストから選択するか、IDを入力）
firebase use --add

# Firebase Hostingへのデプロイ
firebase deploy --only hosting
```

完了すると `Hosting URL: https://...` が表示されます。これが公開URLです！
