# Slide Generator

論文のPDFファイルからスライドを生成するプログラムです。

## 事前準備

1. OpenAIのAPIキーを取得

  - 以下のサイト(OpenAI API)に登録して、OpenAIのAPIキーを取得してください。
  - [OpenAI API](https://openai.com/index/openai-api/)

2. LaTeXコンパイラのインストール

  - 以下の方法に従って、LaTeXコンパイラをインストールしてください。

### Windowsの場合
1. [MiKTeX](https://miktex.org/download)をダウンロードしてインストールします。
2. インストール後、環境変数にMiKTeXのパスが追加されていることを確認します。

### Macの場合
1. ターミナルを開き、以下のコマンドを実行します。
```
brew install mactex
```

### Linuxの場合
1. ターミナルを開き、以下のコマンドを実行します。
```
sudo apt-get update
sudo apt-get install texlive-full
```

3. パッケージのインストール

  - requirements.txtに従って、必要なpythonパッケージをインストールしてください。

4. .envファイルの作成

  - 以下の形式に従って、.envファイルをslide_generator直下に作成してください。
```
OPENAI_API_KEY=[OpenAIのAPIキー]
```

5. resourcesディレクトリの作成

  - resourcesディレクトリをslide_generator直下に作成してください。

## 実行方法

1. スライドを作成したい論文をresourcesディレクトリに格納します。

  - "タイトル名.pdf"という名前で保存してください。

2. scriptsディレクトリに移動し、以下のコマンドを実行します。
```
python main.py --paper=タイトル名
```
