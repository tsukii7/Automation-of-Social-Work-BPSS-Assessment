import json
from gpt_rewrite import transform_dialogue_to_narrative

json_file_path = '../data/json/conversa_log.json'
conversation_json = {}

with open(json_file_path, 'r') as f:
    data = json.load(f)
    cnt = 0
    for key in data:
        cnt += 1
        conversation_obj = {'message_cnt': len(data[key]), 'dialogue': "\n".join(data[key]),
                            'narrative': transform_dialogue_to_narrative(data[key])}
        conversation_json[key] = conversation_obj
    print(cnt)
    conversation_json = dict(sorted(conversation_json.items(), key=lambda x: x[1]["message_cnt"]))
    conversation_json['total_conversations'] = cnt
    json.dump(conversation_json, open('data/json/conversation_narrative.json', 'w'), indent=4)
