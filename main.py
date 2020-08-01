from flask import Flask, render_template, request
import os

app = Flask(__name__)

# 10進-->2進変換 (整数部, 小数部それぞれ8bit)
def dectobin(target):
    # target を整数部と小数部に分ける
    i = int(target)
    f = target - i

    # 整数部を2進数に変換する
    a = []      # 余りを入れるリスト=2進の整数部
    c = []      # 商を入れるリスト
    n = 0       # 繰り返した回数
    while n < 8:
        a.append(i % 2)   # 余り
        c.append(i)
        i = i //2           # 商
        n += 1
    
    # 要素を逆順にする
    # a.reverse()

    # 小数部を2進数に変換
    b = []      # かけた後の整数部を入れるリスト=2進の小数部
    d = []      # かけた後の小数部を入れるリスト
    n = 0       # 繰り返した回数
    while n < 8:
        temp = f * 2        # 小数部*2
        b.append(int(temp)) # かけた後の整数部
        d.append(round(f,9))
        f = temp - int(temp)
        n += 1
        if (n >= 10):
            break
    
    return a, b, c, d


# 2進-->10進変換 ('0','1','.' 以外の入力、整数部,小数部それぞれ8ケタを超える、場合はFalseを返す)
def bintodec(target2):
    # 入力をstrに変換
    target2 = str(target2)

    # 17ケタを超える、または、ピリオドが1つを超える、または、'0','1','.' 以外が入力されている場合は Falseを返す
    if len(target2) > 17 or target2.count('.') > 1 or len(target2) != (target2.count('0') + target2.count('1') + target2.count('.')):
        return False

    else:
        # 2進の各桁のリストを用意、入力文字をリストに1文字ずつ入れる
        e = []
        for x in range(len(target2)):
            e.append(target2[x])

        # '.'があるか判定、無ければリスト末尾に追加
        if '.' not in e:
            e.append('.')

        # 整数部、小数部が8桁を超えている場合は Falseを返す
        if e.index('.') > 8 or e.index('.') < len(e) - 9:
            return False
        
        else:
            # '.' 以外を数字にする
            for x in range(len(e)):
                if e[x] != '.':
                    e[x] = int(e[x])

            # '.' が e[8]になるまでリスト先頭に 0 を追加、追加後'.'を削除
            while e.index('.') != 8:
                e.insert(0, 0)
                if e.index('.') >= 8:
                    break
            e.remove('.')

            # 各ケタに重みをかけて合計を求める
            f = []
            g = 0.0
            for x in range(len(e)):
                f.append(e[x] * 2**(7-x))
                g += f[x]
            
            return e, f, g


@app.route('/')
def hello():
    name = "Hello Python!"
    return name

@app.route('/good')
def good():
    name = "Routing fanction is working"
    return name

@app.route('/form2', methods = ['POST', 'GET'])
def form():
   return render_template('form2.html')

# 10進-->2進のリクエスト
@app.route('/confirm2', methods = ['POST', 'GET'])
def confirm2():
   if request.method == 'POST':
      result = request.form
      try:
            target = float(request.form["Dec"])
            if target < 0 or target > 255 :
                return render_template("form3.html", Error_num=2)
            Dec_int = int(target)
            Dec_fra = round(target - Dec_int, 9)
            Bin_int8 = dectobin(target)[0]    # 固定小数点2進数 整数部8bit
            Bin_fra8 = dectobin(target)[1]    # 固定小数点2進数 小数部8bit
            num_1 = dectobin(target)[2]       # 整数部の計算過程で商を入れるリスト
            num_2 = dectobin(target)[3]       # 小数部の計算でかけた後の小数部を入れるリスト
            return render_template("confirm2.html",result = result, target=target, 
            Dec_int=Dec_int, Dec_fra=Dec_fra, Bin_int8=Bin_int8, Bin_fra8=Bin_fra8, 
            num_1=num_1, num_2=num_2)
      except:
          return render_template("form3.html", Error_num=2)

# 2進-->10進のリクエスト
@app.route('/confirm3', methods = ['POST', 'GET'])
def confirm3():
   if request.method == 'POST':
      result = request.form
      try:
            target2 = str(request.form["Bin"])
            Bin_list = bintodec(target2)[0]     # 元の2進数の各桁リスト
            Dec_sep = bintodec(target2)[1]      # 重みをかけた後の各桁リスト
            Dec_sum = round(bintodec(target2)[2], 9)    # 10進変換後の数値
            return render_template("confirm3.html" ,result = result, target2=target2, 
            Bin_list=Bin_list, Dec_sep=Dec_sep, Dec_sum=Dec_sum )
      except:
          return render_template("form3.html", Error_num=3)


if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)