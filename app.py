# Mark Black (mark@fnord.foundation)
# 4 December 2020

from bottle import route, request, run
import json
from datetime import datetime
import time


# set initial state
state = dict()
state['users'] = [
    {
        'user': 'homer', 
        'points': []
    }
]

@route('/v1/points/<username>') # GET
def get_points(username):
    user = next((user for user in state['users'] if user['user'] == username), None)
    if type(user) == type(None): # make sure the user exists
        return json.dumps({'error': 'User not found!'})
    points = sum([point['value'] for point in user['points']])
    # sum points for each company
    companies = set([point['company'] for point in user['points']])
    overview = dict()
    for company in companies:
        overview[company] = dict()
        # overview[company]['company'] = company
        matches = [point for point in user['points'] if point['company'] == company]
        # sum matches
        points_for_company = sum([int(points['value']) for points in matches])
        overview[company]['points'] = points_for_company

    return json.dumps(overview)

@route('/v1/points/<username>', method='POST')
def alter_points(username):
    user = next((user for user in state['users'] if user['user'] == username), None)
    if type(user) == type(None): # make sure the user exists
        return json.dumps({'error': 'User not found!'})
    points = sum([point['value'] for point in user['points']])
    if 'value' in request.json and int(request.json['value']) < 0: # deduct points
        deduct_value = int(request.json['value'])
        if abs(deduct_value) > points:
            return json.dumps({'error': 'Deduction value higher than user\'s points!'})
        deductions = []
        while abs(deduct_value) != 0:
            # deduct points from oldest first
            valid_points = [p for p in user['points'] if p['value'] > 0]
            oldest_timestamp = min([point['date'] for point in valid_points])
            oldest_points = next((point for point in valid_points if point['date'] == oldest_timestamp), None)
            if abs(deduct_value) <= oldest_points['value']:
                oldest_points['value'] += deduct_value # subtracts points to be deducted from oldest_points
                points += deduct_value # subtracts deduction value from points variable
                deductions.append({'company': oldest_points['company'], 'value': deduct_value, 'time': round(time.time())})
                deduct_value = 0
            else:
                # zero out points
                points -= oldest_points['value']
                deduct_value += oldest_points['value']
                deductions.append({'company': oldest_points['company'], 'value': -(oldest_points['value']), 'time': round(time.time())})
                oldest_points['value'] -= oldest_points['value']
        
        return json.dumps(deductions)
    else: # add or deduct depending on value
        if request.json['point']['value'] < 0: # deduct specific points
            deduct_value = int(request.json['point']['value'])
            points_to_deduct_from = next((user['points'][i] for i in range(len(user['points'])) if user['points'][i]['company'] == request.json['point']['company']), None)
            points_to_deduct_from['value'] += deduct_value 
            return json.dumps(points_to_deduct_from)
        new_points = request.json['point']
        new_points['date'] = round(time.mktime(datetime.strptime(new_points['date'], '%m/%d/%Y %H:%M:%S').timetuple()))
        user['points'].append(new_points)
        return json.dumps(new_points)


run(host='localhost', port=5000)
