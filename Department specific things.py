import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv('Data/department_metrics.csv')

# Define function to map department codes to names
def map_department_code(code):
    department_mapping = {
        1: 'Bakery & Pastry',
        2: 'Beer & Wine',
        3: 'Books & Magazines',
        4: 'Candy & Chips',
        5: 'Care & Hygiene',
        6: 'Cereals & Spreads',
        7: 'Cheese & Tapas',
        8: 'Dairy & Eggs',
        9: 'Freezer',
        10: 'Fruit & Vegetables',
        11: 'Household & Pet',
        12: 'Meat & Fish',
        13: 'Pasta & Rice',
        14: 'Salads & Meals',
        15: 'Sauces & Spices',
        16: 'Soda & Juices',
        17: 'Special Diet',
        18: 'Vegetarian & Vegan'
    }
    return department_mapping.get(code, 'Unknown')

# Apply function to 'Department' column and create new column 'Department1'
df['Department1'] = df['Department'].apply(map_department_code)


# Set up the plot
plt.figure(figsize=(12, 8))
ax1 = sns.barplot(data=df, x='Department1', y='AvgPricePerItem', palette='Set1')

# Create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot the count of products on the second y-axis
sns.lineplot(data=df, x='Department1', y='NumItems', ax=ax2, color='orange', marker='o', linestyle='--')

# Set labels and title
ax1.set_xlabel('Department')
ax1.set_ylabel('Average Price per Product')
ax2.set_ylabel('NumItems')
plt.title('Average Price per Product and Count of Products by Department')

# Rotate x-axis labels for better readability
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

# Show the plot
plt.tight_layout()  # Adjust layout to prevent cropping
plt.show()