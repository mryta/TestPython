import sqlite3

#DBファイル名
DB_NAME = 'example_data.db' 
TABLE_NAME = 'product_info'

def db_operation_example():
    """
    SQLite DBに接続し、データ登録と取得の基本操作を行います。
    """
    conn = None
    try:
        # --- 1. DB接続（ファイルが存在しなければ作成）---
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        print(f"✅ DB接続成功: {DB_NAME}")

        # --- 2. テーブル作成（SQL: CREATE TABLE） ---
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                tag_name TEXT NOT NULL,
                tag_value TEXT
            )
        """)
        print(f"✅ テーブル '{TABLE_NAME}' の作成または確認完了。")

        # --- 3. データ登録（SQL: INSERT INTO） ---
        
        # 登録するデータ (これはあなたの data_storage に相当します)
        new_data = [
            ('name', 'モジュール分離ツール'),
            ('version', '1.0.1'),
            ('comment', 'DB連携テストデータ')
        ]
        
        # SQL文の実行（executemanyで複数のデータをまとめて登録）
        # ? (プレースホルダー) を使うことで、SQLインジェクションを防ぎ安全に登録できます
        cursor.executemany(f"""
            INSERT INTO {TABLE_NAME} (tag_name, tag_value) VALUES (?, ?)
        """, new_data)
        
        conn.commit() # 変更を確定（コミット）
        print(f"✅ {len(new_data)} 件のデータを登録しました。")

        # --- 4. データ取得（SQL: SELECT） ---
        
        # テーブル内のすべてのデータ (全レコード) を取得するSQLを実行
        cursor.execute(f"SELECT tag_name, tag_value FROM {TABLE_NAME}")
        
        # 取得したデータをループで表示
        print("\n--- 取得結果 ---")
        fetched_records = cursor.fetchall()
        
        for record in fetched_records:
            tag, value = record # record はタプル (tag_name, tag_value)
            print(f"タグ名: {tag}, 値: {value}")
        
    except sqlite3.Error as e:
        print(f"❌ SQLiteエラーが発生しました: {e}")
    finally:
        # --- 5. DB接続の終了 ---
        if conn:
            conn.close()
            print("\n✅ DB接続を閉じました。")

if __name__ == "__main__":
    # 前回の実行結果をクリアしたい場合は、DBファイルを削除してから実行
    # if os.path.exists(DB_NAME):
    #     os.remove(DB_NAME)
        
    db_operation_example()