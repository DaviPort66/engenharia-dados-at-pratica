import os
import psycopg2
from psycopg2 import errors
from dotenv import load_dotenv

load_dotenv(os.getenv("ENV_FILE", ".env"))


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "universidade"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options="-c search_path=universidade,public",
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
    )


def executar(sql, params=None, fetch=False):
    """Executa um comando. Retorna as linhas (fetch=True) ou o nº de linhas afetadas.
    Traduz os erros do Postgres em mensagens claras (ValueError)."""
    conn = conectar()
    try:
        with conn, conn.cursor() as cur:  # 'with conn' faz commit/rollback
            cur.execute(sql, params)
            return cur.fetchall() if fetch else cur.rowcount
    except errors.UniqueViolation:
        raise ValueError("Violação de chave/unicidade: já existe um registro com esse valor.")
    except errors.ForeignKeyViolation:
        raise ValueError("Violação de integridade referencial: o registro referenciado não existe "
                         "ou ainda é usado por outra tabela.")
    except errors.NotNullViolation:
        raise ValueError("Campo obrigatório (NOT NULL) não informado.")
    except errors.CheckViolation:
        raise ValueError("Valor viola uma restrição CHECK da tabela.")
    except (errors.InvalidTextRepresentation, errors.InvalidDatetimeFormat,
            errors.NumericValueOutOfRange, errors.StringDataRightTruncation):
        raise ValueError("Valor inválido para o domínio do campo (formato, tamanho ou opção do enum).")
    except psycopg2.Error as e:
        raise ValueError(f"Erro no banco: {e.pgerror or e}")
    finally:
        conn.close()


def atualizar_campos(tabela, campos, permitidos, condicao, params_cond):
    """Monta e executa um UPDATE só com os campos informados (e permitidos)."""
    campos = {k: v for k, v in campos.items() if k in permitidos}
    if not campos:
        raise ValueError("Nenhum campo para atualizar.")
    sets = ", ".join(f"{col} = %s" for col in campos)
    return executar(f"UPDATE {tabela} SET {sets} WHERE {condicao}",
                    (*campos.values(), *params_cond))
