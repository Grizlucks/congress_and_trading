import numpy as np


def tvd(data, col, group_on) -> float:
    """
    Calculates total variation distance of the distribution of values
    in col between the two groups of group_on. Assumes that col is
    categorical.
    Parameters
    -----------
    data: pd.DataFrame
        DataFrame with labels for the two groups
    col: str
        String name of a categorical column.
    group_on: str
        String name for column containing the two group labels
    Returns
    -----------
    tvd: float
        Test statistic (total variation distance of the distribution of
        values in col between the two groups of group_on)
    """
    tvd = (
        data.pivot_table(index=col, columns=group_on, aggfunc="size", fill_value=0)
        .apply(lambda x: x / x.sum())
        .diff(axis=1)
        .iloc[:, -1]
        .abs()
        .sum()
        / 2
    )
    return


def permutation_test(data, col, group_on, test_stat, n=1000) -> tuple:
    """
    Returns a distribution of permuted test statistics and the observed
    test statistic resulting from permutation tests.
    Parameters
    -----------
    data: pd.DataFrame
        DataFrame with labels for the two groups
    col: str
        String name of a categorical column.
    group_on: str
        String name for column containing the two group labels
    test_stat: function
        Function to generate test statistic
    n: int (default = 100)
        Number of permutation tests to be run.
    Returns
    -----------
    stats: np.array
        Array of permutated (simulated) test statistics
    obs: float
        Observed test statistic
    """
    # calculate observed test statistic
    obs = test_stat(data, col, group_on)

    # permutation test
    stats = np.zeros(n)

    # create a copy dataframe to avoid overwriting original
    shuffled_data = data.copy()
    shuffled_col = shuffled_data[group_on].values
    for i in range(n):
        shuffled_col = np.random.permutation(shuffled_col)
        shuffled_data["shuffled"] = shuffled_col
        created_stat = test_stat(shuffled_data, col, "shuffled")
        stats[i] = created_stat

    return stats, obs
