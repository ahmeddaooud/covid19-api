"""
FILE: covid_model_api_v2.py
DESCRIPTION: Covid-19 Model for API v2
AUTHOR: Nuttaphat Arunoprayoch
DATE: 14-March-2020
"""
# Import libraries
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
from utils.get_data import (get_data_daily_reports, get_data_time_series,
                            get_US_time_series, get_data_lookup_table)


class NovelCoronaAPIv2:
    """ Covid-19 API v2 model and its methods
        SCHEMA: {
            "data": Any,
            "dt": str = "{datetime}",
            "ts": int = "{timestamp}
        }
    """
    def __init__(self) -> None:
        """ Initiate DataFrames """
        self.df = get_data_daily_reports()
        self.df_time_series = get_data_time_series()
        self.df_US_time_series = get_US_time_series()
        self.lookup_table = get_data_lookup_table()

        concerned_columns = ['Confirmed', 'Deaths', 'Recovered', 'Active']
        self.df_grp_by_country = self.df.groupby('Country_Region')[concerned_columns].sum()
        self.df_grp_by_country[concerned_columns] = self.df_grp_by_country[concerned_columns].astype(int)

        self.datetime = max(self.df['Last_Update'].tolist())
        self.timestamp = datetime.strptime(self.datetime, '%Y-%m-%d %H:%M:%S').timestamp()

        self.scheme = {
            'data': None,
            'dt': self.datetime,
            'ts': self.timestamp
        }
    
    def get_current(self) -> Dict[str, Any]:
        """ Current data from all locations (Lastest date) """
        df_grp_by_country = self.df_grp_by_country.sort_values(by='Confirmed', ascending=False)
        df_grp_by_country = df_grp_by_country.reset_index()
        df_grp_by_country.columns = ['location', 'confirmed', 'deaths', 'recovered', 'active']
        data = [v for v in df_grp_by_country.to_dict('index').values()]
        packed_data = self.scheme
        packed_data['data'] = data

        return packed_data

    def get_country(self, country_name: str) -> Dict[str, Any]:
        """ Get a country data from its name or ISO 2 """
        all_country_data = self.get_current()['data']

        # Search for a given country
        if country_name not in [country_data['location'].lower() for country_data in all_country_data]:
            country_name = self.lookup_table[country_name.upper()] # translate country code to its name

        data = [country_data for country_data in all_country_data
                                if country_name.lower() == country_data['location'].lower()][0]
        packed_data = self.scheme
        packed_data['data'] = data

        return packed_data

    def get_confirmed(self) -> Dict[str, Any]:
        """ Summation of all confirmed cases """
        data = self.df['Confirmed'].sum()
        packed_data = self.scheme
        packed_data['data'] = int(data)

        return packed_data

    def get_deaths(self) -> Dict[str, Any]:
        """ Summation of all deaths """
        data = self.df['Deaths'].sum()
        packed_data = self.scheme
        packed_data['data'] = int(data)

        return packed_data
    
    def get_recovered(self) -> Dict[str, Any]:
        """ Summation of all recovers """
        data = self.df['Recovered'].sum()
        packed_data = self.scheme
        packed_data['data'] = int(data)

        return packed_data

    def get_active(self) -> Dict[str, Any]:
        """ Summation of all actives """
        data = self.df['Active'].sum()
        packed_data = self.scheme
        packed_data['data'] = int(data)

        return packed_data
    
    def get_total(self) -> Dict[str, Any]:
        """ Summation of Confirmed, Deaths, Recovered, Active """
        packed_data = self.scheme
        packed_data['data'] = {
            'confirmed': int(self.df['Confirmed'].sum()),
            'deaths': int(self.df['Deaths'].sum()),
            'recovered': int(self.df['Recovered'].sum()),
            'active': int(self.df['Active'].sum())
        }
        
        return packed_data

    def __extract_time_series(self, time_series: Dict) -> List[Dict]:
        time_series_data = []

        for data in time_series.values():
            excluded_cols = ['Province/State', 'Country/Region', 'Lat', 'Long']
            temp_dict = {}
            temp_dict['Province/State'] = data['Province/State']
            temp_dict['Country/Region'] = data['Country/Region']
            temp_dict['Coordinates'] = {'Lat': float(data['Lat']), 'Long': float(data['Long'])}

            temp_time_series_dict = {k: int(v) for k, v in data.items() if k not in excluded_cols}
            temp_dict['TimeSeries'] = [{'date': k, 'value': v} for k, v in temp_time_series_dict.items()]
            
            time_series_data.append(temp_dict)   

        return time_series_data

    def __extract_US_time_series(self, time_series: Dict) -> List[Dict]:
        time_series_data = []

        for data in time_series.values():
            excluded_cols = ['UID', 'iso2', 'iso3', 'code3', 'FIPS',
                            'Admin2','Province_State', 'Country_Region', 'Lat', 'Long_', 
                            'Combined_Key','Population']

            temp_dict = {}
            temp_dict['Province_State'] = data['Province_State']
            temp_dict['Country_Region'] = data['Country_Region']
            temp_dict['Info'] = {
                'UID': data['UID'],
                'iso2': data['iso2'],
                'iso3': data['iso3'],
                'code3': data['code3'],
                'FIPS': data['FIPS'],
                'Admin2': data['Admin2']
            }
            temp_dict['Coordinates'] = {'Lat': float(data['Lat']), 'Long': float(data['Long_'])}

            temp_time_series_dict = {k: int(v) for k, v in data.items() if k not in excluded_cols}
            temp_dict['TimeSeries'] = [{'date': k, 'value': v} for k, v in temp_time_series_dict.items()]
            
            time_series_data.append(temp_dict) 

        return time_series_data

    def __extract_time_series_global(self, dataframe_dict: Dict[str, pd.DataFrame]) -> List[Dict]:
        global_df_list = []

        for key, df in dataframe_dict.items():
            df_temp = pd.DataFrame(df.iloc[:, 4:].astype('int32').sum(axis=0))
            df_temp.columns = [key]
            global_df_list.append(df_temp)

        # Combine DataFrames
        global_dict = pd.concat(global_df_list, axis=1, sort=False).T.to_dict()
        data = [{k: v} for k, v in global_dict.items()]

        return data

    def get_time_series(self, case: str) -> Dict[str, Any]:
        if case not in ['global']:
            raw_data = self.df_time_series[case].T.to_dict()
            data = self.__extract_time_series(raw_data)
        else:
            raw_data = self.df_time_series
            data = self.__extract_time_series_global(raw_data)

        packed_data = self.scheme
        packed_data['data'] = data

        return packed_data
    
    def get_US_time_series(self, case: str) -> Dict[str, Any]:
        """ Get USA time series """
        if case not in ['confirmed', 'deaths']:
            data = []
        else:
            raw_data = self.df_US_time_series[case].T.to_dict()
            data = self.__extract_US_time_series(raw_data)
        
        packed_data = self.scheme
        packed_data['data'] = data

        return packed_data
