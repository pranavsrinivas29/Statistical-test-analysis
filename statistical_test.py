import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import chi2_contingency

class Statistical_test:
    def __init__(self):
        self.teststat = 0
        self.p_val = 0
        self.alpha = 0.05
    
    def hypothesis_test(self):
        if self.p_val <= self.alpha:
            return "Reject the Null Hypothesis"
        else:
            return "Accept the Null Hypothesis"
    
    def print_values(self):
        print(f'Test-Statistics: {self.teststat}, P-Value: {self.p_val}')  
        
    def two_sample_ttest(self, df:pd.DataFrame, group1:str, group2:str):
        df_group1 = df[df['WHO Region']==group1]['Deaths / 100 Cases']
        df_group2 = df[df['WHO Region']==group2]['Deaths / 100 Cases']
        self.teststat, self.p_val = ttest_ind(df_group1.dropna(), df_group2.dropna())
        return self.teststat, self.p_val
    
    def one_sample_ttest(self, df:pd.DataFrame, col:str, region:str, flag:str):
    
        # Drop NA values for valid mean calculation
        global_mean = df[col].dropna().mean()
        print("Global mean:", round(global_mean, 2))

        # Extract region
        df_test = df[df["WHO Region"] == region][col].dropna()

        # One-sample t-test
        self.teststat, p_two_tailed = ttest_1samp(df_test, global_mean)
        
        if flag == 'greater':
            self.p_val = p_two_tailed / 2 if self.teststat > 0 else 1 - (p_two_tailed / 2)

        elif flag == 'less':
            self.p_val = p_two_tailed / 2 if self.teststat < 0 else 1 - (p_two_tailed / 2)

        else:  # two-sided (default)
            self.p_val = p_two_tailed

        return self.teststat, self.p_val

    def z_test_proportions(self, df, region1:str, region2:str, proportionality:int = 70, col:str = 'Recovered / 100 Cases', sign:str = 'greater'):
        if sign.lower() == 'greater':
            df['prop_col'] = (df[col] > proportionality).astype(int)
        else:
            df['prop_col'] = (df[col] < proportionality).astype(int)
        
        group1 = df[df['WHO Region'] == region1]['prop_col']
        group2 = df[df['WHO Region'] == region2]['prop_col']

        if group1.empty or group2.empty:
            return None, None, "Insufficient data"

        successes = [group1.sum(), group2.sum()]
        totals = [group1.count(), group2.count()]

        self.teststat, self.p_val = proportions_ztest(successes, totals)
        return self.teststat, self.p_val

    def chi_square_test_binary(self, df: pd.DataFrame, 
                            group_col: str = 'WHO Region',
                            metric_col: str = 'Recovered / 100 Cases',
                            condition: str = '>',
                            threshold: float = 70.0,
                            new_flag_name: str = 'Binary Flag'):
        # Validate condition
        if condition == '>':
            df[new_flag_name] = (df[metric_col] > threshold).astype(int)
        elif condition == '<':
            df[new_flag_name] = (df[metric_col] < threshold).astype(int)
        elif condition == '>=':
            df[new_flag_name] = (df[metric_col] >= threshold).astype(int)
        elif condition == '<=':
            df[new_flag_name] = (df[metric_col] <= threshold).astype(int)
        elif condition == '==':
            df[new_flag_name] = (df[metric_col] == threshold).astype(int)
        else:
            raise ValueError("Invalid condition. Must be one of: '>', '<', '>=', '<=', '=='")

        # Drop NA and create contingency table
        subset = df[[group_col, new_flag_name]].dropna()
        contingency = pd.crosstab(subset[group_col], subset[new_flag_name])

        if contingency.empty or contingency.shape[0] < 2:
            return None, None, contingency, "❌ Insufficient data for test."

        self.teststat, self.p_val, dof, expected = chi2_contingency(contingency)

        return self.teststat, self.p_val, dof, expected



if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv('country_wise_latest.csv')
    st = Statistical_test()
    #t, p = st.one_sample_ttest(df, "Recovered / 100 Cases", 'South-East Asia', 'greater')
    #t, p = st.z_test_proportions(df, 'Europe', 'Africa', 80 )
    t, p, dof, exp = st.chi_square_test_binary(df, 'WHO Region', 'Recovered / 100 Cases', '>', 70)
    print(t, p)
    print(st.hypothesis_test())