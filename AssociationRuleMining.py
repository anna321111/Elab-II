import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from matplotlib import pyplot as plt


def identify_and_sort_frequent_itemsets(csv_file_path, min_support=0.3):
    df = pd.read_csv(csv_file_path, nrows=1000)
    transactions = df.groupby('tripnumber')['departmentnumber'].apply(list).tolist()

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_trans = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df_trans, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

    # Calculating lift for the rules
    rules['lift'] = rules['confidence'] / (rules['consequent support'] / rules['antecedent support'])

    # Select and rename columns, and format numbers
    rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    rules['itemset'] = rules['antecedents'].astype(str) + ' -> ' + rules['consequents'].astype(str)
    rules['support'] = rules['support'].round(2)
    rules['confidence'] = rules['confidence'].round(2)
    rules['lift'] = rules['lift'].round(2)
    rules = rules[['itemset', 'support', 'confidence', 'lift']]

    # Sort by support, confidence, and lift
    sorted_rules = rules.sort_values(by=['support', 'confidence', 'lift'], ascending=[False, False, False])
    return sorted_rules


def save_df_as_image(df, filename='Plots/dataframe.png'):
    fig, ax = plt.subplots(figsize=(12, 8))  # Set dimensions for the figure
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)  # Set font size
    the_table.scale(1.2, 1.2)  # Scale table
    plt.savefig(filename, dpi=300)
    plt.close()


# Run the process
csv_file_path = 'Data/supermarket_enhanced.csv'
rules_df = identify_and_sort_frequent_itemsets(csv_file_path)
print(rules_df.head(20))  # Print the top 20 rules
save_df_as_image(rules_df.head(20), 'plots/sorted_frequent_itemsets.png')