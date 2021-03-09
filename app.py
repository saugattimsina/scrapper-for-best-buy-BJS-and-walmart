from flask import Flask,render_template,request,jsonify
import get_price



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/response', methods = ['POST', 'GET'])
def getting_file():
    if request.method == "POST":
        
        m = request.get_json()
        keys = list(m.keys())
        

        needed_string_query = m[keys[0]]
        info_data = get_price.get_modelPrices(needed_string_query)
        info_data["place"] = keys[0]
        print(info_data)

        return jsonify(info_data)
    
    return "error in code"

if __name__ == '__main__':    
    app.run(host="0.0.0.0")


    
