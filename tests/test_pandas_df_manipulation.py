import pandas as pd

from tests.custom_fixtures import pytest, create_general_test_file

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
    'in2, in3, expected', [
        (
            2, ['mathematics', 'biology'],
            {
                'district_code': ['dt1', 'dt3', 'dt2'],
                'mathematics': [1, 2, 1],
                'biology': [3, 0, 1]
            }
         ),
        (
            3, ['biology', 'history', 'literature'],
            {
                'district_code': ['dt1', 'dt2', 'dt3'],
                'biology': [2, 1, 0],
                'history': [1, 1, 0],
                'literature': [1, 0, 1]
            }
        )
    ]
)
def test_df_manipulation(in2, in3, expected, create_general_test_file, tmp_path):
    input_csv = create_general_test_file
    input_csv.write_text(input_data)
    fake_result = {'district_code': ['dt5', 'dt1', 'dt2'], 'mathematics': [1, 2, 1], 'biology': [3, 0, 1]}

    actual = df_manipulation(f'{tmp_path}/file.ext', in2, in3)
    assert actual.equals(pd.DataFrame(expected))
    assert not actual.equals(pd.DataFrame(fake_result))