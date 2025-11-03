import http.server
import socketserver
import os
import psycopg2
import json
from datetime import datetime

# --- Configuração do Banco de Dados ---
# Lê as credenciais do banco de dados a partir de variáveis de ambiente
db_host = os.environ.get("DB_HOST", "localhost")
db_user = os.environ.get("DB_USER", "user")
db_password = os.environ.get("DB_PASSWORD", "password")
db_name = os.environ.get("DB_NAME", "database")

def query_database():
    """
    Conecta ao banco de dados, executa uma consulta e retorna uma lista de dicionários.
    """
    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name
        )
        cursor = conn.cursor()
        # Altere a query para a sua necessidade
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN pac.nome_social IS NOT NULL THEN pac.nome_social
                    ELSE pac.nome
                END AS nome,
                sala.sala,
                unf.descricao,
                esp.nome_especialidade AS especialidade,
                unf.seq,
                con.dthr_inicio,
                con.dthr_fim,
                CASE con.ret_seq 
                        WHEN 10 THEN 'PACIENTE ATENDIDO'
                        WHEN 30 THEN 'PROFISSIONAL FALTOU'
                        WHEN 40 THEN 'PACIENTE FALTOU'
                        WHEN 9  THEN 'PACIENTE AGENDADO'
                        WHEN 50 THEN 'PACIENTE DESISTIU CONS'
                        WHEN 20 THEN 'AGUARDANDO ATENDIMENTO'
                        WHEN 60 THEN 'EM ATENDIMENTO'
                        ELSE 'OUTRO'
                    END AS status
                FROM 
                agh.aac_consultas con
                LEFT JOIN agh.aip_pacientes pac
                ON pac.codigo = con.pac_codigo 
                LEFT JOIN agh.agh_microcomputadores micro
                ON micro.ip = con.nome_micro 
                LEFT JOIN agh.aac_unid_funcional_salas sala
                ON micro.unf_seq = sala.unf_seq 
                AND micro.usl_sala = sala.sala
                LEFT JOIN agh.agh_unidades_funcionais unf
                ON sala.unf_seq = unf.seq
                LEFT JOIN agh.aac_grade_agendamen_consultas grd
                ON con.grd_seq = grd.seq
                LEFT JOIN agh.agh_especialidades esp
                ON grd.esp_seq = esp.seq
                WHERE con.dthr_inicio IS NOT NULL
                AND con.dthr_inicio >= NOW() - INTERVAL '30 minutes'
                ORDER BY con.dthr_inicio DESC
            """)
        
        # Pega o nome das colunas
        columns = [desc[0] for desc in cursor.description]
        # Busca todos os resultados e cria uma lista de dicionários
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        print(f"Resultado da consulta ao banco de dados: {len(result)} registros encontrados.")
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Erro ao conectar ou consultar o banco de dados: {e}")
        return []

# --- Configuração do Servidor Web ---
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if self.path == '/api/pacientes':
                data = query_database()
            else:
                data = {"error": f"Endpoint '{self.path}' not found. Please use '/api/pacientes'."}
            
            def json_converter(o):
                if isinstance(o, datetime):
                    return o.isoformat()
            
            json_data = json.dumps(data, default=json_converter)
            self.wfile.write(json_data.encode('utf-8'))
            return

        if self.path == '/':
            self.path = 'painel.html'
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# --- Inicialização ---
if __name__ == "__main__":
    # Inicia o servidor web
    PORT = 8000
    Handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor iniciado em http://localhost:{PORT}")
        print(f"Endpoint de dados disponível em http://localhost:{PORT}/api/pacientes")
        httpd.serve_forever()
