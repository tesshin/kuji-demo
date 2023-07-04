from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# 定義する賞のリスト
special_prizes = ['S賞_1', 'S賞_2', 'S賞_3']
normal_prizes = ['通常賞_' + str(i+1) for i in range(20)]
all_prizes = special_prizes + normal_prizes  # 全ての賞のリスト

@app.route('/')
def home():
    # ホームページをレンダリング
    return render_template('index.html')

@app.route('/draw')
def draw():
    # クライアントから送信される抽選回数の取得
    times = int(request.args.get('times', 1))
    
    # 抽選回数が全賞の種類数を超える場合はエラーメッセージを返す
    if times > len(all_prizes):
        return jsonify({'error': 'You cannot draw more times than the total number of prizes'})
        
    prizes = []  # 抽選結果を格納するリスト
    remaining_prizes = all_prizes[:]  # 残りの賞を追跡するためのリスト（初期状態では全ての賞が含まれる）
    
    # 抽選を指定回数分行う
    for _ in range(times):
        prize = single_draw(remaining_prizes)  # 残りの賞から一つを選ぶ
        prizes.append(prize)  # 選ばれた賞を結果リストに追加
        remaining_prizes.remove(prize)  # 選ばれた賞を残りの賞のリストから削除
    return jsonify({'prizes': prizes})  # 抽選結果をJSON形式で返す

def single_draw(remaining_prizes):
    # 残りの賞から一つをランダムに選ぶ
    draw_result = random.choices(
        population=remaining_prizes,
        weights=[2/100 if prize in special_prizes else 4.7/100 for prize in remaining_prizes],
        k=1
    )
    return draw_result[0]  # 選ばれた賞を返す

if __name__ == '__main__':
    app.run(debug=True)  # アプリケーションの起動
