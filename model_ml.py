import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error


def treinar_modelo(arquivo="dataset_unificado.csv"):
    df = pd.read_csv(arquivo)

    colunas = [c.lower().strip() for c in df.columns]
    df.columns = colunas

    if "produtividade" in df.columns:
        target = "produtividade"
    elif "produtividade_sacas_ha" in df.columns:
        target = "produtividade_sacas_ha"
    elif "produtividade_ha" in df.columns:
        target = "produtividade_ha"
    else:
        raise ValueError("Coluna de produtividade não encontrada no dataset.")

    if "chuva" in df.columns:
        chuva_col = "chuva"
    elif "chuva_mm" in df.columns:
        chuva_col = "chuva_mm"
    else:
        raise ValueError("Coluna de chuva não encontrada no dataset.")

    if "temp" in df.columns:
        temp_col = "temp"
    elif "temperatura_c" in df.columns:
        temp_col = "temperatura_c"
    elif "temperatura" in df.columns:
        temp_col = "temperatura"
    else:
        raise ValueError("Coluna de temperatura não encontrada no dataset.")

    X = df[[chuva_col, temp_col]]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("--- PERFORMANCE DO MODELO ---")
    print(f"R²: {r2:.4f}")
    print(f"MAE: {mae:.2f} sacas/ha")

    return modelo, r2, mae


if __name__ == "__main__":
    treinar_modelo()