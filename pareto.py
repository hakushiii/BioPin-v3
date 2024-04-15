import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations


def maximization(max_val: int, min_val: int, pc_raw: int) -> float:
    '''Return pc_norm maximization'''
    return (9 * ((pc_raw - min_val) / (max_val - min_val))) + 1


def minimization(max_val: int, min_val: int, pc_raw: int) -> float:
    '''Return minimization of the pc_norm'''
    return (9 * ((max_val - pc_raw) / (max_val - min_val))) + 1


def min_max(table: dict) -> pd.DataFrame:
    '''Return a DataFrame with the values of ability to satisfy the criterion'''

    temp_list = []

    # Extract the table, _ for the "Constraint Name"
    for _, constraints in table.items():

        # Extract the operation (min, max) and list of constraints and perform
        # the operation needed
        for operation, constraints_vals in constraints.items():
            max_raw = max(constraints_vals)
            min_raw = min(constraints_vals)
            if operation == 'max':
                temp_array = [maximization(max_raw, min_raw, x)
                              for x in constraints_vals]
            elif operation == 'min':
                temp_array = [minimization(max_raw, min_raw, x)
                              for x in constraints_vals]
            temp_list.append(temp_array)

    return pd.DataFrame(temp_list, columns=[
                        f'D{i+1}' for i in range(len(temp_list[0]))])


def ability_to_satisfy(options: pd.DataFrame) -> list:
    '''Return a 2D list of possible values of ability_to_satisfy'''

    # Create a generator for permutations of the array
    ranking = permutations([10, 9, 8, 7, 6], 5)

    result = []
    permutation_list = []

    # Compute the percentages per ranking / scale
    for ranks in ranking:
        percentages = [rank / sum(ranks) for rank in ranks]
        permutation_list.append(ranks)
        temp_result = []

        # Compute the sum of ability to satisfy the criterion inputs
        for _, values in options.items():
            temp_result.append(
                sum([x * y for (x, y) in zip(values, percentages)]))
        result.append(temp_result)

    df2 = pd.DataFrame(result, columns=['D1', 'D2', 'D3'])
    df2.plot(figsize=(20, 12)).grid()
    plt.savefig('result.png')

    df2.to_csv('result.csv', index=False)
    pd.DataFrame(permutation_list).to_csv(
        'possible_permutation.csv', index=False)

    return df2


if __name__ == '__main__':
    df = {
        'economic': {
            'min': [7137.66, 12435.40, 10657],
        },
        'environmental': {
            'min': [1140.737, 865.5055, 808.0682],
        },
        'safety': {
            'max': [10, 11, 11],
        },
        'reliability': {
            'max': [3.81, 6.67, 10.5],
        },
        'reliability': {
            'max': [3.81, 6.67, 5.5555],
        },
    }
    df = min_max(df)
    df = ability_to_satisfy(df)
    print(df)