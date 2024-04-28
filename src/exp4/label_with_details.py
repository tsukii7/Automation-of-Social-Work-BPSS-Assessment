import pandas as pd

df = pd.read_csv('../data/csv/sentences_with_labels.csv', encoding='GBK')

for i, row in df.iterrows():
    if row['Coarse_grained_label'] == 'B':
        df.loc[i, 'Coarse_grained_label'] = 'Biological'
        df.loc[i, 'Fine_grained_label'] = ['Employment', 'Financial', 'Medical needs', 'Education', 'Developmental Milestones'][row['Fine_grained_label']-1]
    elif row['Coarse_grained_label'] == 'P':
        df.loc[i, 'Coarse_grained_label'] = 'Psychological'
        df.loc[i, 'Fine_grained_label'] = ['Psychological', 'Mental Health', 'Emotional', 'Coping', 'Cognitive', 'Spiritual'][row['Fine_grained_label']-1]
    elif row['Coarse_grained_label'] == 'S':
        df.loc[i, 'Coarse_grained_label'] = 'Social'
        df.loc[i, 'Fine_grained_label'] = ['Cultural', 'Marital Relationship', 'Parent-Child Relationship', 'Relationship with FOO / Family Relationship', 'Formal and Informal Systems'][row['Fine_grained_label']-1]

df.to_csv('../data/sentences_with_labels_details.csv', index=False)
