import pandas as pd
import os


def run_etl():
    print("🚀 Iniciando Pipeline ETL da EmpresaX...")

    clima_file = "clima.csv"
    produtividade_file = "produtividade.csv"
    output_file = "dataset_unificado.csv"

    if not os.path.exists(clima_file):
        print(f"❌ Erro: arquivo '{clima_file}' não encontrado.")
        return

    if not os.path.exists(produtividade_file):
        print(f"❌ Erro: arquivo '{produtividade_file}' não encontrado.")
        return

    # Extract
    df_clima = pd.read_csv(clima_file)
    df_produtividade = pd.read_csv(produtividade_file)

    # Transform
    df_clima = df_clima.drop_duplicates().dropna()
    df_produtividade = df_produtividade.drop_duplicates().dropna()

    df_clima.columns = [col.strip().lower() for col in df_clima.columns]
    df_produtividade.columns = [col.strip().lower() for col in df_produtividade.columns]

    if "fazenda_id" not in df_clima.columns or "fazenda_id" not in df_produtividade.columns:
        print("❌ Erro: coluna 'fazenda_id' não encontrada em um dos arquivos.")
        return

    df_unificado = pd.merge(
        df_clima,
        df_produtividade,
        on="fazenda_id",
        how="inner"
    )

    if "chuva_mm" in df_unificado.columns and "produtividade_sacas_ha" in df_unificado.columns:
        df_unificado["eficiencia_chuva"] = (
            df_unificado["produtividade_sacas_ha"] / df_unificado["chuva_mm"]
        )

    # Load
    df_unificado.to_csv(output_file, index=False)

    print(f"✅ Sucesso! {len(df_unificado)} registros processados e salvos em '{output_file}'.")


if __name__ == "__main__":
    run_etl()