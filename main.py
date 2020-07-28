from flask import Flask, render_template, request
import os

app = Flask(__name__)

# 10進-->2進変換
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


@app.route('/')
def hello():
    name = "Hello Python!"
    return name

@app.route('/good')
def good():
    name = "Routing fanction is working"
    return name

@app.route('/form2')
def form():
   return render_template('form2.html')

@app.route('/confirm2', methods = ['POST', 'GET'])
def confirm():
   if request.method == 'POST':
      result = request.form
      target = float(request.form["Dec"])
      Dec_int = int(target)
      Dec_fra = round(target - Dec_int, 9)
      Bin_int8 = dectobin(target)[0]    # 固定小数点2進数 整数部8bit
      Bin_fra8 = dectobin(target)[1]    # 固定小数点2進数 小数部8bit
      num_1 = dectobin(target)[2]       # 整数部の計算過程で商を入れるリスト
      num_2 = dectobin(target)[3]       # 小数部の計算でかけた後の小数部を入れるリスト
      return render_template("confirm2.html",result = result, target=target, 
      Dec_int=Dec_int, Dec_fra=Dec_fra, Bin_int8=Bin_int8, Bin_fra8=Bin_fra8, 
      num_1=num_1, num_2=num_2)
    

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)