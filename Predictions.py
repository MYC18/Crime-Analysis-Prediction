import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fbprophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

class Predictions:
    def __init__(self):
        self.path = "Data"
        self.save_path = "static/CSVs"

    def predict_FB(self):
        path = 'Data'
        files = glob.glob(path + '/*' + '/*' + '*-street.csv')
        files.sort()

        UK_df = pd.DataFrame()
        for i in range(len(files)):
            temp_df = UK_df
            df = pd.read_csv(str(files[i]))
            UK_df = pd.concat([df, temp_df], ignore_index=True)

        # Preprocessing
        UK_df.drop(['Crime ID', 'Reported by', 'Falls within', 'LSOA code', 'Context'], inplace=True, axis=1)
        UK_df.Month = pd.to_datetime(UK_df.Month, format='%Y/%m')
        UK_df.index = pd.DatetimeIndex(UK_df.Month)
        monthly_crime_frequency = UK_df.resample('m').size()
        UK_Prophet = monthly_crime_frequency.reset_index()
        UK_Prophet.columns = ['Date', 'Crime Count']

        UK_Prophet_Final = UK_Prophet.rename(columns={'Date': 'ds', 'Crime Count': 'y'})
        model = Prophet(weekly_seasonality=True, daily_seasonality=True)
        model.fit(UK_Prophet_Final)
        future = model.make_future_dataframe(periods=(365 * 2))
        forecast = model.predict(future)
        figure = model.plot(forecast, xlabel='Date', ylabel='Crime Count')
        plt.show()

        figure = model.plot_components(forecast)
        plt.show()

    def Linear_Regression(self):
        path = 'Data'
        files = glob.glob(path + '/*' + '/*' + '*-street.csv')
        files.sort()
        UK_df = pd.DataFrame()
        for i in range(len(files)):
            temp_df = UK_df
            df = pd.read_csv(str(files[i]))
            UK_df = pd.concat([df, temp_df], ignore_index=True)

        UK_df.drop(['Crime ID', 'Reported by', 'Falls within', 'LSOA code', 'Context'], inplace=True, axis=1)

        UK_df.Month = pd.to_datetime(UK_df.Month, format='%Y/%m')
        UK_df.index = pd.DatetimeIndex(UK_df.Month)

        monthly_crime_frequency = UK_df.resample('m').size()

        UK_Prophet = monthly_crime_frequency.reset_index()
        UK_Prophet.columns = ['Date', 'Crime Count']
        UK_Prophet_Final = UK_Prophet.rename(columns={'Date': 'ds', 'Crime Count': 'y'})
        df = UK_Prophet_Final
        x = np.arange(df['ds'].size)

        fit=np.polyfit(x, df['y'], deg=1)
        print('Slope: ', fit[0])
        print('Intercept: ', fit[1])

        fit_function=np.poly1d(fit)

        plt.figure(figsize=(15,5))
        plt.plot(df['ds'], fit_function(x))
        plt.plot(df['ds'], df['y'])
        plt.xlabel('Date')
        plt.ylabel('Crime Count')
        plt.title('Monthly Linear Regression')
        plt.show()

        plt.figure(figsize=(15,5))
        plt.plot(df['ds'], fit_function(x))
        plt.scatter(df['ds'], df['y'])
        plt.xlabel('Date')
        plt.ylabel('Crime Count')
        plt.title('Monthly Linear Regression')
        plt.show()



    def Random_Forest_stop_and_search(self):
        df = pd.read_csv('Crime_Prediction_Random_Forest_Stop_and_Search_v3.csv')
        df.dropna(subset=['Longitude', 'Latitude', 'Legislation', 'Object of search', 'Outcome'], inplace=True)
        df.drop(['Year', 'Unnamed: 0'], inplace=True, axis=1)
        labels = np.array(df['Outcome'])
        features = df.drop(['Outcome'], axis=1)
        feature_list = list(features.columns)
        features = np.array(features)
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state= 42)
        rf_model = RandomForestRegressor(n_estimators=200, max_depth=20)
        rf_model.fit(train_features, train_labels)
        predictions = rf_model.predict(test_features)
        errors = abs(predictions - test_labels)
        # Mean absolute percentage error
        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        return accuracy

    def KNN_stop_and_search(self):
        df = pd.read_csv('Crime_Prediction_Random_Forest_Stop_and_Search_v3.csv')
        df.dropna(subset=['Longitude', 'Latitude', 'Legislation', 'Object of search', 'Outcome'], inplace=True)
        df.drop(['Year', 'Unnamed: 0'], inplace=True, axis=1)
        labels = np.array(df['Outcome'])
        features = df.drop(['Outcome'], axis=1)
        feature_list = list(features.columns)
        features = np.array(features)
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                                    random_state=42)
        train_scores = []
        test_scores = []
        for k in range(1, 20, 2):
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(train_features, train_labels)
            train_score = knn.score(train_features, train_labels)
            test_score = knn.score(test_features, test_labels)
            train_scores.append(train_score)
            test_scores.append(test_score)
            print(f"k: {k}, Train/Test Score: {train_score:.3f}/{test_score:.3f}")

        plt.plot(range(1, 20, 2), train_scores, marker='o')
        plt.plot(range(1, 20, 2), test_scores, marker="x")
        plt.xlabel("k neighbors")
        plt.ylabel("Testing accuracy Score")
        plt.show()

















