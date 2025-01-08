import json

from .models import Budget

def callback(ch, method, properties, body):
    # print('Received in main')
    data = json.loads(body)
    # print(data)

def delete_user_budget(ch, method, properties, body):
    # print('Received in main for deletion')
    data = json.loads(body)
    # print(data)
    budgets = Budget.objects.filter(owner=data)
    budgets.delete()
    