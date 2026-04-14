import os
import pandas as pd
import pytest
from etl_pipeline import run_etl


# Teste 1: verificar se os arquivos de entrada existem e possuem colunas mínimas esperadas
def test_input_files_exist_and_have_expected_columns():
    assert os.path.exists("clima.csv"), "Arquivo clima.csv não encontrado."
    assert os.path.exists("produtividade.csv"), "Arquivo produtividade.csv não encontrado."

    df_clima = pd.read_csv("clima.csv")
    df_prod = pd.read_csv("produtividade.csv")

    assert not df_clima.empty
    assert not df_prod.empty

    assert "fazenda_id" in df_clima.columns
    assert "chuva_mm" in df_clima.columns
    assert "temperatura_c" in df_clima.columns

    assert "fazenda_id" in df_prod.columns
    assert "produtividade_sacas_ha" in df_prod.columns


# Teste 2: verificar se o ETL lida com ausência de arquivo sem lançar exceção inesperada
def test_etl_missing_file():
    temp_name = "clima_backup.csv"

    if os.path.exists("clima.csv"):
        os.rename("clima.csv", temp_name)

    try:
        run_etl()
    except Exception as e:
        pytest.fail(f"O ETL falhou ao lidar com arquivo ausente: {e}")
    finally:
        if os.path.exists(temp_name):
            os.rename(temp_name, "clima.csv")


# Teste 3: verificar se o arquivo final é gerado corretamente
def test_etl_generates_output_file():
    run_etl()
    assert os.path.exists("dataset_unificado.csv"), "O arquivo dataset_unificado.csv não foi gerado."


# Teste 4: verificar se o dataset unificado contém as colunas esperadas
def test_etl_output_columns():
    run_etl()
    df_unificado = pd.read_csv("dataset_unificado.csv")

    assert not df_unificado.empty
    assert "fazenda_id" in df_unificado.columns
    assert "chuva_mm" in df_unificado.columns
    assert "temperatura_c" in df_unificado.columns
    assert "produtividade_sacas_ha" in df_unificado.columns


# Teste 5: verificar se a coluna opcional de eficiência hídrica foi criada
def test_etl_creates_eficiencia_chuva():
    run_etl()
    df_unificado = pd.read_csv("dataset_unificado.csv")

    assert "eficiencia_chuva" in df_unificado.columns


# Teste 6: verificar se não há nulos no dataset final
def test_etl_output_no_nulls():
    run_etl()
    df_unificado = pd.read_csv("dataset_unificado.csv")

    assert df_unificado.isnull().sum().sum() == 0, "Dataset unificado contém valores nulos"


# Teste 7: verificar se o merge não perdeu registros (número esperado)
def test_etl_merge_completeness():
    run_etl()
    df_unificado = pd.read_csv("dataset_unificado.csv")

    assert len(df_unificado) > 0, "Merge resultou em dataset vazio"
    assert len(df_unificado) <= 50, "Merge resultou em mais registros que o esperado"