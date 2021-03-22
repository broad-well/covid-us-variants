import pandas as pd
from datetime import date

start_date = date(2021, 1, 6)
end_date = date.today()
variant_names = {
    'b117': ('Variant B.1.1.7', 'B.1.1.7 Variant '),
    'p1': ('Variant P.1', 'P.1 Variant '),
    'b1351': ('Variant B.1.351', 'B.1.351 Variant ')
}



def read_rows(_date: date) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(f'updates/{_date.isoformat()}.csv')
    banned_states = ['Total']
    df = df[~df.State.isin(banned_states)][~df.State.isna()]
    df['State'] = df['State'].replace('District of Columbia', 'DC')
    cols = df.columns.values.tolist()
    if 'Rate' in cols:
        df = df.rename(columns={'State': 'state', 'Rate': 'b117'})[['state', 'b117']]
        df['p1'] = 0
        df['b1351'] = 0
        return df
    if cols == ['State', 'Cases']:
        df = df.rename(columns={'State': 'state', 'Cases': 'b117'})
        df['p1'] = 0
        df['b1351'] = 0
        return df
    elif 'filter' in cols:
        return df[['State'] + [in_col for (_, in_col) in variant_names.values()]].drop_duplicates(subset=['State']).rename(columns=dict([(in_col, code) for code, (_, in_col) in variant_names.items()] + [('State', 'state')])).fillna(0)
    elif 'B.1.1.7 Variant ' in cols:
        return df.rename(columns=dict([(in_col, code) for code, (_, in_col) in variant_names.items()] + [('State', 'state')]))


def run():
    gdf = pd.DataFrame()
    for _date in pd.date_range(start_date, end_date):
        try:
            df = read_rows(_date.date())
            if df is None:
                print(f'warning: {_date.date().isoformat()}')
                continue
            df['date'] = _date.date()
            gdf = gdf.append(df)
        except FileNotFoundError:
            print(f'omitted {_date.date().isoformat()}')


    for col in variant_names.keys():
        gdf[col] = gdf[col].fillna(0).astype('int32')

    gdf.sort_values(by=['date', 'state']).to_csv('us-states.csv', index=False)


if __name__ == '__main__':
    run()