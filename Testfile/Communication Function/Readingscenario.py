def read_scenario(filepath):
   print(f"'{filepath}'の読み込みを開始")

   #ファイルの読み込み処理
   try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()] 
        
        print(f"--- [Reader] {len(lines)} 行のデータを読み込み完了 ---")
        return lines

    # エラーの表示
   except FileNotFoundError:
        print(f"ファイルが見つかりません: {filepath}")
    
        return []