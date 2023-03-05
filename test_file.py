import cleanedData as cd
import pandas as pd
from projects_utils import assert_equals
import niyat_questions as n
import devina_questions as d


# store string as constant and read content to get the data frame
TEST_OBESITY_RESULT = pd.read_csv('https://raw.githubusercontent.com/DevinaT/'
                                  'CSE163/main/obesity_test_clean.csv')
test_tabacco_result = pd.read_csv('https://raw.githubusercontent.com/DevinaT/'
                                  'CSE163/main/TES_tabacco_filtered.csv')
test_tabcacco_filtered_result = pd.read_csv('https://raw.githubusercontent.com/DevinaT/'
                                            'CSE163/main/TEST_T_FILTER_RESULT.csv')
test_c_cleaned = pd.read_csv('https://raw.githubusercontent.com/DevinaT/'
                             'CSE163/main/cardiovascular_test_cleaned.csv')
top_ten_list = [['OK', 'UT', 'FL', 'WY', 'IL', 'WI', 'ND', 'IA', 'ID', 'VT']]  # type for this??
format_cardiovasc_method = pd.read_csv('https://raw.githubusercontent.com/DevinaT/CSE163/main/format_cardio_vasc.csv')


def test_tabacco_clean(test_file: str, result_file: str) -> None:
    '''
    This function takes in a test data set anf returns a cleaned version. 
    This is used to test the tabacco_clean method in the CleanedData file. 
    '''
    filtered_test_df = cd.tabacco_clean(test_file)
    filtered_test_df = filtered_test_df.reset_index(drop=True)
    assert_equals(len(result_file), len(filtered_test_df))
    print("test_tabacco_clean passed!")


def test_tabcacco_filtered(test_file: str, result_file: str) -> None:
    '''
    This function tests the tabacco_filtered method.
    '''
    filtered_df = n.tabacco_filtered(test_file)
    filtered_df = filtered_df.reset_index(drop = True)
    assert_equals(filtered_df, test_tabcacco_filtered_result)
    assert_equals(len(result_file), len(filtered_df))
    print("test_tabacco_filtered passed!")


def test_obesity_clean(test_file: str, result_file: str) -> None:
    """
    This function takes in a test data set and a cleaned verison of the
    test dataset and sees if they are equal to each other after the
    function cd.obesity_cleaned is called on them. In order to test this,
    the indexes of the cleaned test_file must be rest so the indexs are
    the same. If not the files will not be equal even if the content
    inside of them are equal.
    """
    clean_obesity_test = cd.obesity_cleaned(test_file)
    # drop the indexes
    clean_obesity_test = clean_obesity_test.reset_index(drop=True)

    assert_equals(len(result_file), len(clean_obesity_test))
    assert_equals(TEST_OBESITY_RESULT, clean_obesity_test)
    print("test_obsity_clean passed")


def test_cardiovascular_clean(result_file: str) -> None:
    """
    This function takes in a test data set and a cleaned verison of the
    test dataset and sees if they are equal to each other after the
    function cd.cardiovascular_cleaned is called on them. In order to test this,
    the indexes of the cleaned test_file must be rest so the indexs are
    the same. If not the files will not be equal even if the content
    inside of them are equal.
    """
    clean_cardio = cd.cardiovascular_cleaned('https://raw.githubusercontent.com/DevinaT/CSE163/main/cardiovascular_test.csv')
    # drop the indexes
    clean_cardio = clean_cardio.reset_index(drop=True)

    assert_equals(len(result_file), len(clean_cardio))
    assert_equals(result_file, clean_cardio)
    print("test_cardiovascular_clean passed!")


def test_top_ten_list() -> None:
    top_ten = d.find_top_ten(test_c_cleaned)
    assert_equals(top_ten_list, top_ten)
    print("top ten passed!")


def test_format_cardiovasc(test_file: str) -> None:
    assert_equals(format_cardiovasc_method, d.format_cardiovasc(test_file, top_ten_list))
    print("format_cardiovasc passed!")


def test_format_obesity(test_file: str) -> None:
    assert_equals(test_file, d.format_obesity(test_file, top_ten_list))
    print("format_obesity passed!")


def main():

    test_obesity_clean("https://raw.githubusercontent.com/DevinaT/CSE163/main/obesity_test.csv",
                       TEST_OBESITY_RESULT)
    test_tabacco_clean("https://raw.githubusercontent.com/DevinaT/CSE163/main/test_tabacco.csv",
                       test_tabacco_result)
    test_tabcacco_filtered(test_tabacco_result, test_tabcacco_filtered_result)
    test_cardiovascular_clean(test_c_cleaned)
    test_top_ten_list()
    test_format_cardiovasc(test_c_cleaned)
    test_format_obesity(TEST_OBESITY_RESULT)


if __name__ == "__main__":
    main()
