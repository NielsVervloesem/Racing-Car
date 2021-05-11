import pygame
import neat
from car import Car
from randomRacetrack import RandomRacetrack

#Training loop
def run(genomes, config):
    #Generate racetrack
    racetrack = RandomRacetrack(screen_width, screen_height, 15)

    #Init cars + networks
    networks = []
    cars = []
    car_x = int(racetrack.start[0])
    car_y = int(racetrack.start[1])

    for id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        car = Car(car_x, car_y)
        cars.append(car)

    global current_generation
    current_generation = current_generation + 1

    #Game params
    lock_screen = 0
    is_panning = False
    pan_start_pos = (0,0)
    zoom = 1
    loop = True
    ticks = 40

    screen_x = 0
    screen_y = 0
    world_offset_x = 0
    world_offset_y = 0

    #Game Loop
    run = True
    while run:
        pygame.display.set_caption('Murphy simulator (%d FPS)' % (clock.get_fps()))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        #User input for pan/zoom/exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                #Hit enter to avoid panning and zooming
                if event.key == pygame.K_RETURN:
                    if lock_screen == 0:
                        lock_screen = 1
                    elif lock_screen == 1:
                        lock_screen = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                '''
                if event.button == 4 or event.button == 5:
                    # X and Y before the zoom
                    mouseworld_x_before, mouseworld_y_before = screen_2_world(mouse_x, mouse_y)

                    # ZOOM IN/OUT
                    if event.button == 4:
                        game_state.zoom *= scale_up
                    elif event.button == 5:
                        game_state.zoom *= scale_down

                    # X and Y after the zoom
                    mouseworld_x_after, mouseworld_y_after = screen_2_world(mouse_x, mouse_y)

                    # Do the difference between before and after, and add it to the offset
                    game_state.world_offset_x += mouseworld_x_before - mouseworld_x_after
                    game_state.world_offset_y += mouseworld_y_before - mouseworld_y_after
                '''
                #Click and drag left mouse button to start panning
                if event.button == 1:
                    is_panning = True
                    pan_start_pos = mouse_x, mouse_y

            #Stop panning when left mouse button is released
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and is_panning:
                    is_panning = False

        if is_panning:
            world_offset_x -= (mouse_x - pan_start_pos[0])
            world_offset_y -= (mouse_y - pan_start_pos[1]) 
            pan_start_pos = mouse_x, mouse_y

        #Draw racetrack        
        for line in racetrack.innerHitLine:
            pygame.draw.lines(screen, (255,0,0), False, line,2)

        for line in racetrack.outerHitLine:
            for l in line:
                l = (l[0] + world_offset_x, l[1] + world_offset_y)
            pygame.draw.lines(screen, (255,0,0), False, line,2)

        #Draw checkpoints
        colorOffset = 0
        for i in range(0,len(racetrack.checkpoints),2):
            p1 = (int(racetrack.checkpoints[i][0]),int(racetrack.checkpoints[i][1]))
            p2 = (int(racetrack.checkpoints[i+1][0]),int(racetrack.checkpoints[i+1][1]))
            pygame.draw.line(screen, (0, 255 - colorOffset,0+colorOffset), p1, p2, 1)    
            colorOffset = colorOffset + 5
        
        #loop tru cars and predict output
        for index, car in enumerate(cars):
            if(car.is_alive):
                #180, -90, -40, -15, 0, 15, 40, 90
                sensors = car.radar.calculate_distance(racetrack) 
                output = networks[index].activate(sensors)


        pygame.display.update()
        screen.fill(background_colour)
        clock.tick(ticks)


#Pygame init params
(screen_width, screen_height) = (750, 750)
background_colour = (0,0,0)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
ticks = 40

#NEAT PARAMS
generations = 200
model_name = "model"
config_path = "./config-feedforward.txt"

#NEAT init
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
population = neat.Population(config)
population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)
population.add_reporter(neat.Checkpointer(5, 3600, "/" + model_name + "/checkpoint"))

global current_generation
current_generation = 0 

model = population.run(run, generations)

with open("/" + model_name + "/" + model_name + ".pkl", "wb") as f:
    pickle.dump(model, f)
    f.close()


