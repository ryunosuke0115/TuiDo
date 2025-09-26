# TuiDo

## Requirements
- Python 3.11.7 ~
- Homebrew 4.6.9 ~
- Supabase CLI 2.39.2
- Textual 6.10.0
- python-dotenv 1.1.1

## Setup
### 依存パッケージのインストール

プロジェクトディレクトリで下記のコマンドを実行し，必要な依存パッケージをインストールする．
``` bash
pip install -r requirements.txt
```
``` bash
brew install supabase/tap/supabase
```

### Supabase での新規プロジェクトを作成
1. [Supabase](https://supabase.com/) にアクセスし，アカウントを作成する．
2. `Start your project` -> `+ New organization` の順に押し，新規 organization を作成する．
3. 作成した organization を選択し，`+ New Project` を押す．
4. `Project name`，`Database password`，`Region` を入力し，新規プロジェクトを作成する．

### 使用するテーブルの作成
1. ターミナルから Supabase にログインする．
``` bash
supabase login
```
- これ以降の操作はパスワードが求められるため，以下のコマンドを実行することでパスワードの入力を省略できる．
    ``` bash
    export SUPABASE_DB_PASSWORD=<your-db-password>
    ```

2. 先ほど作成したプロジェクトと接続する．
``` bash
supabase link --project-ref <your-project-id>
```
- your-project-ref は `Project` -> `Project Settings` から取得可能．

3. マイグレーションファイルを作成する．
``` bash
supabase migration new setup_table
cp database/setup-table.sql supabase/migrations/<new-migration.sql>
```
4. ローカルにあるマイグレーションファイルをリモートに反映する．
``` bash
supabase db push
```

### 設定ファイルの作成
1.  以下のコマンドを実行し，.env.sample を .env に変更する．
``` bash
cp .env.sample .env
```
2. `Project` -> `Project Settings` -> `Data API` から `Project URL` を，`Project` -> `Project Settings` -> `API Key` -> `API Keys` -> `Legacy API Keys` から `API Key` を取得する．
3. .env の SUPABASE_URL と SUPABASE_KEY をそれぞれ自身の情報に書き換える．

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
### 表示について
tuido を起動すると，左右に2つのテーブルが表示される．
画面左側には，3つのタブが存在する．対応を以下に示す．
- PENDING … 未完了タスク
- COMPLETED … 完了タスク
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
|`f`|タスク/タグ の検索 (今後実装予定)|
|`space`|タスクの 完了/未完了 切り替え|
|`Ctrl + p`|コマンドパレット (テーマなどが変更可能)|
