from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sqlite3
import sys

conexao = sqlite3.connect("usuarios.db")
meu_cursor = conexao.cursor()

meu_cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    senha TEXT
)
""")
conexao.commit()

janelas_abertas = []

def entrada():
    tela_entrada = QWidget()
    tela_entrada.setWindowTitle("Você entrou!!!")
    tela_entrada.resize(310, 350)
    tela_entrada.setStyleSheet("background-color: lightblue;")

    layout_entrada = QVBoxLayout()

    texto = QLabel("Você entrou com sucesso!")
    texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
    texto.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout_entrada.addWidget(texto)

    tela_entrada.setLayout(layout_entrada)
    tela_entrada.show()

    janelas_abertas.append(tela_entrada)


def abrir_janela_cadastro():
    tela_cadastro = QWidget()
    tela_cadastro.setWindowTitle("Cadastro")
    tela_cadastro.resize(310, 350)
    tela_cadastro.setStyleSheet("background-color: lightblue;")

    layout_cadastro = QVBoxLayout()

    titulo = QLabel("CADASTRO")
    titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
    layout_cadastro.addWidget(titulo)

    linha = QFrame()
    linha.setFrameShape(QFrame.Shape.HLine)
    linha.setFrameShadow(QFrame.Shadow.Sunken)
    linha.setStyleSheet("background-color: blue; height: 2px;")
    layout_cadastro.addWidget(linha)

    layout_cadastro.addSpacing(20)

    global nome, email, senha

    nome = QLineEdit()
    nome.setPlaceholderText("Nome completo")
    nome.setStyleSheet("background-color: white;")
    layout_cadastro.addWidget(nome)

    layout_cadastro.addSpacing(25)

    email = QLineEdit()
    email.setPlaceholderText("Email")
    email.setStyleSheet("background-color: white;")
    layout_cadastro.addWidget(email)

    layout_cadastro.addSpacing(25)

    senha = QLineEdit()
    senha.setPlaceholderText("Senha")
    senha.setEchoMode(QLineEdit.EchoMode.Password) 
    senha.setStyleSheet("background-color: white;")
    layout_cadastro.addWidget(senha)

    layout_cadastro.addSpacing(25)

    botao_cadastrar = QPushButton("Cadastrar")
    botao_cadastrar.setStyleSheet("background-color: skyblue;")
    layout_cadastro.addWidget(botao_cadastrar)

    def salvar_usuario():
        nome = nome.text()
        email = email.text()
        senha = senha.text()

        if nome == "" or email == "" or senha == "":
            QMessageBox.warning(tela_cadastro, "Erro", "Preencha todos os campos!")

            return
            
        
        meu_cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = meu_cursor.fetchone()

        if usuario:
            QMessageBox.warning(tela_cadastro, "Erro", "Email já cadastrado.")
        else:
            meu_cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conexao.commit()
            QMessageBox.information(tela_cadastro, "Sucesso", "Cadastro realizado com sucesso!")
            tela_cadastro.close()

    botao_cadastrar.clicked.connect(salvar_usuario)

    tela_cadastro.setLayout(layout_cadastro)
    tela_cadastro.show()

    janelas_abertas.append(tela_cadastro)


def fazer_login():
    email = input_email.text().strip()
    senha = input_senha.text().strip()

    if email == "" or senha == "":
        QMessageBox.warning(janela, "Erro", "Preencha todos os campos!")

        return

    meu_cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = meu_cursor.fetchone()

    if usuario:
        entrada()
    else:
        QMessageBox.warning(janela, "Erro", "Email ou senha incorretos.")


app = QApplication([])

janela = QWidget()
janela.resize(310, 350)
janela.setWindowTitle("Login")
janela.setStyleSheet("background-color: lightblue;")

layout = QVBoxLayout()

titulo = QLabel("LOGIN")
titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
layout.addWidget(titulo)

linha = QFrame()
linha.setFrameShape(QFrame.Shape.HLine)
linha.setFrameShadow(QFrame.Shadow.Sunken)
linha.setStyleSheet("background-color: blue; height: 2px;")
layout.addWidget(linha)

layout.addSpacing(25)

input_email = QLineEdit()
input_email.setPlaceholderText("Email")
input_email.setStyleSheet("background-color: white;")
layout.addWidget(input_email)

layout.addSpacing(20)

input_senha = QLineEdit()
input_senha.setPlaceholderText("Senha")
input_senha.setEchoMode(QLineEdit.EchoMode.Password)
input_senha.setStyleSheet("background-color: white;")
layout.addWidget(input_senha)

layout.addSpacing(120)

botao_login = QPushButton("Entrar")
botao_login.setStyleSheet("background-color: skyblue;")
botao_login.clicked.connect(fazer_login)
layout.addWidget(botao_login)

botao_cadastro = QPushButton("Não tenho cadastro")
botao_cadastro.setStyleSheet("background-color: skyblue;")
botao_cadastro.clicked.connect(abrir_janela_cadastro)
layout.addWidget(botao_cadastro)

janela.setLayout(layout)
janela.show()

sys.exit(app.exec())