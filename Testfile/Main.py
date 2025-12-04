import tkinter as tk
from tkinter import messagebox

# ----------------------------------------------------
# 状態管理変数
# ----------------------------------------------------
# StringVar: Tkinterでウィジェット（Labelなど）の表示内容を動的に変更するための変数
display_var = tk.StringVar()
display_var.set("0") # 初期値は "0"

current_input = ""  # 現在入力中の文字列（次のオペランド）
first_number = None # 最初のオペランド（計算対象の数値）
operator = None     # 演算子（'+', '-', '*', '/'）

# ----------------------------------------------------
# 計算ロジック関数
# ----------------------------------------------------
def calculate(num1, op, num2):
    """計算を実行する関数"""
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        # ゼロ除算の例外処理は呼び出し元で行う
        return num1 / num2
    return num2 # ありえないケース

def display_update(text):
    """ディスプレイの表示を更新する関数"""
    # 結果が float で .0 が付く場合は整数として表示する
    try:
        if float(text) == int(float(text)):
            text = str(int(float(text)))
    except ValueError:
        # floatに変換できない文字列（例: 演算子記号など）は何もしない
        pass

    display_var.set(text)

# ----------------------------------------------------
# ボタンクリックイベントハンドラ
# ----------------------------------------------------
def button_click(text):
    """全てのボタンからの入力を処理するメイン関数"""
    global current_input, first_number, operator

    # 4. クリアキー (C) の処理
    if text == 'C':
        current_input = ""
        first_number = None
        operator = None
        display_update("0")
        return

    # 1. 数字キーと小数点キーの処理
    if text.isdigit() or text == '.':
        # current_inputが空の状態で '.' が押された場合 "0." を表示する
        if text == '.' and current_input == "":
            current_input = "0."
        # 初期値 "0" の状態から数字が入力されたら "0" をクリア
        elif current_input == "" and text != '.':
            current_input = text
        # 小数点が既に含まれている場合は追加しない
        elif text == '.' and '.' in current_input:
            pass
        else:
            current_input += text

        display_update(current_input)
        return

    # 2. 演算子キー ('+', '-', '*', '/') の処理
    elif text in ('+', '-', '*', '/'):
        # 連続して演算子を押した場合、演算子を上書きする
        if first_number is not None and operator is not None and current_input == "":
            operator = text
            # 演算子を一時的に表示して次の入力を待つ（オプション）
            display_update(text)
            return

        # 最初の数値が未設定で、かつ現在の入力があれば
        if first_number is None and current_input != "":
            try:
                # 入力された文字列をfloatに変換し、最初の数値として保存
                first_number = float(current_input)
                operator = text
                current_input = "" # 入力文字列をリセットし、次の数値を待つ
                display_update(text) # 演算子を表示
            except ValueError:
                messagebox.showerror("エラー", "不正な入力です")
                button_click('C')
                return
            return

    # 3. 等号キー (=) の処理
    elif text == '=':
        # 最初の数値、演算子、次の入力（2番目の数値）が揃っていることを確認
        if first_number is not None and operator is not None and current_input != "":
            try:
                second_number = float(current_input)

                # ゼロ除算のチェック
                if operator == '/' and second_number == 0:
                    messagebox.showerror("エラー", "ゼロで割ることはできません")
                    button_click('C')
                    return

                # 計算実行
                result = calculate(first_number, operator, second_number)

                # 結果を表示
                display_update(str(result))

                # 次の計算のために状態をリセット
                first_number = result # 結果を次の計算の最初の数値として保持 (連鎖計算対応)
                operator = None
                current_input = "" # 次の新しい入力を待つ
            except ValueError:
                messagebox.showerror("エラー", "不正な入力です")
                button_click('C')
            return


# ----------------------------------------------------
# GUI設定とウィジェット配置
# ----------------------------------------------------

# ルートウィンドウの作成
root = tk.Tk()
root.title("Python GUI 電卓")
root.geometry("400x500") # ウィンドウのサイズを電卓らしく設定

# --- 1. 表示エリア（ディスプレイ）の配置 ---
display_label = tk.Label(root, textvariable=display_var, font=("Arial", 36),
                         anchor="e", # 右寄せ
                         bg="#333333", # 背景色
                         fg="white", # 文字色
                         padx=20, pady=20)
# grid(row=0, column=0)から4列分をまたいで（columnspan=4）配置
display_label.grid(row=0, column=0, columnspan=4, sticky="nsew")


# --- 2. ボタンの定義と配置 ---
buttons = [
    ('C', 1, 0), ('/', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2),
]

# ボタンの色設定
def get_button_color(text):
    if text in ('+', '-', '*', '/', '='):
        return "#FF9900" # 演算子
    elif text == 'C':
        return "#AAAAAA" # クリア
    else:
        return "#CCCCCC" # 数字・小数点

for (text, row, col) in buttons:
    # 0ボタンを2列分に広げる
    columnspan = 2 if text == '0' else 1
    col = 0 if text == '0' else col

    button_bg = get_button_color(text)

    # commandに引数付きの関数を設定するためには lambda を使用します
    button = tk.Button(root, text=text, font=("Arial", 20, "bold"),
                       bg=button_bg, fg="black", # 色設定を適用
                       command=lambda t=text: button_click(t))

    button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=2, pady=2)


# --- 3. ウィンドウの行と列の重み付け設定 ---
# これにより、ウィンドウのサイズを変更したときにボタンやディスプレイが拡大・縮小するようになります
for i in range(6): # row 0（ディスプレイ）から row 5（最後のボタン）まで
    root.grid_rowconfigure(i, weight=1)
for i in range(4): # column 0 から column 3 まで
    root.grid_columnconfigure(i, weight=1)

# ----------------------------------------------------
# アプリケーションの実行
# ----------------------------------------------------
root.mainloop()