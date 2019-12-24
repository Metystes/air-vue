#==============================
# Just started working on that
#==============================
from scipy import interpolate
import pickle
from os import path
import pandas as pd
import numpy as np


class Interpolation():
    def __init__(self):
        self.model_path = path.join('models', 'interpolation.pk')

    def train(self, coor, vals):
        """Training Interpolation model and saving it to pickle format.
        
        Parameters
        ----------
        coor : ndarray of floats
            Data point coordinates
        vals : ndarray of float
            Data values.
        """
        interp = interpolate.LinearNDInterpolator(coor, vals)
        with open(self.model_path, 'wb') as f:
            pickle.dump(interp, f)

    def predict_grid(self, x_min, x_max, y_min, y_max, step=0.01):
        """Calculating interpolation for the grid created by given x_min_max
           and y_min_max by given step.
        
        Parameters
        ----------
        x_min : float
            Min grid value on x coordinate
        x_max : float
            Max grid value on x coordinate
        y_min : float
            Min grid value on y coordinate
        y_max : float
            Max grid value on y coordinate
        step : float, optional
            How dense should the grid be, by default 0.01
        
        Returns
        -------
        df
            Returns pandas dataframe, with cols: x, y
        """
        with open(self.model_path, 'rb') as f:
            interp = pickle.load(f)
        grid = self._generate_grid(x_min, x_max, y_min, y_max, step)
        print('Starting Prediction')
        grid.loc[:, "val"] = grid.apply(lambda x: interp(x[0], x[1]), axis=1)
        return grid

    def _generate_grid(self, x_min, x_max, y_min, y_max, step=0.01):
        x = np.arange(x_min, x_max, step)
        y = np.arange(y_min, y_max, step)
        xv, yv = np.meshgrid(x, y, sparse=False, indexing='ij')
        grid = np.transpose(
            np.array([np.matrix.flatten(xv), np.matrix.flatten(yv)]))
        grid = pd.DataFrame(grid, columns=['x', 'y'])
        return grid


# %% Tests
Tests = False
if Tests is True:
    from src.data.createDB import (Database, db_backend, db_name)
    dbms = Database(db_backend, db_name)
    query = """WITH ranked AS(
        SELECT m.*, ROW_NUMBER() OVER(PARTITION BY id ORDER BY time DESC) as rm
        FROM `airly_raw_data` as m
    ), locs as (SELECT id, lat, lng, city, street FROM 'airly_locs')
    SELECT r.*, l.lat, l.lng
    FROM ranked r LEFT JOIN locs as l on l.id = r.id where rm = 1
    """
    data = dbms.pd_readSQL(sql=query)
    inter = Interpolation()
    inter.train(data.loc[:, ['lat', 'lng']].values, data.loc[:, 'pm10'])
    data_pred = inter.predict_grid(49.8, 50.24, 19.6, 20.25, 0.001)
    print(data_pred.head())
