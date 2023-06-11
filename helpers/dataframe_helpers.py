from __future__ import annotations

import pandas as pd
import numpy as np
import scipy


def bracket_value(df: pd.Dataframe, value: str, lower: float, upper: float)->pd.DataFrame:
    mask_a_resist=(df[value]>=lower) & (df[value]<=upper)
    df_2=df.loc[mask_a_resist]
    return df_2

def get_max_min(df: pd.Dataframe, col: str)->dict(float):
    ends={"min": None, "max":None}
    ends.update({"min":df[col].min()})
    ends.update({"max":df[col].max()})
    return ends

def get_slope(_x1, _y1, _x2, _y2):
    slope = (_y2-_y1)/(_x2-_x1)
    return slope

def get_np_slope_and_intercept(_x: np.ndarray, _y: np.ndarray, _degree: int)->list(float):
    series=np.polynomial.polynomial.Polynomial.fit(_x, _y, _degree)
    return series.convert().coef

    