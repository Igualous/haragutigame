import pygame
import sys
import random

# --- Configurações Iniciais ---
pygame.init()

# Cores Fofinhas
COR_GRAMA = (124, 252, 0)
COR_GRAMA_ESCURA = (50, 205, 50)
COR_SOL = (255, 223, 0)
COR_UI = (100, 149, 237)
COR_TEXTO = (255, 255, 255)
COR_ZUMBI = (75, 0, 130) # Mudei para Roxo Índigo para destacar mais na grama!
COR_PEASHOOTER = (0, 255, 127)
COR_SUNFLOWER = (255, 215, 0)
COR_JOGADOR = (255, 105, 180)
COR_TIRO = (144, 238, 144)

# Dimensões
LARGURA_TELA = 800
ALTURA_TELA = 600
TAM_GRID = 80
LINHAS = 5
COLUNAS = 9
OFFSET_X = 40
OFFSET_Y = 100

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jardim da Dudinha vs Zumbis (Correção) 🌻🧟")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 20, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 50, bold=True)

# --- Classes do Jogo ---

class Projetil:
    def __init__(self, x, y, linha):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.linha = linha
        self.velocidade = 7
        self.dano = 25

    def update(self):
        self.rect.x += self.velocidade

    def draw(self, superficie):
        pygame.draw.circle(superficie, COR_TIRO, self.rect.center, 8)

class Planta:
    def __init__(self, x, y, linha, tipo):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.linha = linha
        self.tipo = tipo # 1 = Girassol, 2 = Disparervilha
        self.vida = 100
        self.timer_acao = pygame.time.get_ticks()
        
        if self.tipo == 1: # Girassol
            self.custo = 50
            self.cor = COR_SUNFLOWER
            self.intervalo = 7000 
        else: # Disparervilha
            self.custo = 100
            self.cor = COR_PEASHOOTER
            self.intervalo = 1200

    def update(self, jogo):
        agora = pygame.time.get_ticks()
        
        if self.tipo == 1: 
            if agora - self.timer_acao > self.intervalo:
                jogo.sois.append(Sol(self.rect.centerx, self.rect.centery, destino_fixo=True))
                self.timer_acao = agora
        
        elif self.tipo == 2:
            zumbi_na_linha = False
            for zumbi in jogo.zumbis:
                if zumbi.linha == self.linha and zumbi.rect.x > self.rect.x:
                    zumbi_na_linha = True
                    break
            
            if zumbi_na_linha and agora - self.timer_acao > self.intervalo:
                jogo.projeteis.append(Projetil(self.rect.centerx, self.rect.centery, self.linha))
                self.timer_acao = agora

    def draw(self, superficie):
        cor_base = self.cor
        pygame.draw.rect(superficie, cor_base, self.rect, border_radius=10)
        if self.tipo == 1:
            pygame.draw.circle(superficie, (255, 140, 0), self.rect.center, 15)
        else:
            pygame.draw.circle(superficie, (0, 100, 0), (self.rect.right, self.rect.centery - 10), 10)
            
        razao_vida = self.vida / 100
        pygame.draw.rect(superficie, (255, 0, 0), (self.rect.x, self.rect.y - 10, 60, 5))
        pygame.draw.rect(superficie, (0, 255, 0), (self.rect.x, self.rect.y - 10, 60 * razao_vida, 5))

class Zumbi:
    def __init__(self, linha):
        self.linha = linha
        # Começa logo na borda para aparecer rápido
        x_pos = LARGURA_TELA + random.randint(10, 50) 
        y_pos = OFFSET_Y + (linha * TAM_GRID) + 10
        self.rect = pygame.Rect(x_pos, y_pos, 60, 60)
        
        # CORREÇÃO IMPORTANTE: Usar float para posição exata
        self.pos_x = float(x_pos) 
        self.velocidade = 0.4 # Um pouquinho mais rápido
        
        self.vida = 100
        self.dano = 0.5
        self.comendo = False
        self.planta_alvo = None

    def update(self, jogo):
        if self.vida <= 0:
            if self in jogo.zumbis:
                jogo.zumbis.remove(self)
                jogo.pontuacao += 1
            return

        self.comendo = False
        self.planta_alvo = None
        
        for planta in jogo.plantas:
            if planta.linha == self.linha and self.rect.colliderect(planta.rect):
                self.comendo = True
                self.planta_alvo = planta
                break
        
        if self.comendo:
            if self.planta_alvo:
                self.planta_alvo.vida -= self.dano
                if self.planta_alvo.vida <= 0:
                    if self.planta_alvo in jogo.plantas:
                        jogo.plantas.remove(self.planta_alvo)
                    self.comendo = False
        else:
            # Move usando float e atualiza o rect int
            self.pos_x -= self.velocidade
            self.rect.x = int(self.pos_x)

        if self.rect.right < 0:
            jogo.game_over = True

    def draw(self, superficie):
        pygame.draw.rect(superficie, COR_ZUMBI, self.rect, border_radius=5)
        # Olhos
        pygame.draw.circle(superficie, (255, 50, 50), (self.rect.x + 15, self.rect.y + 20), 5)
        pygame.draw.circle(superficie, (255, 50, 50), (self.rect.x + 45, self.rect.y + 20), 5)
        # Boca
        pygame.draw.rect(superficie, (0,0,0), (self.rect.x + 20, self.rect.y + 40, 20, 5))

class Sol:
    def __init__(self, x, y, destino_fixo=False):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.destino_y = y if destino_fixo else random.randint(OFFSET_Y, ALTURA_TELA - 50)
        self.valor = 25
        self.tempo_vida = pygame.time.get_ticks()
        if not destino_fixo:
            self.rect.y = -50

    def update(self):
        if self.rect.y < self.destino_y:
            self.rect.y += 3 # Sóis caem mais rápido
        
        if pygame.time.get_ticks() - self.tempo_vida > 8000:
            return False
        return True

    def draw(self, superficie):
        pygame.draw.circle(superficie, COR_SOL, self.rect.center, 20)
        pygame.draw.circle(superficie, (255, 255, 200), self.rect.center, 10)

class Jogador:
    def __init__(self):
        self.rect = pygame.Rect(LARGURA_TELA//2, ALTURA_TELA//2, 40, 40)
        self.velocidade = 5
        self.planta_selecionada = 1

    def mover(self, teclas):
        if teclas[pygame.K_w] or teclas[pygame.K_UP]: self.rect.y -= self.velocidade
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]: self.rect.y += self.velocidade
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]: self.rect.x -= self.velocidade
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]: self.rect.x += self.velocidade
        self.rect.clamp_ip(tela.get_rect())

    def coletar_sois(self, sois, jogo):
        for sol in sois[:]:
            if self.rect.colliderect(sol.rect):
                jogo.recursos += sol.valor
                sois.remove(sol)

    def plantar(self, jogo):
        col = (self.rect.centerx - OFFSET_X) // TAM_GRID
        lin = (self.rect.centery - OFFSET_Y) // TAM_GRID

        if 0 <= col < COLUNAS and 0 <= lin < LINHAS:
            x = OFFSET_X + col * TAM_GRID + 10
            y = OFFSET_Y + lin * TAM_GRID + 10
            
            ocupado = False
            for p in jogo.plantas:
                if p.rect.collidepoint(x + 30, y + 30):
                    ocupado = True
                    break
            
            custo = 50 if self.planta_selecionada == 1 else 100
            
            if not ocupado and jogo.recursos >= custo:
                jogo.recursos -= custo
                nova_planta = Planta(x, y, lin, self.planta_selecionada)
                jogo.plantas.append(nova_planta)

    def draw(self, superficie):
        pygame.draw.circle(superficie, COR_JOGADOR, self.rect.center, 20)
        pygame.draw.rect(superficie, (255, 255, 255), (self.rect.x+10, self.rect.y+5, 20, 10))

# --- Gerenciador do Jogo ---

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.plantas = []
        self.zumbis = []
        self.projeteis = []
        self.sois = []
        self.jogador = Jogador()
        self.recursos = 150
        self.pontuacao = 0
        self.game_over = False
        self.vitoria = False
        self.spawn_timer = 150 # Começa alto para o 1º zumbi aparecer logo!
        self.sol_timer = 0
        self.objetivo_vitoria = 20 #zumbis mortos para vencer 

    def run(self):
        while True:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.game_over or self.vitoria:
                        if event.key == pygame.K_r:
                            self.reset()
                    else:
                        if event.key == pygame.K_e:
                            self.jogador.plantar(self)
                        if event.key == pygame.K_1:
                            self.jogador.planta_selecionada = 1
                        if event.key == pygame.K_2:
                            self.jogador.planta_selecionada = 2

            # Lógica
            if not self.game_over and not self.vitoria:
                teclas = pygame.key.get_pressed()
                self.jogador.mover(teclas)
                self.jogador.coletar_sois(self.sois, self)

                # Gerar Sol
                self.sol_timer += 1
                if self.sol_timer > 300:
                    x_sol = random.randint(OFFSET_X, LARGURA_TELA - 50)
                    self.sois.append(Sol(x_sol, -50))
                    self.sol_timer = 0

                # Gerar Zumbis
                self.spawn_timer += 1
                if self.spawn_timer > 400: 
                    linha_zumbi = random.randint(0, LINHAS - 1)
                    self.zumbis.append(Zumbi(linha_zumbi))
                    self.spawn_timer = 0

                # Updates (Usando [:] para cópia segura em listas)
                for p in self.plantas[:]: p.update(self)
                for z in self.zumbis[:]: z.update(self)
                for pr in self.projeteis[:]: pr.update()
                
                self.sois = [s for s in self.sois if s.update()]

                # Colisão Projétil vs Zumbi
                for pr in self.projeteis[:]:
                    bateu = False
                    if pr.rect.x > LARGURA_TELA:
                        if pr in self.projeteis: self.projeteis.remove(pr)
                        continue
                    
                    for z in self.zumbis:
                        if z.linha == pr.linha and pr.rect.colliderect(z.rect):
                            z.vida -= pr.dano
                            bateu = True
                            break
                    if bateu:
                        if pr in self.projeteis: self.projeteis.remove(pr)

                if self.pontuacao >= self.objetivo_vitoria:
                    self.vitoria = True

            # Desenho
            tela.fill((34, 139, 34)) 

            # Grid
            pygame.draw.rect(tela, (139, 69, 19), (OFFSET_X - 10, OFFSET_Y - 10, COLUNAS * TAM_GRID + 20, LINHAS * TAM_GRID + 20))
            for col in range(COLUNAS):
                for lin in range(LINHAS):
                    cor = COR_GRAMA if (col + lin) % 2 == 0 else COR_GRAMA_ESCURA
                    rect = pygame.Rect(OFFSET_X + col * TAM_GRID, OFFSET_Y + lin * TAM_GRID, TAM_GRID, TAM_GRID)
                    pygame.draw.rect(tela, cor, rect)

            for p in self.plantas: p.draw(tela)
            for z in self.zumbis: z.draw(tela)
            for pr in self.projeteis: pr.draw(tela)
            for s in self.sois: s.draw(tela)
            
            if not self.game_over and not self.vitoria:
                self.jogador.draw(tela)

            # UI
            pygame.draw.rect(tela, COR_UI, (0, 0, LARGURA_TELA, 80))
            texto_sol = fonte.render(f"Sóis: {self.recursos} ☀️", True, COR_TEXTO)
            texto_score = fonte.render(f"Zumbis: {self.pontuacao}/{self.objetivo_vitoria} 💀", True, COR_TEXTO)
            
            nome_planta = "Girassol (50)" if self.jogador.planta_selecionada == 1 else "Ervilha (100)"
            texto_selecao = fonte.render(f"Selecionado [1/2]: {nome_planta}", True, COR_TEXTO)
            texto_controles = fonte.render("WASD: Mover | E: Plantar | R: Reiniciar", True, COR_TEXTO)

            tela.blit(texto_sol, (20, 10))
            tela.blit(texto_score, (20, 40))
            tela.blit(texto_selecao, (300, 10))
            tela.blit(texto_controles, (300, 40))

            # Telas Finais
            if self.game_over:
                sombra = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
                sombra.set_alpha(200)
                sombra.fill((0,0,0))
                tela.blit(sombra, (0,0))
                msg = fonte_grande.render("ZUMBIS NA COZINHA! 🧠", True, (255, 50, 50))
                msg2 = fonte.render("Pressione 'R' para tentar de novo, Dudinha!", True, (255, 255, 255))
                tela.blit(msg, (LARGURA_TELA//2 - msg.get_width()//2, ALTURA_TELA//2 - 50))
                tela.blit(msg2, (LARGURA_TELA//2 - msg2.get_width()//2, ALTURA_TELA//2 + 20))

            if self.vitoria:
                sombra = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
                sombra.set_alpha(200)
                sombra.fill((255, 255, 255))
                tela.blit(sombra, (0,0))
                msg = fonte_grande.render("VITÓRIA FOFINHA! 🎉", True, (0, 150, 0))
                msg2 = fonte.render("Pressione 'R' para jogar de novo.", True, (50, 50, 50))
                tela.blit(msg, (LARGURA_TELA//2 - msg.get_width()//2, ALTURA_TELA//2 - 50))
                tela.blit(msg2, (LARGURA_TELA//2 - msg2.get_width()//2, ALTURA_TELA//2 + 20))

            pygame.display.flip()
            relogio.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()