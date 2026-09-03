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

Windows/Macともに、以下のコマンドで4096ビット長のRSA鍵を作成する。

```shell
ssh-keygen -t rsa -b 4096
```

ホームディレクトリの`.ssh`ディレクトリ内に生成された`id_rsa.pub`の内容をGitHubの「Settings」→「SSH and GPG keys」から登録する。`id_rsa`は秘密鍵なので公開しないこと。

</details>

## 課題テンプレートのダウンロード

講義中に指示する[GitHub Classroom](https://classroom.github.com/classrooms)の課題作成用URLにアクセスし、手順に従って課題用レポジトリを作成する。

### レポジトリのクローン

```shell
git clone git@github.com:tatsy-classes/sudoku-solver-username.git
```

`username`の部分は各自のGitHubアカウント名に読み替えること。

### 仮想環境の作成

```shell
python -m venv .venv
.venv/Scripts/activate       # Windows
source .venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

## 課題の作成

課題用レポジトリに含まれる`sudoku.py`を編集し、画像から数独問題を認識して、その問題を解くプログラムを作成する。ファイル名は変更しないこと。

今回の課題では、処理を次の2段階に分ける。

```text
image
  ↓
recognize(image, level)
  ↓
problem
  ↓
solve(problem)
  ↓
answer
```

### `recognize(image, level)`

画像から元の9x9の数独問題を認識する。

```python
def recognize(image, level) -> np.ndarray:
    ...
```

返り値は`dtype=np.int32`, `shape=(9, 9)`のNumPy配列とする。

- `1`〜`9`: 認識した数字
- `0`: 空欄、または数字はあるが認識に自信がないセル

無理に数字を推測して間違えるより、分からないセルを`0`として返してよい。後段の`solve()`では、数独の制約を利用して認識結果の欠落や矛盾を補う工夫を行ってもよい。

### `solve(problem)`

`recognize()`が返した9x9配列から完成盤面を求める。

```python
def solve(problem) -> np.ndarray:
    ...
```

返り値は`dtype=np.int32`, `shape=(9, 9)`で、全セルが`1`〜`9`の完成盤面になっている必要がある。

採点時も必ず`recognize()`の返り値がそのまま`solve()`へ渡される。`solve()`から元画像を直接参照することはできない。

## 難易度について

課題にはLevel 1〜3がある。

- **Level 1**: 基本的な画像
- **Level 2**: Level 1より難しい画像
- **Level 3**: challenge level

Level 2まで十分に処理できれば、この課題としては良好な達成度である。Level 3まで高精度に処理できればかなり良い結果と考えてよい。

## 採点方法

採点は **Recognition 60点 + Final 60点 = 合計120点** で行う。

### Recognition: 最大60点

hidden画像10枚について、元の問題をどれだけ正しく認識したかをLevelごとにmicro F1で評価する。

- TP: 正しい数字を正しく認識
- FP: 非0を出力したが正解と異なる
- FN: 本来数字があるが正解と一致しない

別の数字へ誤認した場合はFP=1かつFN=1として数える。

```text
F1 = 2 TP / (2 TP + FP + FN)
```

各LevelでF1が0.2, 0.4, 0.6, 0.8, 1.0以上になるたびに加点される。

| Level | 1 thresholdあたり | 最大 |
|---|---:|---:|
| 1 | 2点 | 10点 |
| 2 | 4点 | 20点 |
| 3 | 6点 | 30点 |

### Final: 最大60点

Recognitionの出力を`solve()`へ渡して得られた完成盤面を、hidden画像ごとに採点する。

| Level | 1問あたり | 10問合計 |
|---|---:|---:|
| 1 | 1点 | 10点 |
| 2 | 2点 | 20点 |
| 3 | 3点 | 30点 |

## テスト方法

`data`ディレクトリのサンプル画像を利用してローカルテストできる。講義中に案内する追加サンプルも利用してよい。

```shell
pytest
```

RecognitionのF1を表示したい場合は、標準出力を表示して実行する。

```shell
pytest -s -k recognition
```

Finalのみ確認したい場合は、

```shell
pytest -k final
```

とする。

## サーバー上でのテスト方法

`sudoku.py`の変更をGitHubへコミット・プッシュするとGitHub Actionsによる自動採点が実行される。

```shell
git status -u
git add -u
git add "/file/name/you/wanna/track"  # 必要な場合のみ
git commit -m "コミットコメント"
git push origin main
```

**注意:** 作成した大規模なデータセットはレポジトリへアップロードしないこと。

### 実行時間の制約

実行時間は**1画像当たり最大15秒**である。各画像は独立したプロセスで評価されるため、ある画像でタイムアウトやエラーが発生しても、他の画像の採点は継続される。

## 課題の提出方法

プログラムの作成が終了したら、Google Classroomから、

- 採点してほしいコミットのSHA値
- 取組内容を説明したレポート (目安A4用紙1枚程度、PDFまたはMicrosoft Word)

の2つを提出する。

コミットのSHA値の取得方法については、講義資料中の[SHA値の取得方法](https://tatsy.github.io/1284-sds-advml/contents/appendix/submit-assignment.html#sha)を参照のこと。
