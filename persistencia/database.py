import sqlite3
import hashlib  # Para o hash da senha


class Database:
    def __init__(self, db_name="locadora.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Conecta ao banco de dados."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Conexão com o banco de dados estabelecida.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            # Em uma aplicação real, você pode querer exibir um messagebox aqui
            # e talvez impedir que a aplicação continue se o BD for essencial.
            # Por exemplo, levantar uma exceção personalizada ou chamar exit().
            # exit() # Descomente se quiser parar a execução em caso de falha na conexão

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")

    def create_tables(self):
        """Cria as tabelas se elas não existirem."""
        if not self.conn or not self.cursor:
            print("Não foi possível criar tabelas: conexão com o banco de dados não estabelecida.")
            return

        try:
            # Tabela Gerentes (Administrador)
            # Ajustado para refletir os campos da História 1 e boas práticas de nomenclatura
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS gerentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_completo TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha_hash TEXT NOT NULL -- Armazenará o hash da senha
                )
            ''')

            # Tabela de Funcionários
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    funcao TEXT,
                    status BOOLEAN NOT NULL DEFAULT 1 -- 1 para Ativo, 0 para Inativo
                )
            ''')

            # Tabela Clientes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    rua TEXT,
                    numero TEXT,
                    bairro TEXT
                )
            ''')

            # --- ALTERADO: Tabela Veículos SEM a coluna 'chassi' ---
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    placa TEXT UNIQUE NOT NULL,
                    cor TEXT,
                    status TEXT NOT NULL DEFAULT 'DISPONIVEL' -- Valores: DISPONIVEL, ALUGADO, MANUTENCAO
                )
            ''')

            # Tabela Locações
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS locacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    veiculo_id INTEGER NOT NULL,
                    funcionario_id INTEGER, -- Adicionado para vincular o funcionário que fez a locação
                    data_inicio TEXT NOT NULL,
                    data_prev_fim TEXT NOT NULL,
                    data_fim_real TEXT, -- Para registrar quando foi devolvido
                    valor_diaria REAL NOT NULL,
                    valor_total REAL, -- Pode ser calculado na devolução
                    observacoes TEXT,
                    status TEXT DEFAULT 'ATIVA', -- Ex: ATIVA, FINALIZADA, ATRASADA
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
                    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
                )
            ''')

            # Tabela Multas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS multas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    locacao_id INTEGER,
                    data_multa TEXT NOT NULL,
                    valor REAL NOT NULL,
                    descricao TEXT NOT NULL,
                    situacao TEXT NOT NULL, -- Ex: Pendente, Paga, Contestada
                    FOREIGN KEY (locacao_id) REFERENCES locacoes(id)
                )
            ''')
            self.conn.commit()
            print("Tabelas verificadas/criadas com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

    # --- Métodos para Gerentes (Administrador) ---
    def admin_existe(self):
        """Verifica se algum gerente (administrador) já foi cadastrado."""
        if not self.cursor: return False
        try:
            self.cursor.execute("SELECT COUNT(id) FROM gerentes")
            count = self.cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"Erro ao verificar admin: {e}")
            return False  # Assume que não existe em caso de erro para permitir o cadastro

    def insert_gerente(self, nome_completo, email, senha_texto_puro):
        """
        Insere o gerente inicial com senha criptografada.
        IMPORTANTE: Em um sistema real, use bcrypt ou Argon2 para hashing de senha, são mais seguros.
        SHA256 é rápido e pode ser vulnerável a ataques de força bruta com hardware moderno.
        """
        if not self.cursor or not self.conn: return False
        # Gerando o hash da senha
        # Para maior segurança, um "salt" deveria ser gerado e armazenado também.
        # Bibliotecas como bcrypt cuidam disso automaticamente.
        senha_hash = hashlib.sha256(senha_texto_puro.encode('utf-8')).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO gerentes (nome_completo, email, senha_hash) VALUES (?, ?, ?)",
                (nome_completo, email, senha_hash)
            )
            self.conn.commit()
            print(f"Gerente {nome_completo} inserido com sucesso.")
            return True
        except sqlite3.IntegrityError:
            print(f"Erro: Email '{email}' já existe para um gerente.")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao inserir gerente: {e}")
            return False

    def get_gerente_by_email(self, email):
        """Busca um gerente pelo email."""
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT * FROM gerentes WHERE email = ?", (email,))
            return self.cursor.fetchone()  # Retorna (id, nome_completo, email, senha_hash) ou None
        except sqlite3.Error as e:
            print(f"Erro ao buscar gerente por email: {e}")
            return None

    # --- Métodos CRUD para Funcionários ---
    def insert_funcionario(self, nome, email, cpf, funcao, status=1):
        """Insere um novo funcionário."""
        if not self.cursor or not self.conn: return False
        try:
            self.cursor.execute(
                "INSERT INTO funcionarios (nome, email, cpf, funcao, status) VALUES (?, ?, ?, ?, ?)",
                (nome, email, cpf, funcao, status)
            )
            self.conn.commit()
            print(f"Funcionário {nome} inserido com sucesso.")
            return True
        except sqlite3.IntegrityError:  # Falha se email ou CPF já existirem
            print(f"Erro: Email '{email}' ou CPF '{cpf}' já existe para um funcionário.")
            return False
        except sqlite3.Error as e:
            print(f"Erro ao inserir funcionário: {e}")
            return False

    def get_all_funcionarios(self):
        """Retorna todos os funcionários."""
        if not self.cursor: return []
        try:
            self.cursor.execute('SELECT id, nome, email, cpf, funcao, status FROM funcionarios')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar todos os funcionários: {e}")
            return []

    def get_funcionario_by_id(self, funcionario_id):
        """Busca um funcionário pelo ID."""
        if not self.cursor: return None
        try:
            self.cursor.execute('SELECT * FROM funcionarios WHERE id = ?', (funcionario_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar funcionário por ID: {e}")
            return None

    # --- Métodos CRUD para Clientes ---
    def insert_cliente(self, nome, cpf, telefone, rua, numero, bairro):
        if not self.cursor or not self.conn: return None
        try:
            self.cursor.execute('''
                INSERT INTO clientes (nome, cpf, telefone, rua, numero, bairro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, telefone, rua, numero, bairro))
            self.conn.commit()
            print(f"Cliente {nome} inserido com sucesso. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid  # Retorna o ID do cliente inserido
        except sqlite3.IntegrityError:
            print(f"Erro: CPF {cpf} já existe para um cliente.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir cliente: {e}")
            return None

    def delete_cliente(self, cliente_id):
        try:
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Cliente com ID {cliente_id} removido com sucesso.")
                return True
            else:
                print(f"Nenhum cliente com ID {cliente_id} foi encontrado.")
                return False
        except Exception as e:
            print("Erro ao excluir cliente:", e)
            return False


    def get_all_clientes(self):
        if not self.cursor: return []
        try:
            self.cursor.execute('SELECT id, nome, cpf, telefone, rua, numero, bairro FROM clientes')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar todos os clientes: {e}")
            return []

    def get_cliente_by_id(self, cliente_id):
        if not self.cursor: return None
        try:
            self.cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar cliente por ID: {e}")
            return None

    def insert_veiculo(self, marca, modelo, ano, placa, cor, status='DISPONIVEL'):
        """Insere um novo veículo, com status opcional (padrão 'DISPONIVEL')."""
        if not self.cursor or not self.conn: return None
        try:
            self.cursor.execute(
                "INSERT INTO veiculos (marca, modelo, ano, placa, cor, status) VALUES (?, ?, ?, ?, ?, ?)",
                (marca, modelo, ano, placa, cor, status)
            )
            self.conn.commit()
            print(f"Veículo {marca} {modelo} (Placa: {placa}) inserido com status '{status}'.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Erro: Placa '{placa}' já existe.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir veículo: {e}")
            return None
    def delete_veiculo(self, veiculo_id):

        try:
            self.cursor.execute('DELETE FROM veiculos WHERE id = ?', (veiculo_id,))
            if self.cursor.rowcount == 0:
                print(f"Nenhum veículo com ID {veiculo_id} foi encontrado.")
                return False
            self.conn.commit()
            print(f"Veículo com ID {veiculo_id} removido com sucesso.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao excluir veículo: {e}")
            return False

    def get_available_veiculos(self):
        """Retorna os veículos com status 'DISPONIVEL'."""
        if not self.cursor: return []
        try:
            self.cursor.execute(
                "SELECT id, marca, modelo, placa FROM veiculos WHERE status = 'DISPONIVEL' ORDER BY marca, modelo")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar veículos disponíveis: {e}")
            return []

    def get_all_veiculos(self):
        """Retorna todos os veículos cadastrados."""
        if not self.cursor: return []
        try:
            # Seleciona os campos que você provavelmente vai querer listar
            self.cursor.execute(
                'SELECT id, marca, modelo, ano, placa, cor, status FROM veiculos ORDER BY marca, modelo')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar todos os veículos: {e}")
            return []

    # --- FIM DO NOVO MÉTODO ---

    def update_veiculo_status(self, veiculo_id, novo_status):
        """Atualiza o status de um veículo."""
        if not self.cursor or not self.conn: return False
        try:
            self.cursor.execute("UPDATE veiculos SET status = ? WHERE id = ?", (novo_status, veiculo_id))
            self.conn.commit()
            print(f"Status do veículo ID {veiculo_id} atualizado para '{novo_status}'.")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar status do veículo: {e}")
            return False

    def delete_locacao(self, locacao_id):
        try:
            self.cursor.execute('DELETE FROM locacoes WHERE id = ?', (locacao_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Locação com ID {locacao_id} removida com sucesso.")
                return True
            else:
                print(f"Nenhuma locação encontrada com ID {locacao_id}.")
                return False
        except sqlite3.Error as e:
            print(f"Erro ao remover locação: {e}")
            return False



    # --- Métodos CRUD para Multas ---
    # def insert_multa(self, locacao_id, data_multa, valor, descricao, situacao):
    # --- Métodos para Locações ---
    def insert_locacao(self, cliente_id, veiculo_id, funcionario_id, data_inicio, data_prev_fim, valor_diaria,
                       observacoes=""):
        """Insere uma nova locação no banco de dados."""
        if not self.cursor or not self.conn: return None
        try:
            self.cursor.execute('''
                INSERT INTO locacoes (cliente_id, veiculo_id, funcionario_id, data_inicio, data_prev_fim, valor_diaria, observacoes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'ATIVA')''',
                                (cliente_id, veiculo_id, funcionario_id, data_inicio, data_prev_fim, valor_diaria,
                                 observacoes))
            self.conn.commit()
            print(
                f"Locação ID {self.cursor.lastrowid} inserida para Cliente ID {cliente_id}, Veículo ID {veiculo_id}, Funcionário ID {funcionario_id}.")
            return self.cursor.lastrowid
        except sqlite3.Error as e:  # Captura erro genérico, IntegrityError é um subtipo
            print(f"Erro ao inserir locação: {e}. Verifique se os IDs de cliente/veículo/funcionário são válidos.")
            return None

    def get_all_locacoes(self):
        """Retorna todas as locações com nomes para exibição na Treeview."""
        if not self.cursor: return []
        try:
            # Query ajustada para pegar os nomes e placa para a Treeview da locação
            self.cursor.execute('''
                SELECT l.id, c.nome AS nome_cliente, v.placa AS placa_veiculo, 
                       l.data_inicio, l.data_prev_fim, l.valor_diaria, l.status
                FROM locacoes l
                JOIN clientes c ON l.cliente_id = c.id
                JOIN veiculos v ON l.veiculo_id = v.id
                ORDER BY l.id DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar todas as locações: {e}")
            return []


# Exemplo de como usar (para teste, se executar este arquivo diretamente)
if __name__ == '__main__':
    db = Database(db_name="teste_locadora.db")  # Usa um BD de teste para não sujar o principal

    # Teste de criação de gerente
    if not db.admin_existe():
        print("Nenhum admin encontrado, criando um...")
        db.insert_gerente("Administrador Principal", "admin@locadora.com", "senha123")
    else:
        print("Admin já existe.")

    gerente = db.get_gerente_by_email("admin@locadora.com")
    if gerente:
        print(f"Gerente encontrado: {gerente[1]}, Email: {gerente[2]}")
        # Para verificar a senha (exemplo básico, não faça isso em produção sem bcrypt.compare):
        # senha_teste_hash = hashlib.sha256("senha123".encode('utf-8')).hexdigest()
        # if gerente[3] == senha_teste_hash:
        # print("Hash da senha corresponde!")
        # else:
        # print("Hash da senha NÃO corresponde.")

    # Teste de funcionário
    db.insert_funcionario("João Silva", "joao.silva@locadora.com", "12345678900", "Atendente", 1)
    funcionarios = db.get_all_funcionarios()
    print(f"Funcionários: {funcionarios}")

    # Teste de cliente
    cliente_id = db.insert_cliente("Maria Souza", "98765432100", "11987654321", "Rua das Flores", "123", "Centro")
    if cliente_id:
        clientes = db.get_all_clientes()
        print(f"Clientes: {clientes}")

    # Teste de veículo
    veiculo_id = db.insert_veiculo("Fiat", "Mobi", 2023, "BRA2E19", "Vermelho", "9BWZZZ377HP123456")
    if veiculo_id:
        veiculos = db.get_all_veiculos()
        print(f"Veículos: {veiculos}")

    # Teste de locação (simulando que o funcionário João (ID 1, se for o primeiro) fez a locação)
    # Você precisaria pegar o ID real do funcionário logado
    funcionario_teste_id = None
    if funcionarios and funcionarios[0]:  # Pega o ID do primeiro funcionário inserido
        funcionario_teste_id = funcionarios[0][0]

    if cliente_id and veiculo_id and funcionario_teste_id:
        db.insert_locacao(cliente_id, veiculo_id, funcionario_teste_id, "2024-05-25", "2024-05-30", 75.50,
                          "Cliente pediu cadeira de bebê.")
        locacoes = db.get_all_locacoes()
        print(f"Locações: {locacoes}")

    db.close()
