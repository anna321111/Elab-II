import pandas as pd
import numpy as np

# Import the enhanced csv data

df = pd.read_csv('Data/supermarket_enhanced.csv')




#Method which subsets the data depending on the departmments and then aggregates the data to find out how much the customer spent on each department

def subset_data(df, department):
    temp = df[df['departmentnumber'] == department]
    aggregated_data = temp.groupby('tripnumber').agg({'timebetween': 'sum', 'price': 'sum', 'purchasenumber': 'first'}).reset_index()
    aggregated_data['count'] = temp.groupby('tripnumber').size().reset_index(name='count')['count']
    return aggregated_data


if __name__ == '__main__':

    department_names = {
        1: "bakery&pastry", 2: "beer&Wine", 3: "books&magazines", 4: "candy&chips",
        5: "care&hygiene", 6: "cereals&spreads", 7: "cheese&tapas", 8: "dairy&eggs",
        9: "freezer", 10: "fruit&vegetables", 11: "household&pet", 12: "meat&fish",
        13: "pasta&rice", 14: "salads&meals", 15: "sauces&spices", 16: "soda&juices",
        17: "specialDiet", 18: "vegetarian&vegan"
    }

    departments = range(1, 19)

    for department in departments:
        data = subset_data(df, department)
        department_name = department_names[department]
        data.to_csv(f'Data/Aggregated/{department_name}.csv', index=False)