import sqlite3

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
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            # Em uma aplicação real, você pode querer exibir um messagebox aqui
            exit() # Para impedir que a aplicação continue sem BD

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Cria as tabelas se elas não existirem."""
        try:
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
            # Tabela Veículos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS veiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marca TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    placa TEXT UNIQUE NOT NULL,
                    cor TEXT,
                    chassi TEXT UNIQUE
                )
            ''')
            # Tabela Locações
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS locacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    veiculo_id INTEGER NOT NULL,
                    data_inicio TEXT NOT NULL,
                    data_prev_fim TEXT NOT NULL,
                    valor_diaria REAL NOT NULL,
                    observacoes TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
                )
            ''')
            # Tabela Multas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS multas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    locacao_id INTEGER, -- Pode ser nulo se a multa não for associada a uma locação específica, mas a um veículo.
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

    # --- Métodos CRUD para Clientes ---
    def insert_cliente(self, nome, cpf, telefone, rua, numero, bairro):
        try:
            self.cursor.execute('''
                INSERT INTO clientes (nome, cpf, telefone, rua, numero, bairro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, telefone, rua, numero, bairro))
            self.conn.commit()
            print(f"Cliente {nome} inserido com sucesso. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid # Retorna o ID do cliente inserido
        except sqlite3.IntegrityError:
            print(f"Erro: CPF {cpf} já existe.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir cliente: {e}")
            return None

    def get_all_clientes(self):
        self.cursor.execute('SELECT * FROM clientes')
        return self.cursor.fetchall()

    def get_cliente_by_id(self, cliente_id):
        self.cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        return self.cursor.fetchone()

    # --- Métodos CRUD para Veículos ---
    def insert_veiculo(self, marca, modelo, ano, placa, cor):
        try:
            self.cursor.execute('''
                INSERT INTO veiculos (marca, modelo, ano, placa, cor)
                VALUES (?, ?, ?, ?, ?)
            ''', (marca, modelo, ano, placa, cor))
            self.conn.commit()
            print(f"Veículo {marca}/{modelo} inserido com sucesso. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Erro: Placa {placa} já existe.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir veículo: {e}")
            return None

    def get_all_veiculos(self):
        self.cursor.execute('SELECT * FROM veiculos')
        return self.cursor.fetchall()

    def get_veiculo_by_id(self, veiculo_id):
        self.cursor.execute('SELECT * FROM veiculos WHERE id = ?', (veiculo_id,))
        return self.cursor.fetchone()

    # --- Métodos CRUD para Locações ---
    def insert_locacao(self, cliente_id, veiculo_id, data_inicio, data_prev_fim, valor_diaria, observacoes):
        try:
            self.cursor.execute('''
                INSERT INTO locacoes (cliente_id, veiculo_id, data_inicio, data_prev_fim, valor_diaria, observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cliente_id, veiculo_id, data_inicio, data_prev_fim, valor_diaria, observacoes))
            self.conn.commit()
            print(f"Locação para Cliente ID {cliente_id} e Veículo ID {veiculo_id} inserida com sucesso. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Erro de integridade ao inserir locação. Verifique IDs de Cliente/Veículo.")
            return None
        except sqlite3.Error as e:
            print(f"Erro ao inserir locação: {e}")
            return None

    # --- Métodos CRUD para Multas ---
    def insert_multa(self, locacao_id, data_multa, valor, descricao, situacao):
        try:
            self.cursor.execute('''
                INSERT INTO multas (locacao_id, data_multa, valor, descricao, situacao)
                VALUES (?, ?, ?, ?, ?)
            ''', (locacao_id, data_multa, valor, descricao, situacao))
            self.conn.commit()
            print(f"Multa para Locação ID {locacao_id} inserida com sucesso. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao inserir multa: {e}")
            return None