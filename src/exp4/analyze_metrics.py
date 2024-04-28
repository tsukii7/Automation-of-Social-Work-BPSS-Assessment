# Identify the metrics of interest for accuracy, consistency, and semantic relevance
import numpy as np
import pandas as pd
updated_file_path = 'results/total.xlsx'
updated_data = pd.read_excel(updated_file_path)
accuracy_metrics = ['PCNARz', 'PCCNCz', 'CRFNO1']
consistency_metrics = ['PCREFz', 'PCDCz', 'PCCONNz', 'CRFCWO1']
semantic_relevance_metrics = ['LSASS1', 'SMCAUSlsa', 'SYNLE', 'DRPVAL']

# List all specific metrics
all_metrics = accuracy_metrics + consistency_metrics + semantic_relevance_metrics

metric_data_list = []  # List to collect data for each metric across all versions

# Calculate normalized values for each metric across all versions
for metric in all_metrics:
    if metric in updated_data['TextID'].values:
        metric_data = updated_data[updated_data['TextID'] == metric]

        # Extracting all relevant columns for the metric
        relevant_columns = metric_data.filter(regex=r'\d_\d\.docx/').columns
        all_values = metric_data[relevant_columns].values

        # Flattening the array of values and removing NaNs for normalization
        flattened_values = all_values.flatten()
        flattened_values = flattened_values[~np.isnan(flattened_values)]

        # Normalization using min-max scaling
        min_val = np.min(flattened_values)
        max_val = np.max(flattened_values)
        normalized_values = (metric_data[relevant_columns] - min_val) / (max_val - min_val)

        # Calculating mean values for original, non-BERT, and BERT processed texts
        for col in relevant_columns:
            version_type = 'Original' if '_1' in col else 'Non-BERT' if '_2' in col else 'BERT'
            mean_val = normalized_values[col].mean()
            metric_data_list.append({
                'Metric': metric,
                'Version': version_type,
                'Normalized Mean': mean_val
            })

metric_analysis_df = pd.DataFrame(metric_data_list)

# Display normalized results for comparison
print(metric_analysis_df.pivot_table(index=['Metric'], columns='Version', values='Normalized Mean', aggfunc=np.mean))
