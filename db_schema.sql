-- Criação das tabelas
CREATE TABLE IF NOT EXISTS fazendas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
    area_ha NUMERIC(10,2) NOT NULL CHECK (area_ha > 0)
);

CREATE TABLE IF NOT EXISTS clima (
    id SERIAL PRIMARY KEY,
    fazenda_id INTEGER NOT NULL REFERENCES fazendas(id) ON DELETE CASCADE,
    data DATE NOT NULL,
    chuva_mm NUMERIC(10,2) NOT NULL CHECK (chuva_mm >= 0),
    temperatura_c NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtividade (
    id SERIAL PRIMARY KEY,
    fazenda_id INTEGER NOT NULL REFERENCES fazendas(id) ON DELETE CASCADE,
    safra VARCHAR(10) NOT NULL,
    sacas_hectare NUMERIC(10,2) NOT NULL CHECK (sacas_hectare >= 0)
);

-- Índices úteis para junções e agregações
CREATE INDEX IF NOT EXISTS idx_clima_fazenda_id ON clima(fazenda_id);
CREATE INDEX IF NOT EXISTS idx_produtividade_fazenda_id ON produtividade(fazenda_id);

-- Consulta de inteligência de mercado
SELECT
    f.regiao,
    p.safra,
    ROUND(AVG(p.sacas_hectare), 2) AS media_produtividade
FROM fazendas f
JOIN produtividade p ON f.id = p.fazenda_id
GROUP BY f.regiao, p.safra
ORDER BY media_produtividade DESC;