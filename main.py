import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def simular_dados(n_fazendas=50, seed=42):
    np.random.seed(seed)

    chuva_mm = np.random.normal(loc=1600, scale=250, size=n_fazendas)
    temperatura_c = np.random.normal(loc=22, scale=3, size=n_fazendas)
    produtividade_sacas_ha = 20 + (chuva_mm * 0.03) + np.random.normal(loc=0, scale=5, size=n_fazendas)

    df = pd.DataFrame({
        "fazenda_id": range(1, n_fazendas + 1),
        "chuva_mm": chuva_mm,
        "temperatura_c": temperatura_c,
        "produtividade_sacas_ha": produtividade_sacas_ha
    })

    return df


def salvar_arquivos_base(df):
    df_clima = df[["fazenda_id", "chuva_mm", "temperatura_c"]].copy()
    df_produtividade = df[["fazenda_id", "produtividade_sacas_ha"]].copy()

    df_clima.to_csv("clima.csv", index=False)
    df_produtividade.to_csv("produtividade.csv", index=False)


def analisar_estatistica(df):
    media_prod = df["produtividade_sacas_ha"].mean()
    std_prod = df["produtividade_sacas_ha"].std()
    correlacao = df["chuva_mm"].corr(df["produtividade_sacas_ha"])
    conf_int = stats.t.interval(
        confidence=0.95,
        df=len(df) - 1,
        loc=media_prod,
        scale=stats.sem(df["produtividade_sacas_ha"])
    )
    shapiro_stat, p_valor = stats.shapiro(df["produtividade_sacas_ha"])

    print("--- RELATÓRIO ESTATÍSTICO ---")
    print(f"Média da produtividade: {media_prod:.2f} sacas/ha")
    print(f"Desvio padrão da produtividade: {std_prod:.2f}")
    print(f"Correlação chuva x produtividade: {correlacao:.4f}")
    print(
        "Intervalo de confiança de 95% para a produtividade média: "
        f"({conf_int[0]:.2f}, {conf_int[1]:.2f})"
    )
    print(f"Teste Shapiro-Wilk (estatística): {shapiro_stat:.4f}")
    print(f"Teste Shapiro-Wilk (p-valor): {p_valor:.4f}")

    if p_valor < 0.05:
        print("Conclusão: rejeita-se a hipótese de normalidade.")
    else:
        print("Conclusão: não há evidências para rejeitar a normalidade.")

    return media_prod, std_prod, correlacao, conf_int, shapiro_stat, p_valor


def treinar_modelo(df):
    X = df[["chuva_mm", "temperatura_c"]]
    y = df["produtividade_sacas_ha"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    previsoes = modelo.predict(X_test)

    r2 = r2_score(y_test, previsoes)
    mae = mean_absolute_error(y_test, previsoes)

    print("\n--- PERFORMANCE DO MODELO ---")
    print(f"R²: {r2:.4f}")
    print(f"MAE: {mae:.2f} sacas/ha")

    return modelo, r2, mae


def main():
    df = simular_dados()
    salvar_arquivos_base(df)
    analisar_estatistica(df)
    treinar_modelo(df)


if __name__ == "__main__":
    main()