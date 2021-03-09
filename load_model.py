import pickle
import neat

model_path = '09032021-101354.pkl'
config_file = '..\config-feedforward.txt'

# Unpickle saved winner
with open(model_path, "rb") as f:
    winner = pickle.load(f)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

winner_model = neat.nn.FeedForwardNetwork.create(winner, config)

input = [5,1,2,3,4,6]
output = winner_model.activate(input)

print(output)