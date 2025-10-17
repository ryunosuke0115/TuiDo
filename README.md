# TuiDo

## Requirements
- Python 3.11.7 ~
- Textual 6.10.0

## Setup
### 依存パッケージのインストール

プロジェクトディレクトリで下記のコマンドを実行し，必要な依存パッケージをインストールする．
``` bash
pip install -r requirements.txt
```

### コマンドのパスを設定

パスを通した任意のディレクトリ内に tuido の実行ファイル (todo) へのシンボリックリンクを作成する．

``` bash
export PATH=path/to/your/directory:$PATH
cd your/directory
ln -s path/to/TuiDo/todo todo
```
以下に設定例を示す．

``` bash
export PATH=$HOME/.local/bin:$PATH #(.bashrc or .zshrc に追加することで，設定を永続化)
cd ~/.local/bin
ln -s ~/git/TuiDo/todo todo
```

## Usage
### 初回起動時
#### 新規ユーザ登録
TuiDo のアカウントを所持していない場合，以下の手順で新しいアカウントを作成可能である．
1. 起動時，`Do you have an account? (y/n): ` と聞かれるので `n` を入力し `Enter` を押す．
``` bash
Do you have an account? (y/n): n
```

2. 登録に使用するメールアドレスをパスワードを入力する．入力したパスワードは表示されない．
``` bash
Email: your-email@example.com
Password (at least 6 characters):
```

3. アカウントが作成されると，入力したメールアドレスに認証メールが送信される．
``` bash
Sent a verification email to your email address.
Please login again after verifying your email.
```
- アプリは一度終了する．メールを確認し，記載されたリンクをクリックしてメールアドレスの認証を完了させる必要がある．その後，再度 TuiDo を起動して `既存ユーザのログイン` に進む．


#### 既存ユーザのログイン
既に TuiDo のアカウントを所持している場合，以下の手順でログインできる．
1. 起動時，`Do you have an account? (y/n): ` と聞かれるので `y` を入力し `Enter` を押す．
``` bash
Do you have an account? (y/n): y
```

2. 登録済みのメールアドレスとパスワードを入力する．
``` bash
Email: your-email@example.com
Password (at least 6 characters):
```

3. 認証に成功すると次回以降の自動ログインのため，`credentials/user.json` にログイン情報が保存される．


### 次回以降の起動時
- 初回ログインに成功すると，次回以降の起動時には `credentials/user.json` に保存されたログイン情報を使用して自動的にログインされる．

### 表示について
TuiDo を起動すると，左右に2つのテーブルが表示される．
画面左側には，3つのタブが存在する．対応を以下に示す．
- TODO … 未完了タスク
- DONE … 完了タスク
- TAGS … タグ

画面右側には，タスク/タグの詳細が表示される．

### 基本操作
|キー|説明|
|---|---|
|`↑` or `k`|上へ移動|
|`↓` or `j`|下へ移動|
|`←` or `h`|左へ移動|
|`→` or `l`|右へ移動|
|`q`|終了|
|`Esc`|一つ戻る|
|`Enter`|決定|
|`Ctrl + s`|操作を保存する|
|`Ctrl + r`|タスク/タグ 一覧の更新|
|`i`|タスク/タグ の新規作成|
|`e`|タスク/タグ の編集|
|`d`|タスク/タグ の削除|
|`f`|タスク/タグ の検索|
|`space`|タスクの 完了/未完了 切り替え or 選択したタグで検索|
|`Ctrl + p`|コマンドパレット (テーマなどが変更可能)|
