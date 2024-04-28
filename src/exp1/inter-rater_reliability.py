import pandas as pd
from sklearn.metrics import cohen_kappa_score

file_path = '../data/csv/test_dataset.csv'
# Attempt to read the file using 'GBK' encoding
data_gbk = pd.read_csv(file_path, encoding='GBK')
data_gbk.head()

# Clean up the sublabel data for comparison
# Convert sublabel columns to string to handle different types like float or int
data_gbk['sublabel'] = data_gbk['sublabel'].astype(str)
data_gbk['yugin_sublabel'] = data_gbk['yugin_sublabel'].astype(str)

# Calculate the inter-rater reliability for the main labels
main_label_kappa = cohen_kappa_score(data_gbk['label'], data_gbk['yugin_label'])

# For those rows where the main labels agree, calculate the sublabel kappa score
agreed_main_labels = data_gbk[(data_gbk['label'] == data_gbk['yugin_label']) & (data_gbk['label'] != 'N')]
sublabel_kappa = cohen_kappa_score(agreed_main_labels['sublabel'], agreed_main_labels['yugin_sublabel'])
# sublabel_kappa = cohen_kappa_score(data_gbk['sublabel'], data_gbk['yugin_sublabel'])

print(f"Main label Cohen's Kappa: {main_label_kappa}")
print(f"Sublabel Cohen's Kappa: {sublabel_kappa}")