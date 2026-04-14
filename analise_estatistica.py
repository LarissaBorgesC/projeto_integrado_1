import pandas as pd
import numpy as np
from scipy import stats


def gerar_dados(n_fazendas=50, seed=42):
    np.random.seed(seed)

    chuva = np.random.normal(loc=1600, scale=250, size=n_fazendas)
    temperatura = np.random.normal(loc=22, scale=3, size=n_fazendas)
    produtividade = 20 + (chuva * 0.03) + np.random.normal(loc=0, scale=5, size=n_fazendas)

    df = pd.DataFrame({
        "chuva_mm": chuva,
        "temperatura_c": temperatura,
        "produtividade_sacas_ha": produtividade
    })

    return df


def analisar_dados(df):
    media_prod = df["produtividade_sacas_ha"].mean()
    desvio_padrao_prod = df["produtividade_sacas_ha"].std()
    correlacao = df["chuva_mm"].corr(df["produtividade_sacas_ha"])

    intervalo_confianca = stats.t.interval(
        confidence=0.95,
        df=len(df) - 1,
        loc=media_prod,
        scale=stats.sem(df["produtividade_sacas_ha"])
    )

    shapiro_stat, p_valor = stats.shapiro(df["produtividade_sacas_ha"])

    return {
        "media_prod": media_prod,
        "desvio_padrao_prod": desvio_padrao_prod,
        "correlacao": correlacao,
        "intervalo_confianca": intervalo_confianca,
        "shapiro_stat": shapiro_stat,
        "p_valor": p_valor
    }


def interpretar_normalidade(p_valor, alpha=0.05):
    if p_valor < alpha:
        return (
            "Os dados de produtividade não seguem distribuição normal "
            f"(p-valor = {p_valor:.4f} < {alpha})."
        )
    return (
        "Não há evidências para rejeitar a normalidade dos dados de produtividade "
        f"(p-valor = {p_valor:.4f} >= {alpha})."
    )


def main():
    df = gerar_dados()

    resultados = analisar_dados(df)

    print("=== ANÁLISE ESTATÍSTICA DA PRODUTIVIDADE AGRÍCOLA ===")
    print(f"Média da produtividade: {resultados['media_prod']:.2f} sacas/ha")
    print(f"Desvio padrão da produtividade: {resultados['desvio_padrao_prod']:.2f}")
    print(f"Correlação entre chuva e produtividade: {resultados['correlacao']:.4f}")
    print(
        "Intervalo de confiança de 95% para a produtividade média: "
        f"({resultados['intervalo_confianca'][0]:.2f}, {resultados['intervalo_confianca'][1]:.2f})"
    )
    print(f"Estatística do teste Shapiro-Wilk: {resultados['shapiro_stat']:.4f}")
    print(interpretar_normalidade(resultados["p_valor"]))

    print("\nJustificativa do teste:")
    print(
        "Foi utilizado o teste de Shapiro-Wilk por ser apropriado para amostras pequenas "
        "e moderadas, como neste caso com 50 propriedades, sendo amplamente usado para "
        "verificar a normalidade dos dados."
    )


if __name__ == "__main__":
    main()