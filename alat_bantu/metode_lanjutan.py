"""Perhitungan lanjutan untuk pengajar; ikut dibagikan dalam paket data.

Peserta cukup memakai fungsi pada notebook. Implementasi terbuka di sini
agar rumus dan cara estimasinya tetap dapat diperiksa.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from statsmodels.tools.sm_exceptions import PerfectSeparationError


def coba_logit(rumus, data):
    """Demo separation: tampilkan kegagalan MLE tanpa menghentikan kelas."""
    try:
        hasil = smf.logit(rumus, data=data).fit(disp=0)
    except (PerfectSeparationError, np.linalg.LinAlgError) as error:
        return pd.Series({"status": "MLE tidak dapat diestimasi", "sebab": str(error)})
    print("MLE konvergen:", hasil.mle_retvals["converged"])
    print("Koefisien pada data terpisah tidak layak dipakai untuk inferensi.")
    return hasil.params.round(3)


def _negloglik_tobit(parameter, X, y, batas):
    """Y = max(batas, X beta + error), error normal dengan sigma > 0."""
    beta = parameter[:-1]
    sigma = np.exp(parameter[-1])
    mu = X @ beta
    tersensor = y <= batas
    loglik = np.empty(len(y))
    loglik[tersensor] = norm.logcdf((batas - mu[tersensor]) / sigma)
    loglik[~tersensor] = norm.logpdf((y[~tersensor] - mu[~tersensor]) / sigma) - np.log(
        sigma
    )
    return -loglik.sum()


def estimasi_tobit(data, y, x, batas=0.0):
    """Tobit tersensor kiri via MLE, dengan OLS pada sampel yang sama.

    Yang ditampilkan adalah koefisien laten dan sigma, tanpa klaim p-value.
    Nilai nol diasumsikan hasil sensor, bukan otomatis bukti adanya sensor.
    """
    sampel = data[[y] + x].dropna()
    if not np.isfinite(sampel.to_numpy(dtype=float)).all():
        raise ValueError("Data Tobit harus berupa angka berhingga.")
    if (sampel[y] < batas).any():
        raise ValueError("Ada nilai Y di bawah batas sensor.")
    X = sm.add_constant(sampel[x], has_constant="add")
    y_array = sampel[y].to_numpy(dtype=float)
    X_array = X.to_numpy(dtype=float)
    if np.linalg.matrix_rank(X_array) < X_array.shape[1]:
        raise ValueError("Variabel penjelas Tobit memiliki kolinearitas sempurna.")
    if (y_array > batas).sum() < X_array.shape[1]:
        raise ValueError(
            "Observasi tanpa sensor belum cukup untuk contoh estimasi ini."
        )
    ols = LinearRegression().fit(sampel[x], y_array)
    beta_ols = np.r_[ols.intercept_, ols.coef_]
    residu_ols = y_array - ols.predict(sampel[x])
    sigma_awal = max(float(np.std(residu_ols)), 1e-6)
    awal = np.r_[beta_ols, np.log(sigma_awal)]
    hasil = minimize(
        _negloglik_tobit,
        awal,
        args=(X_array, y_array, batas),
        method="Nelder-Mead",
        options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-8},
    )
    if not hasil.success or not np.isfinite(hasil.fun):
        raise RuntimeError("Estimasi Tobit belum konvergen: " + str(hasil.message))
    tabel = pd.DataFrame({"OLS": beta_ols, "Tobit": hasil.x[:-1]}, index=X.columns)
    mse_ols = np.sum(residu_ols**2) / (len(sampel) - X_array.shape[1])
    tabel.loc["sigma"] = [np.sqrt(mse_ols), np.exp(hasil.x[-1])]
    print("Tobit konvergen:", hasil.success)
    print("Observasi tersensor:", int((y_array <= batas).sum()), "dari", len(y_array))
    return tabel
