import GameEnv
import pygame
import numpy as np
from ddqn_keras import DDQNAgent
from collections import deque
import random, math
import matplotlib.pyplot as plt

TOTAL_GAMETIME = 1000  # Max game time for one episode
N_EPISODES = 10000
REPLACE_TARGET = 50

game = GameEnv.RacingEnv()
game.fps = 60

GameTime = 0
GameHistory = []
renderFlag = False

ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=5, epsilon=1.00, epsilon_end=0.10, epsilon_dec=0.9995,
                       replace_target=REPLACE_TARGET, batch_size=512, input_dims=19)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
# ddqn_agent.load_model()

ddqn_scores = []
eps_history = []
episode_rewards = []
average_rewards = []


def run():
    lane_change = None

    for e in range(N_EPISODES):
        game.reset()  # reset env

        done = False
        score = 0
        counter = 0

        observation_, reward, done = game.step(0,lane_change=lane_change)
        observation = np.array(observation_)

        gtime = 0  # set game time back to 0

        renderFlag = False  # if you want to render every episode set to true

        if e % 10 == 0 and e > 0:  # render every 10 episodes
            renderFlag = True

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lane_change = "left"
                    elif event.key == pygame.K_RIGHT:
                        lane_change = "right"
                    else:
                        lane_change = None
            
            action = ddqn_agent.choose_action(observation,lane_change=lane_change)
            observation_, reward, done = game.step(action,lane_change=lane_change)
            observation_ = np.array(observation_)

            # This is a countdown if no reward is collected the car will be done within 100 ticks
            if reward == 0:
                counter += 1
                if counter > 100:
                    done = True
            else:
                counter = 0

            score += reward

            ddqn_agent.remember(observation, action, reward, observation_, int(done))
            observation = observation_
            ddqn_agent.learn()

            gtime += 1

            if gtime >= TOTAL_GAMETIME:
                done = True

            if renderFlag:
                game.render(action)

            # Eş zamanlı olarak grafikleri güncelle
            plot_learning_curve(episode_rewards, average_rewards)

        eps_history.append(ddqn_agent.epsilon)
        ddqn_scores.append(score)
        avg_score = np.mean(ddqn_scores[max(0, e - 100):(e + 1)])

        episode_rewards.append(score)
        average_rewards.append(avg_score)

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ddqn_agent.update_network_parameters()

        if e % 10 == 0 and e > 10:
            ddqn_agent.save_model()
            print("save model")

        print('episode: ', e, 'score: %.2f' % score,
              ' average score %.2f' % avg_score,
              ' epsolon: ', ddqn_agent.epsilon,
              ' memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)
        if e % 50 == 0:
            plot_learning_curve(episode_rewards, average_rewards)

        game.render(action)
          # Oyunun FPS'ini kontrol etmek için

    pygame.quit()
    plt.show()


def plot_learning_curve(scores, avg_scores):
    x = [i + 1 for i in range(len(scores))]

    # Her bir episode için elde edilen skoru çizdirin
    plt.plot(x, scores, label='Episode Score')

    # 100 episode'ın ortalamasını çizdirin
    plt.plot(x, avg_scores, label='Average Score (100 Episodes)')

    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.title('Reinforcement Learning Performance')
    plt.legend()

    # plt.show() komutunu kaldırdık
    plt.pause(0.01)


run()
