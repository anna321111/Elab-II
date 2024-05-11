import pandas as pd
import numpy as np
import pyperclip

# Import the enhanced csv data






#Method which subsets the data depending on the departmments and then aggregates the data to find out how much the customer spent on each department

def subset_data(df, department):
    temp = df[df['departmentnumber'] == department]
    aggregated_data = temp.groupby('tripnumber').agg({'timebetween': ['sum', 'max', 'min', 'mean'],'price': ['sum', 'max', 'min', 'mean'], 'purchasenumber': 'first'}).reset_index()
    aggregated_data['count'] = temp.groupby('tripnumber').size().reset_index(name='count')['count']
    return aggregated_data


def sample_data(df: pd.DataFrame, name):
    # Assuming the trip numbers are strings in the DataFrame, if they are not integers
    sampled_trip_numbers = df.iloc[1:, 0].sample(n=150, random_state=69420)

    # Convert the sampled trip numbers to string
    sampled_trip_numbers = sampled_trip_numbers.astype(str)

    sampled_trip_numbers_str = sampled_trip_numbers.to_string(index=False)

    # Copy the string to the clipboard
    pyperclip.copy(sampled_trip_numbers_str)

    # Save the sampled trip numbers to CSV
    sampled_trip_numbers.to_csv(f'Data/Samples/sampled_{name}', index=False)


if __name__ == '__main__':


    department_names = {
        1: "bakery&pastry", 2: "beer&Wine", 3: "books&magazines", 4: "candy&chips",
        5: "care&hygiene", 6: "cereals&spreads", 7: "cheese&tapas", 8: "dairy&eggs",
        9: "freezer", 10: "fruit&vegetables", 11: "household&pet", 12: "meat&fish",
        13: "pasta&rice", 14: "salads&meals", 15: "sauces&spices", 16: "soda&juices",
        17: "specialDiet", 18: "vegetarian&vegan"
    }




    departments = range(1, 19)


    df = pd.read_csv('Data/case47Formatted.csv')
    data = subset_data(df, 18)
    department_name = department_names[18]
    sample_data(data, f'{department_names[18]}')
    data.to_csv(f'Data/Aggregated/{department_name}.csv', index=False)
        

