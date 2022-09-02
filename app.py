import os
import json
import pandas as pd
import rds_connect

class NUTIRITION:
  allergys_keyword = []
  allergy_dict =  {}
  ingredient_list = []
  nutrition_keyword = []
  nutrition_list = []

  def __init__(self):
    self.allergys_keyword = ['계란', '우유', '땅콩', '견과류', '밀', '갑각류', '대두', '메밀', '쇠고기', '돼지고기', '닭고기','생선', '과일']
    self.allergy_dict =  {i:'0' for i in self.allergys_keyword}
    self.ingredient_list = []
    self.nutrition_keyword = set(['영양정보', '영양 정보'])
    self.nutrition_list = []

  def Nutrition_Processing(self, word_list):
    for word in word_list[1:]:
      if '%' in word:
        item_list = word.split('%')
        for item in item_list:
          item = item.strip()
          if item:
             self.nutrition_list.append(item+'%')
      else:
        self.nutrition_list.append(word)

  def Check_Word(self, labels):
    flag = True
    for idx, label in enumerate(labels):
      label = label.strip()
      label = label.replace(',', '|')

      for key in self.allergys_keyword:
        if key in label:
          print(key, label)
          self.allergy_dict[key] = '1'

      if(label in self.nutrition_keyword):
        print('in')
        self.Nutrition_Processing(labels[idx:-2])
        break

      else:
        self.ingredient_list.append(label)


def handler(event, context):
    datas = event['responsePayload']['body']
    key = event['responsePayload']['key']
    bucket = event['responsePayload']['bucket']
    print(key, bucket)

    df = pd.DataFrame(columns=['description', 'box', 'height'])
    for data in datas:
        description = data['description']
        box = data['box']
        height = box[0]/20 + box[1]
        df.loc[len(df.index)]=[description, box, height]

    sorted_df = df.sort_values(by='height')
    show_labels = sorted_df.description.tolist()
    process = NUTIRITION()
    process.Check_Word(show_labels)

    print('fix and Deployed by CodePipeline')
    try:
        rds_connect.Insert_RDS(process, key, bucket)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except:
        return{
            'statusCode': 400,
            'body': json.dumps('ERROR!')
        }
