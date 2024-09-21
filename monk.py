import pygame
import random
import os

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Monkey Math Game')

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OLIVE_GREEN = (107, 142, 35)  # Verde oliva para o fundo da plaquinha

# Fonte
font = pygame.font.Font(None, 36)

# Carregando imagens
background_img = pygame.image.load('background.png')  # Cenário do jogo principal
menu_background_img = pygame.image.load('menu_background.png')  # Background do menu inicial
game_over_background_img = pygame.image.load('score_background.png')  # Background do game over
score_background_img = pygame.image.load('score_background.png')  # Background do score
monkey_idle = pygame.image.load('monkey_idle.png')  # Macaco normal
monkey_blink = pygame.image.load('monkey_blink.png')  # Macaco piscando
basket_img = pygame.image.load('basket.png')  # Cesta de bananas
banana_img = pygame.image.load('banana.png')  # Imagem da banana

# Carregando efeitos sonoros
correct_sound = pygame.mixer.Sound('correct.wav')
wrong_sound = pygame.mixer.Sound('wrong.ogg')
pygame.mixer.music.load('background_music.wav')
pygame.mixer.music.play(-1)  # Música de fundo em loop

# Variáveis do jogo
bananas = 0
max_bananas = 0
question = ""
correct_answer = 0
user_answer = ""
game_active = False
monkey_frame = 0

# Lista de pontuações
high_scores = [0, 0, 0]  # Armazenar as 3 melhores pontuações

# Função para desenhar uma plaquinha com texto
def draw_text_plaque(text, x, y, width, height, text_color=WHITE, bg_color=OLIVE_GREEN, border_color=WHITE, border_thickness=5):
    pygame.draw.rect(screen, border_color, (x - border_thickness, y - border_thickness, width + 2 * border_thickness, height + 2 * border_thickness))
    pygame.draw.rect(screen, bg_color, (x, y, width, height))
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(rendered_text, text_rect)

# Função para criar uma nova questão
def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        return f"{num1} + {num2}", num1 + num2
    elif operation == '-':
        return f"{num1} - {num2}", num1 - num2
    elif operation == '*':
        return f"{num1} * {num2}", num1 * num2
    else:
        num1 *= num2
        return f"{num1} / {num2}", num1 // num2

# Função para desenhar as bananas na cesta
# Função para desenhar as bananas na cesta em pilhas de 6
def draw_bananas():
    global bananas
    # Tamanho máximo de bananas por coluna
    max_bananas_per_column = 20
    # Largura entre as colunas de bananas
    column_spacing = 30
    # Altura entre as bananas em uma mesma coluna
    row_spacing = 15

    for i in range(bananas):
        # Calcular a coluna atual e a linha dentro da coluna
        column = i // max_bananas_per_column
        row = i % max_bananas_per_column

        # Calcular a posição X e Y da banana
        x_position = 210 + column * column_spacing
        y_position = 430 - row * row_spacing

        # Desenhar a banana na posição calculada
        screen.blit(banana_img, (x_position, y_position))


# Função principal do jogo
def game_loop():
    global bananas, max_bananas, question, correct_answer, user_answer, game_active, monkey_frame
    
    running = True
    clock = pygame.time.Clock()

    # Tela de menu
    def menu():
        while True:
            screen.blit(menu_background_img, (0, 0))  # Adiciona o fundo do menu
            
            draw_text_plaque('Monkey Math Game', screen_width // 2 - 150, 100, 300, 50)
            draw_text_plaque('1. New Game', screen_width // 2 - 100, 200, 200, 50)
            draw_text_plaque('2. High Scores', screen_width // 2 - 100, 250, 200, 50)
            draw_text_plaque('Press number to option', screen_width // 2 - 150, 350, 300, 50)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        start_game()
                        return  # Sai do menu e inicia o jogo
                    if event.key == pygame.K_2:
                        show_high_scores()

    # Função para iniciar o jogo
    def start_game():
        global bananas, max_bananas, question, correct_answer, user_answer, game_active
        bananas = 0
        max_bananas = 0
        question, correct_answer = generate_question()
        user_answer = ""
        game_active = True
        game_main_loop()

    # Função para exibir os placares
    def show_high_scores():
        while True:
            screen.blit(score_background_img, (0, 0))  # Fundo do menu de placares
            draw_text_plaque('High Scores', screen_width // 2 - 100, 100, 200, 50)
            for i, score in enumerate(high_scores):
                draw_text_plaque(f'{i+1}. {score}', screen_width // 2 - 100, 160 + i * 50, 200, 50)
            draw_text_plaque('Press ESC to back', screen_width // 2 - 150, 400, 300, 50)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

    # Tela de Game Over
    def game_over_screen():
        global max_bananas
        check_high_score(max_bananas)
        while True:
            screen.blit(game_over_background_img, (0, 0))  # Fundo da tela de game over
            draw_text_plaque('Game Over!', screen_width // 2 - 100, 100, 200, 50)
            draw_text_plaque(f'Your Score: {max_bananas}', screen_width // 2 - 100, 200, 200, 50)
            draw_text_plaque('Press ENTER to menu', screen_width // 2 - 150, 300, 300, 50)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu()

    # Função para verificar e atualizar as pontuações
    def check_high_score(score):
        global high_scores
        # Adiciona o score à lista e mantém os três maiores
        high_scores.append(score)
        high_scores = sorted(high_scores, reverse=True)[:3]

    # Loop principal do jogo
    def game_main_loop():
        global bananas, max_bananas, question, correct_answer, user_answer, monkey_frame, game_active
        
        while game_active:
            screen.blit(background_img, (0, 0))  # Cenário de fundo
            
            # Captura de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Verificar resposta e aceitar números negativos
                        if (user_answer.lstrip('-').isdigit() or (user_answer == '-')) and int(user_answer) == correct_answer:
                            correct_sound.play()  # Som de acerto
                            bananas += 1  # Adiciona uma banana
                            max_bananas = max(max_bananas, bananas)
                            question, correct_answer = generate_question()
                            user_answer = ""
                        else:
                            wrong_sound.play()  # Som de erro
                            if bananas > 0:
                                bananas = 0  # Se errar e ainda tiver bananas, zera as bananas
                            else:
                                game_active = False  # Se errar e já tiver zero bananas, vai para game over
                                game_over_screen()

                    elif event.key == pygame.K_BACKSPACE:
                        user_answer = user_answer[:-1]
                    elif event.unicode == '-' and len(user_answer) == 0:
                        user_answer += event.unicode  # Permitir o sinal de menos apenas no início
                    elif event.unicode.isdigit():
                        user_answer += event.unicode  # Apenas números

            # Animação do macaco piscando
            monkey_frame += 1
            if monkey_frame // 60 % 2 == 0:
                screen.blit(monkey_idle, (100, 200))
            else:
                screen.blit(monkey_blink, (100, 200))
            
            # Cesta de bananas e texto
            screen.blit(basket_img, (200, 400))
            draw_bananas()  # Desenha as bananas na cesta com base no número de bananas
            draw_text_plaque(f'Question: {question}', screen_width // 2 - 100, 50, 300, 50)
            draw_text_plaque(f'Your answer: {user_answer}', screen_width // 2 - 100, 100, 300, 50)
            draw_text_plaque(f'Bananas: {bananas}', screen_width // 2 - 100, 150, 300, 50)
            
            pygame.display.flip()
            clock.tick(60)

    menu()  # Chama o menu inicial

game_loop()
