from flask import Flask, jsonify, request, render_template

# Create a flask object
app = Flask(__name__)

stores = [
    {
        'name':'My Wonderful Store',
        'items':[
            {
                'name':'My item',
                'price':15.90
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

#POST /store data: {name:}
# Create a store using post method
@app.route('/store', methods=['POST'])
def create_store():
    # request made to end point
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    # Converted back to json
    return jsonify(new_store)

# GET/store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over the stores
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST/store/<string:name>/item {name:,price:}
@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    # request made to endpoint
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
    
            store['item'].append(new_item)
            # Converted back to json
            return jsonify(new_item)

# GET/store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'store not found'})        

# run the Flask app
app.run(port=5000)

