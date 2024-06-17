from flask import Blueprint, json, request, render_template
from ..extensions import client

db = client['Techstax']['records']
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook', template_folder='templates')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        print('inside receiver')
        data=request.json
        #print(data)
        try:
            db_item = {'request_id':'','author':'', 'action':'', 'from_branch':'', 'to_branch':'', 'timestamp':'', 'message':''}
            if ('action' in data) and (data['action'] is not None):

                if 'pull_request' in data:
                    if data['action']=='closed':
                        if data['pull_request']['merged_at'] is not None:
                            action = data['pull_request']['merged_by']['login'] +' merged branch from '+data['pull_request']['head']['ref']+' to '+data['pull_request']['base']['ref']+' on '+data['pull_request']['merged_at']
                            db_item['request_id'] = data['pull_request']['id']
                            db_item['author'] = data['pull_request']['merged_by']['login']
                            db_item['action'] = 'MERGE'
                            db_item['from_branch'] = data['pull_request']['head']['ref']
                            db_item['to_branch'] = data['pull_request']['base']['ref']
                            db_item['timestamp'] = data['pull_request']['merged_at']
                            db_item['message'] = action
                            db.insert_one(db_item)
                            
                        else:
                            action = data['pull_request']['head']['label'].split(':')[0] + ' closed a pull request from ' + data['pull_request']['head']['ref'] + ' to ' + data['pull_request']['base']['ref'] + ' on ' + data['pull_request']['closed_at']
                            db_item['request_id'] = data['pull_request']['id']
                            db_item['author'] = data['pull_request']['head']['label'].split(':')[0]
                            db_item['action'] = 'PULL_REQUEST'
                            db_item['from_branch'] = data['pull_request']['head']['ref']
                            db_item['to_branch'] = data['pull_request']['base']['ref']
                            db_item['timestamp'] = data['pull_request']['closed_at']
                            db_item['message'] = action
                            db.insert_one(db_item)

                    elif data['action']=='opened':
                        if ('opened_at' in data['pull_request'].keys()) and (data['pull_request']['opened_at'] is not None):
                            action = data['pull_request']['head']['label'].split(':')[0] + ' submitted a pull request from ' + data['pull_request']['head']['ref'] + ' to ' + data['pull_request']['base']['ref'] + ' on ' + data['pull_request']['opened_at']
                            db_item['request_id'] = data['pull_request']['id']
                            db_item['author'] = data['pull_request']['head']['label'].split(':')[0]
                            db_item['action'] = 'PULL_REQUEST'
                            db_item['from_branch'] = data['pull_request']['head']['ref']
                            db_item['to_branch'] = data['pull_request']['base']['ref']
                            db_item['timestamp'] = data['pull_request']['opened_at']
                            db_item['message'] = action
                            db.insert_one(db_item)
                        else:
                            action = data['pull_request']['head']['label'].split(':')[0] + ' submitted a pull request from ' + data['pull_request']['head']['ref'] + ' to ' + data['pull_request']['base']['ref'] + ' on ' + data['pull_request']['created_at']
                            db_item['request_id'] = data['pull_request']['id']
                            db_item['author'] = data['pull_request']['head']['label'].split(':')[0]
                            db_item['action'] = 'PULL_REQUEST'
                            db_item['from_branch'] = data['pull_request']['head']['ref']
                            db_item['to_branch'] = data['pull_request']['base']['ref']
                            db_item['timestamp'] = data['pull_request']['created_at']
                            db_item['message'] = action
                            db.insert_one(db_item)

            elif ('pusher' in data) and (data['pusher'] is not None):
                action = data['pusher']['name']+' pushed to '+data['ref'].split('/')[-1]+' on '+data['commits'][0]['timestamp']
                db_item['request_id'] = data['commits'][-1]['id']
                db_item['author'] = data['pusher']['name']
                db_item['action'] = 'PUSH'
                db_item['from_branch'] = ''
                db_item['to_branch'] = data['ref'].split('/')[-1]
                db_item['timestamp'] = data['commits'][0]['timestamp']
                db_item['message'] = action
                db.insert_one(db_item)
            if action:
                print(action)
        except:
            pass
    return {}, 200

@webhook.route('/display')
def home():
    data=[]
    cursor = db.find({})
    for i in cursor:
        data.append(i)
    return render_template('webhook/home.html', data=data)
