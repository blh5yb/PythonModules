import pandas as pd

from tests.custom_fixtures import pytest, patch, Mock, create_dummy_input_file

from src.pandas_df_manipulation import *

input_data = (f'school_code,district_code,subjects\n'
              f'sc1,@*dt1,biology history\n'
              f'sc4,_dt_2,mathematics\n'
              f'sc2,@*dt1,mathematics biology literature\n'
              f'sc6,^^dt3,history mathematics\n'
              f'sc5,_dt_2,history mathematics biology\n'
              f'sc7,^^dt3,economics mathematics\n'
              f'sc3,@*dt1,history health biology\n'
              f'sc8,^^dt3,literature speech economics\n')

@pytest.mark.parametrize(
    'create_dummy_input_file',['input.csv'], indirect=True
)
def test_df_manipulation(create_dummy_input_file, tmp_path):
    input_csv = create_dummy_input_file
    input_csv.write_text(input_data)
    expected_data = {'district_code': ['dt1', 'dt3', 'dt2'], 'mathematics': [1, 2, 1], 'biology': [3, 0, 1]}
    fake_result = {'district_code': ['dt5', 'dt1', 'dt2'], 'mathematics': [1, 2, 1], 'biology': [3, 0, 1]}

    result = df_manipulation(f'{tmp_path}/input.csv', 2, ['mathematics', 'biology'])
    assert result.equals(pd.DataFrame(expected_data))
    assert not result.equals(pd.DataFrame(fake_result))