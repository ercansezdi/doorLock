
import geopandas as gpd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    plt.rcParams['figure.figsize'] = (20, 10)
    df_places = gpd.read_file('algiers_algeria_expanded_places.geojson')
    df_admin = gpd.read_file('algiers_algeria_expanded_admin.geojson')
