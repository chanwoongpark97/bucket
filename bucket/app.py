from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where();

client = MongoClient('mongodb+srv://test:sparta@cluster0.n2mmmxj.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]

    count = list(db.bucket.find({}, {'_id': False}))
    num = len(count) + 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷완료'})

@app.route("/bucket/cencel", methods=["POST"])
def bucket_cencel():
    num_receive = request.form['num_cencel']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '버킷취소'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)