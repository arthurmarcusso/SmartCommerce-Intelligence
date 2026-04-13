CREATE TABLE IF NOT EXISTS produtos (
  id INT PRIMARY KEY,
  title VARCHAR(255)  NOT NULL,
  category VARCHAR(100)  NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  discountPercentage DECIMAL(5,2),
  rating DECIMAL(3,1),
  stock INT,
  brand VARCHAR(100),
  availabilityStatus VARCHAR(50),
  minimumOrderQuantity INT
);

CREATE TABLE IF NOT EXISTS clientes (
  id INT PRIMARY KEY,
  nome VARCHAR(150) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  cidade VARCHAR(100),
  estado CHAR(2),
  segmento VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pedidos (
  id INT PRIMARY KEY,
  cliente_id INT NOT NULL,
  data_pedido DATE NOT NULL,
  status VARCHAR(50) NOT NULL,
  valor_total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_pedido (
  id INT PRIMARY KEY,
  pedido_id INT NOT NULL,
  produto_id INT NOT NULL,
  quantidade INT NOT NULL,
  preco_unit DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE IF NOT EXISTS metricas_diarias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data DATE UNIQUE NOT NULL,
  total_pedidos INT NOT NULL DEFAULT 0,
  receita_total DECIMAL(12,2) NOT NULL DEFAULT 0,
  ticket_medio DECIMAL(10,2) NOT NULL DEFAULT 0
);