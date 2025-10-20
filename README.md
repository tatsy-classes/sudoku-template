# 数独ソルバーの作成

<details>
<summary>

## 準備 (全課題共通)

</summary>

### GitHubのアカウントを作成

<https://github.com/>にアクセスしてアカウントを作成する。

### Gitクライアントのインストール (Windows向け)

Windowsの場合にはGitが最初からインストールされていないので、

- [Git for Windows](https://gitforwindows.org/)

を各自のコンピュータにインストールする。インストール後、コマンドプロンプトかPowerShellを実行して、

- `git`
- `ssh-keygen`

の2つのコマンドが認識されれば成功。

### SSHキーの登録

現在、GitHubはSSHの認証鍵を使わないとプライベートレポジトリをダウンロードできないので、SSHキーをGitHubアカウントに登録する。

Windows/Macともに、以下のコマンドで4096ビット長のRSA鍵を作成する。

```shell
ssh-keygen -t rsa -b 4096
```

途中、パスワードの入力などを求められるが、特に不要なら入力する必要はない。

コマンドが正しく実行されると、ホームディレクトリの`.ssh`ディレクトリ内に`id_rsa`と`id_rsa.pub`の二つのファイルが生成される。この二つのうち、`id_rsa`の方は秘密鍵、`id_rsa.pub`の方は公開鍵のファイルである。サーバーに登録して良いのは公開鍵の方。

公開鍵のファイル`id_rsa.pub`を何らかのエディタで開いて、その内容をコピーする。GitHubに移動し、右上のユーザアイコンをクリックし「Settings」を選ぶ。その後、「SSH and GPG keys」を左のメニューから選び、「SSH Keys」の右にある「New SSH key」ボタンを押して、現れるテキストボックスに先ほど`id_rsa.pub`からコピーした内容を貼り付けて、「Add SSH key」を押す。

</details>

## 課題テンプレートのダウンロード

講義中に指示する[GitHub Classroom](https://classroom.github.com/classrooms)の課題作成用URLにアクセスし、手順に従って、課題用のレポジトリである`sudoku-solver-username`が作成される (`username`の部分は各自のGitHubアカウント名に読み替えること)。

### レポジトリのクローン

再び、ローカルの環境に戻り、WindowsならコマンドプロンプトかPowerShell, Macならターミナルを開いて、**Gitレポジトリをクローン**する。正しく、公開鍵が登録されていれば、以下のコマンドでレポジトリがクローンされる。

```shell
# Gitレポジトリのクローン
git clone git@github.com:tatsy-classes/sudoku-solver-username.git
```

### 仮想環境の作成

適当な方法で開発用の仮想環境を作成し、Pipで必要なモジュールをインストールする。以下では`.venv`というディレクトリにvenvの仮想環境を作る方法を示す。

```shell
# 仮想環境の作成
python -m venv .venv
# 仮想環境の切り替え
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Mac/Linux
# モジュールのインストール
pip install -r requirements.txt
```

## 課題の作成


### ソルバー関数の編集

課題用レポジトリに含まれる `sudoku.py`を編集(**ファイル名は変更しないこと**)して、正しい数独の解が得られるプログラムに修正する。

### テスト方法

`data`ディレクトリの中に1枚ずつサンプルの画像が入っているのでそれを利用して良い。また、講義の参加者には`data/samples.zip`の展開用パスワードを指示するので、このZIPファイルに含まれる各レベル5枚のサンプル画像も合わせて使用して良い。準備ができたら、`pytest`を使ってテストを実行する。

```shell
# 汎用的なテスト
pytest 
# 実行状況を細かく表示する場合
pytest --tb=long
```

### サーバー上でのテスト方法

`sudoku.py`に行った編集をGitHub上のレポジトリにコミット、プッシュすると、GitHub Actionsの機能を用いて自動採点が実施される。変更をコミット、プッシュするためのコマンドの一例は以下の通り。

```shell
# リポジトリのルートディレクトリで以下を実行する
# -----
## ローカルの更新状況を確認
git status -u
## ローカルの変更をGitの履歴に反映
git add -u
## 必要に応じて自分で作成したファイルも追加
git add "/file/name/you/wanna/track"
## コミット
git commit -m "コミットコメント (適宜更新内容を入力)"
## プッシュ
git push origin master
```

**注意:** 作成したデータセットはレポジトリのファイルサイズ制限に引っかかるのでアップロードしないこと。

### 実行時間の制約

実行時間は1問当たり最大15秒に設定してある。それ以上が経過すると、自動的にプログラムが終了するので注意すること。

## 課題の提出方法

プログラムの作成が終了したら、Google Classroomから、

- 採点してほしいコミットのSHA値
- 取組内容を説明したレポート (目安A4用紙1毎程度. PDF, Microsoft Wordのいずれか)

の2つを提出する。

コミットのSHA値の取得方法については、講義資料中の[SHA値の取得方法](https://tatsy.github.io/1284-sds-advml/contents/appendix/submit-assignment.html#sha)を参照のこと。
