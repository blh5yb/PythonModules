import argparse
import pandas as pd
import re
########################################################################################################################
# Pandas Dataframe Manipulation
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################


def df_manipulation(input_csv, min_subjects, query_subjects):
    """
    Read dataframe of school subjects offered for certain districts and perform the following operations:
    Drop rows/ schools that offer fewer than <min_subjects> subjects
    remove non alpha-numeric characters from the school_code column
    create data frame with total number of schools offering each <query_subjects> per district
    :param input_csv: path to csv of school subjects data, str
    :param min_subjects: min subjects for output df, int
    :param query_subjects: subjects to tabulate in output df, int
    """
    raw_df = pd.read_csv(input_csv)
    data = {
        'district_code': []
    }
    for sub in query_subjects:
        data[sub] = []

    for index, row in raw_df.iterrows():
        # remove non-alphanumeric characters
        district_code = re.sub(r'[^a-zA-Z0-9]', '', row['district_code'])
        school_subjects = row['subjects'].split(' ')
        if len(school_subjects) >= min_subjects:
            try:
                # if index is found, then this district has already been seen so we update the row with the subject values
                data_index = data['district_code'].index(district_code)
                for subject in query_subjects:
                    if subject in school_subjects:
                        data[subject][data_index] += 1
            except ValueError:
                # we havent seen this subject before so append a new row to the data for this district code
                data['district_code'].append(district_code)
                for subject in query_subjects:
                    if subject in school_subjects:
                        data[subject].append(1)
                    else:
                        data[subject].append(0)
    output_df = pd.DataFrame(data)

    return output_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pandas Dataframe Manipulation")
    parser.add_argument('-i', '--input_csv', type=str, action="store", required=True, help="csv input dataframe")
    parser.add_argument('-m', '--min_subjects', type=int, action="store", required=True, help="minimum school subjects offered")
    parser.add_argument('-s', '--query_subjects', type=str, action="append", required=True, help="subjects to counts for output df")
    parser_args = parser.parse_args()
    result = df_manipulation(parser_args.input_csv, parser_args.min_subjects, parser_args.query_subjects)