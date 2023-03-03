import cleanedData as cd
import pandas as pd
from projects_utils import assert_equals

# unfiltered_test_tabacco = ("https://raw.githubusercontent.com/DevinaT/CSE163/main/test_tabacco.csv")
# filtered_test_tabacco = 


# def test_tabacco_clean(test_file: str) -> None:
    # assert_equals(filtered_test_df, cd.tabacco_clean(unfiltered_test_tabacco))

def test_obsity_clean(test_file: str, result_file: str) -> None:
    assert_equals(result_file, cd.obesity_cleaned(test_file))
    print("test_obsity_clean passed")



def main():
    # test_file = pd.read_csv(unfiltered_test_tabacco)
    # filtered_test_df
    test_obsity_clean()


