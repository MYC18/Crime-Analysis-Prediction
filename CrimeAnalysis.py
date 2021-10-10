import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyBf8iEsubEn7Z2H05VbWfS9ePfqz5UWcHQ')


class CrimeAnalysis:
    def __init__(self):
        self.path = "Data"
        self.save_path = "static/CSVs"

    # street, outcome, stop-and-search

    def load_data(self, name, startyear, startmonth, finishyear, finishmonth, location):
        years = []
        startmonths = []
        finishmonths = []
        allmonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        all_paths = []
        save_path = self.save_path + f'/{location}-{startyear}-{startmonth}-to-{finishyear}-{finishmonth}-{name}.csv'
        check_path = 'static/CSVs/' + f'/{location}-{startyear}-{startmonth}-to-{finishyear}-{finishmonth}-{name}.csv'

        '''files_in_Save_path = glob.glob('static/CSVs//*.csv')
        for i in files_in_Save_path:
            i.replace('static/CSVs\\', '')

        print(files_in_Save_path)
        print(check_path)

        if check_path in files_in_Save_path:
            print('exists')'''
        '''else:'''
        for i in range(int(finishyear) - int(startyear) + 1):
            years.append(int(startyear) + i)
        #print(years)

        i = startmonth
        while i <= 12:
            startmonths.append(i)
            i = i + 1
        #print(startmonths)

        i = finishmonth
        while i >= 1:
            finishmonths.append(i)
            i = i - 1
        finishmonths.sort()
        #print(finishmonths)

        for i in range(len(years)):
            for j in range(len(startmonths)):
                if years[i] == startyear and years[i] != finishyear:
                    if startmonths[j] < 10:
                        all_paths.append(self.path + f'/{years[i]}' + f'-0{startmonths[j]}' + f'/{years[i]}-0{startmonths[j]}-{location}-{name}.csv')
                    else:
                        all_paths.append(self.path + f'/{years[i]}' + f'-{startmonths[j]}' + f'/{years[i]}-{startmonths[j]}-{location}-{name}.csv')

        for i in range(len(years)):
            for j in range(len(allmonths)):
                if years[i] != startyear and years[i] != finishyear:
                    if allmonths[j] < 10:
                        all_paths.append(self.path + f'/{years[i]}' + f'-0{allmonths[j]}' + f'/{years[i]}-0{allmonths[j]}-{location}-{name}.csv')
                    else:
                        all_paths.append(self.path + f'/{years[i]}' + f'-{allmonths[j]}' + f'/{years[i]}-{allmonths[j]}-{location}-{name}.csv')

        for i in range(len(years)):
            for j in range(len(finishmonths)):
                if years[i] == finishyear:
                    if finishmonths[j] < 10:
                        all_paths.append(self.path + f'/{years[i]}' + f'-0{finishmonths[j]}' + f'/{years[i]}-0{finishmonths[j]}-{location}-{name}.csv')
                    else:
                        all_paths.append(self.path + f'/{years[i]}' + f'-{finishmonths[j]}' + f'/{years[i]}-{finishmonths[j]}-{location}-{name}.csv')

        # just printing
        for i in range(len(all_paths)):
            print(all_paths[i])

        uk_df = pd.DataFrame()
        for i in range(len(all_paths)):
            if os.path.isfile(all_paths[i]):
                df = uk_df
                df_temp = pd.read_csv(all_paths[i])
                uk_df = pd.concat([df, df_temp], ignore_index=True)
            else:
                print(f'{all_paths[i]} does not exist!')
        uk_df.to_csv(save_path)
        #print(uk_df.shape)

        return uk_df

    def monthly_crime_frequency(self, uk_df):
            df = uk_df.copy()
            df.drop(['Crime ID','LSOA code',  'Falls within', 'Reported by', 'Context', 'Last outcome category'], inplace=True, axis=1)
            df.Month = pd.to_datetime(df.Month, format='%Y/%m')
            df.index = pd.DatetimeIndex(df.Month)
            monthly_crime_frequency = df.resample('m').size()
            plt.figure(figsize=(15, 5))
            plt.plot(monthly_crime_frequency)
            plt.title('Monthly Crime Frequency')
            plt.xlabel('Month')
            plt.ylabel('Number of Crimes')
            plt.savefig('static/plots/monthly_crime_frequency.png', transparent=True)
            return plt.figure

    def crime_countplot(self, uk_df):
        df = uk_df.copy()
        types = df['Crime type'].value_counts()
        order_types = types.index
        plt.figure(figsize=(15, 10))
        sns.countplot(y='Crime type', data=df, order=order_types)
        plt.savefig('static/plots/crime_count_plot_street.png')

        return plt.figure

    def lsoa_countplot(self, uk_df):
        df = uk_df.copy()
        lsoas = df['LSOA name'].value_counts()
        top_20_lsoas = lsoas[:20]
        order_types = top_20_lsoas.index
        plt.figure(figsize=(15, 10))
        sns.countplot(y='LSOA name', data=df, order=order_types)
        plt.savefig('static/plots/lsoas_count_plot_street.png')

        return plt.figure

    def locations_countplot(self, uk_df):
        df = uk_df.copy()
        locations = df['Location'].value_counts()
        top_20_locations = locations[:20]
        order_types = top_20_locations.index
        plt.figure(figsize=(15, 10))
        sns.countplot(y='Location', data=df, order=order_types)
        plt.savefig('static/plots/locations_count_plot_street.png')

        return plt.figure

    # Pairplot
    def crime_pairplot(self, uk_df):
        df = uk_df.copy()
        df.drop(['Crime ID', 'Reported by', 'Falls within', 'LSOA code', 'Last outcome category', 'Context'], inplace=True, axis=1)
        plt.figure(figsize=(15, 10))
        sns.pairplot(df, hue='Crime type', height= 3)
        plt.savefig('static/plots/crime_pair_plot_street.png')

        return plt.figure

    def geo_heatmap(self, uk_df):
        df = uk_df.copy()
        df.dropna(subset=['Longitude', 'Latitude'], inplace=True)
        crime_locations = df[['Longitude', 'Latitude']]
        fig = gmaps.figure()
        fig.add_layer(gmaps.heatmap_layer(crime_locations))
        plt.savefig('static/gmaps/geo_heatmap.png')
        return fig

    def crime_rate_heatmap(self, uk_df):
        df = uk_df.copy()
        df.drop(['Crime ID', 'LSOA code', 'Falls within', 'Reported by', 'Context', 'Last outcome category'], inplace=True, axis=1)

        df.Month = pd.to_datetime(df.Month, format='%Y/%m')
        df.index = pd.DatetimeIndex(df.Month)

        # we create two more columns for uk_df
        # months and years
        months = []
        years = []
        for i in range(len(df)):
            months.append(df['Month'][i].month)
            years.append(df['Month'][i].year)

        df['Months'] = months
        df['Years'] = years
        df.head()

        monthly_crime_frequency = df.resample('m').size()

        date = []
        values = []
        for i in range(len(monthly_crime_frequency)):
            date.append(monthly_crime_frequency.index[i])
            values.append(monthly_crime_frequency.values[i])

        monthly_crime_frequency_df = pd.DataFrame()
        monthly_crime_frequency_df['Date'] = date
        monthly_crime_frequency_df['Crime Rate'] = values

        monthly_crime_frequency_df['month'] = [i.month for i in monthly_crime_frequency_df.Date]
        monthly_crime_frequency_df['year'] = [i.year for i in monthly_crime_frequency_df.Date]
        monthly_crime_frequency_df['month'] = pd.to_numeric(monthly_crime_frequency_df['month'])
        monthly_crime_frequency_df['year'] = pd.to_numeric(monthly_crime_frequency_df['year'])
        monthly_crime_frequency_df['Crime Rate'] = pd.to_numeric(monthly_crime_frequency_df['Crime Rate'])
        monthly_crime_frequency_df = monthly_crime_frequency_df.groupby(['month', 'year']).mean()
        monthly_crime_frequency_df = monthly_crime_frequency_df.unstack(level=0)

        fig, ax = plt.subplots(figsize = (11, 9))
        sns.heatmap(monthly_crime_frequency_df)
        plt.savefig('static/heatmaps/crime_rate_heatmap.png')

    ############## Monthly Stop and Search Frequency

    def monthly_stop_and_search_frequency(self, uk_df):
            df = uk_df.copy()
            df.drop(['Part of a policing operation','Policing operation',  'Officer-defined ethnicity', 'Outcome linked to object of search', 'Removal of more than just outer clothing'], inplace=True, axis=1)
            df.Date = pd.to_datetime(df.Date, format='%Y/%m')
            df.index = pd.DatetimeIndex(df.Date)
            monthly_stop_and_search_frequency = df.resample('m').size()
            plt.figure(figsize=(15, 5))
            plt.plot(monthly_stop_and_search_frequency)
            plt.title('Monthly Stop and Search Frequency')
            plt.xlabel('Month')
            plt.ylabel('Number of Stop and Search')
            plt.savefig('static/plots/monthly_stop_and_search_frequency.png')
            return plt.figure

    #Object of Search countplot
    def object_of_search_countplot(self, uk_df):
        df = uk_df.copy()
        object_of_search = df['Object of search'].value_counts()
        top_object_of_search = object_of_search
        order_types = top_object_of_search.index
        plt.figure(figsize=(35, 10))

        plt.yticks(fontsize=25)
        sns.countplot(y='Object of search', data=df, order=order_types)
        plt.savefig('static/plots/object_of_search_count_plot_stop_and_search.png')

        return plt.figure

    #Legislation countplot
    def legislation_countplot(self, uk_df):
        df = uk_df.copy()
        legislation = df['Legislation'].value_counts()
        top_legislation = legislation
        order_types = top_legislation.index
        plt.figure(figsize=(20, 10))
        sns.countplot(y='Legislation', data=df, order=order_types)
        plt.savefig('static/plots/legislation_count_plot_stop_and_search.png')

        return plt.figure

    #Outcome countplot
    def outcome_countplot(self, uk_df):
        df = uk_df.copy()
        outcome = df['Outcome'].value_counts()
        top_outcome = outcome
        order_types = top_outcome.index
        plt.figure(figsize=(15, 10))
        sns.countplot(y='Outcome', data=df, order=order_types)
        plt.savefig('static/plots/outcome_count_plot_stop_and_search.png')

        return plt.figure


'''
ca = CrimeAnalysis()
uk_df= ca.load_data('street', 2021, 1, 2021, 5, 'Staffordshire')
ca.crime_rate_heatmap(uk_df)
'''

