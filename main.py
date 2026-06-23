import os
import random
import sys

# Se estiver rodando no PC, simula a proporção de tela de um celular vertical
if sys.platform not in ('android', 'ios'):
    from kivy.config import Config
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

# Importa o módulo do banco de dados local
import database

# Pool de caminhos de imagens das cartas (geradas pelo gerar_imagens.py)
POOL_IMAGENS = [f"imagens/carta_{i}.png" for i in range(1, 19)]

class CardButton(Button):
    """
    Representa uma carta no tabuleiro.
    Os estados e imagens da carta são atualizados dinamicamente pelo Kivy.
    """
    is_revealed = BooleanProperty(False)
    is_matched = BooleanProperty(False)
    card_image = StringProperty('')
    card_value = StringProperty('')
    card_index = NumericProperty(0)


class StartScreen(Screen):
    """
    Tela inicial do jogo. Controla a validação do nome do jogador,
    seleção de dificuldade e navegação inicial.
    """
    def iniciar_jogo(self):
        nome = self.ids.name_input.text.strip()
        if not nome:
            self.ids.error_label.text = 'Por favor, digite seu nome para jogar!'
            return
        
        self.ids.error_label.text = ''
        
        # Determina a dificuldade com base nos ToggleButtons
        if self.ids.btn_easy.state == 'down':
            dificuldade = 'facil'
        else:
            dificuldade = 'dificil'
            
        # Transiciona para a tela do jogo e inicia a partida
        self.manager.current = 'game'
        game_screen = self.manager.get_screen('game')
        game_screen.iniciar_partida(nome, dificuldade)

    def ver_placar(self):
        self.manager.current = 'leaderboard'


class VictoryPopup(Popup):
    """
    Popup que aparece ao finalizar o jogo com sucesso.
    """
    def __init__(self, game_screen, jogadas, tempo_formatado, **kwargs):
        super().__init__(**kwargs)
        self.game_screen = game_screen
        self.ids.stats_label.text = f"Jogadas: {jogadas}  |  Tempo: {tempo_formatado}"

    def jogar_novamente(self):
        self.dismiss()
        self.game_screen.reiniciar_jogo()

    def ir_para_menu(self):
        self.dismiss()
        self.game_screen.voltar_menu()


class GameScreen(Screen):
    """
    Tela principal da partida do Jogo da Memória.
    Controla o cronômetro, a renderização do tabuleiro e a lógica de combinação de cartas.
    """
    jogador_nome = StringProperty('')
    dificuldade = StringProperty('')
    jogadas = NumericProperty(0)
    tempo_formatado = StringProperty('00:00')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tempo_segundos = 0
        self.primeira_carta = None
        self.segunda_carta = None
        self.pares_encontrados = 0
        self.total_pares = 8
        self.cronometro_evento = None

    def iniciar_partida(self, nome, dificuldade):
        self.jogador_nome = nome
        self.dificuldade = dificuldade
        self.jogadas = 0
        self.tempo_segundos = 0
        self.tempo_formatado = '00:00'
        self.primeira_carta = None
        self.segunda_carta = None
        self.pares_encontrados = 0
        
        # Limpa o tabuleiro anterior
        tabuleiro = self.ids.grid_tabuleiro
        tabuleiro.clear_widgets()

        # Configura o layout conforme a dificuldade
        if dificuldade == 'facil':
            self.total_pares = 8
            tabuleiro.cols = 4
            imagens_selecionadas = random.sample(POOL_IMAGENS, 8)
        else:
            self.total_pares = 18
            tabuleiro.cols = 6
            imagens_selecionadas = POOL_IMAGENS.copy()

        # Duplica e embaralha as cartas
        cartas_lista = imagens_selecionadas * 2
        random.shuffle(cartas_lista)

        # Adiciona os botões das cartas ao grid
        for idx, img_path in enumerate(cartas_lista):
            btn = CardButton(
                card_image=img_path,
                card_value=img_path,  # O caminho serve como identificador único para combinação
                card_index=idx
            )
            btn.bind(on_press=self.on_card_clicked)
            tabuleiro.add_widget(btn)

        # Cancela cronômetro anterior se estiver rodando
        if self.cronometro_evento:
            Clock.unschedule(self.cronometro_evento)

        # Inicia o cronômetro (atualiza a cada 1 segundo)
        self.cronometro_evento = Clock.schedule_interval(self.atualizar_tempo, 1.0)

    def atualizar_tempo(self, dt):
        self.tempo_segundos += 1
        minutos = self.tempo_segundos // 60
        segundos = self.tempo_segundos % 60
        self.tempo_formatado = f"{minutos:02d}:{segundos:02d}"

    def on_card_clicked(self, card_button):
        # Ignora se a carta já estiver revelada, combinada ou se já houver duas cartas em processo de validação
        if card_button.is_revealed or card_button.is_matched or (self.primeira_carta and self.segunda_carta):
            return

        # Revela a carta
        card_button.is_revealed = True

        if not self.primeira_carta:
            self.primeira_carta = card_button
        else:
            self.segunda_carta = card_button
            self.jogadas += 1
            self.verificar_combinacao()

    def verificar_combinacao(self):
        if self.primeira_carta.card_value == self.segunda_carta.card_value:
            # Encontrou um par compatível
            self.primeira_carta.is_matched = True
            self.segunda_carta.is_matched = True
            self.primeira_carta = None
            self.segunda_carta = None
            self.pares_encontrados += 1

            # Verifica condição de vitória
            if self.pares_encontrados == self.total_pares:
                self.finalizar_jogo()
        else:
            # Cartas não coincidem, vira de volta após um pequeno delay de 0.8s
            Clock.schedule_once(self.esconder_cartas, 0.8)

    def esconder_cartas(self, dt):
        if self.primeira_carta and self.segunda_carta:
            self.primeira_carta.is_revealed = False
            self.segunda_carta.is_revealed = False
            self.primeira_carta = None
            self.segunda_carta = None

    def finalizar_jogo(self):
        # Para o cronômetro
        if self.cronometro_evento:
            Clock.unschedule(self.cronometro_evento)
            self.cronometro_evento = None

        # Salva o resultado no banco SQLite local
        database.adicionar_pontuacao(
            self.jogador_nome, 
            self.dificuldade, 
            self.jogadas, 
            self.tempo_segundos
        )

        # Exibe o popup de vitória
        popup = VictoryPopup(self, self.jogadas, self.tempo_formatado)
        popup.open()

    def reiniciar_jogo(self):
        self.iniciar_partida(self.jogador_nome, self.dificuldade)

    def voltar_menu(self):
        if self.cronometro_evento:
            Clock.unschedule(self.cronometro_evento)
            self.cronometro_evento = None
        self.manager.current = 'start'

    def on_leave(self):
        # Prevenção contra vazamento de cronômetro ao mudar de tela
        if self.cronometro_evento:
            Clock.unschedule(self.cronometro_evento)
            self.cronometro_evento = None


class LeaderboardItem(BoxLayout):
    """
    Componente visual que representa uma linha de registro na tabela de classificação.
    Contém propriedades reativas StringProperty.
    """
    posicao = StringProperty('1')
    nome = StringProperty('Jogador')
    jogadas = StringProperty('0')
    tempo = StringProperty('00:00')


class LeaderboardScreen(Screen):
    """
    Tela de exibição do placar de líderes (leaderboard) local.
    """
    def on_pre_enter(self):
        # Ao entrar na tela, carrega o placar na dificuldade "Fácil" por padrão
        self.ids.tab_easy.state = 'down'
        self.ids.tab_hard.state = 'normal'
        self.carregar_placar('facil')

    def carregar_placar(self, dificuldade):
        lista = self.ids.lista_pontuacoes
        lista.clear_widgets()

        # Busca dados do SQLite
        melhores = database.obter_melhores_pontuacoes(dificuldade, limite=10)

        if not melhores:
            # Exibe uma mensagem se não houver pontuações gravadas
            from kivy.uix.label import Label
            from kivy.metrics import dp
            mensagem = Label(
                text='Nenhuma pontuação registrada ainda!',
                color=[0.804, 0.839, 0.957, 0.6],
                font_size='16sp',
                size_hint_y=None,
                height=dp(100)
            )
            lista.add_widget(mensagem)
        else:
            # Preenche a lista com os melhores jogadores
            for idx, item in enumerate(melhores):
                jogador, jogadas, tempo_segundos, _ = item
                
                # Formata tempo de segundos para MM:SS
                minutos = tempo_segundos // 60
                segundos = tempo_segundos % 60
                tempo_str = f"{minutos:02d}:{segundos:02d}"

                row = LeaderboardItem(
                    posicao=f"#{idx + 1}",
                    nome=jogador,
                    jogadas=str(jogadas),
                    tempo=tempo_str
                )
                lista.add_widget(row)

    def voltar_menu(self):
        self.manager.current = 'start'


class MemoryGameApp(App):
    """
    Classe principal da aplicação Kivy.
    """
    def build(self):
        # Inicializa o banco de dados e cria a tabela se não existir
        database.inicializar_banco()

        # Configura o ScreenManager e registra as telas
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(LeaderboardScreen(name='leaderboard'))
        
        return sm


if __name__ == '__main__':
    # Executa o aplicativo
    MemoryGameApp().run()
