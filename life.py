import numpy as np
import random as r
from graphics import *
import time

# Copyright (c) 2020 https://github.com/miraakx/

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

#------------------------------------------------------------------------

class Genome:

    def __init__(self, memory, moves, pop_size):
        self.memory = memory
        self.move = moves
        self.size = pop_size
        
    @staticmethod
    def init_from_size(pop_size):
        memory = np.random.randint(0, 16, (pop_size, 4, 16),  dtype=np.int8)
        move = np.random.randint(0, 4, (pop_size, 4, 16), dtype=np.int8)    
        return Genome(memory, move, pop_size)

    def get_new_memory(self, current_memory, item_in_view):
        return self.memory[np.arange(0,self.size),item_in_view,current_memory]  
    
    def get_new_orientation(self, current_memory, item_in_view):
        arr = np.array([[[1,0],[0,1]],[[0,-1],[1,0]],[[0,1],[-1,0]],[[-1,0],[0,-1]]], dtype=np.int8)[self.move[np.arange(0,self.size), item_in_view, current_memory]]
        return arr

    def _crossover(self, matrix, first_parent_index, second_parent_index):
        if((first_parent_index.size != second_parent_index.size) | (first_parent_index.size != matrix.shape[0])):
            raise Exception()
        first_parent = matrix[first_parent_index,:,:]
        second_parent = matrix[second_parent_index,:,:]
        template1 = np.random.randint(0, 2, (first_parent_index.size, 4, 16),  dtype=np.int8)
        template2 = - template1 + 1
        return first_parent * template1 + second_parent * template2

    def crossover(self, first_parent_index, second_parent_index): 
        memory = self._crossover(self.memory, first_parent_index, second_parent_index)
        move = self._crossover(self.move, first_parent_index, second_parent_index)
        return Genome(memory, move, self.size)

    
    def _mutate(self, matrix, mutation_rate, value_range):
        if(mutation_rate > 100):
            raise Exception()
        memory_size = matrix.size
        matrix = np.reshape(matrix,(memory_size,))
        num = int(memory_size/100*mutation_rate) + 1
        for _ in range(0,num):
            value = np.random.randint(value_range[0], value_range[1], dtype=np.int8)
            pos = np.random.randint(0, memory_size)
            matrix[pos] = value
        return np.reshape(matrix,(self.size,4,16))
            
    def mutate(self, mutation_rate):
        memory = self._mutate(self.memory, mutation_rate, (0, 16))
        move = self._mutate(self.move, mutation_rate, (0, 4))
        return Genome(memory, move, self.size)

class RouletteWheelSelector:
    
    def __init__(self, power = 1):
        self.power = power

    def select(self, scores):
        if 0 in scores:
            raise Exception("Zero score not allowed!")
        scores = np.power(scores, self.power)
        np_roulette = np.cumsum(scores)  
        total = np.sum(scores)
        rand = np.random.randint(1, total + 1, scores.size)
        result = np.searchsorted(np_roulette, rand)
        return result

def concatenate(x, y):
    x = np.reshape(x,(x.size,1))
    y = np.reshape(y,(y.size,1))
    return  np.concatenate([x,y], axis=-1)

class Coordinates:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def x(self):
        return self.coordinates[:,0]
    
    def y(self):
        return self.coordinates[:,1]

    def add(self, orientations, condition=None):
        if(condition is not None):
            indices = np.where(condition == True)[0]
            np.add.at(self.coordinates,(indices,slice(None)), orientations[condition])
            result = self.coordinates
        else:
            result = self.coordinates + orientations
        return Coordinates(result)

    def shift(self, value):
        return Coordinates(self.coordinates + value)

    def filter(self, bool_arr):
        return Coordinates(self.coordinates[bool_arr])

    @staticmethod
    def build(x, y):
        return Coordinates(concatenate(x, y))

class SimulationParams:

    def __init__(self, world_width, world_heigth, pop_size, food_number):
        self.world_width = world_width
        self.world_heigth = world_heigth
        self.pop_size = pop_size
        self.food_number = food_number            

class Population:

    def __init__(self, sim_params, coordinates, orientations, memory, genome, world):
        self.sim_params = sim_params
        self.coordinates = coordinates
        self.orientations = orientations
        self.memory = memory
        self.genome = genome
        self.world = world
        self.scores = np.ones((sim_params.pop_size,), dtype=int)
        self.front = None
        
    @staticmethod
    def init_from_params(sim_params, world):
        coordinates = world.generate_population_coordinate(sim_params.pop_size)
        orientations = Population._init_orientations(sim_params.pop_size)
        memory = np.random.randint(0,16,(sim_params.pop_size,), dtype=np.int8)
        genome = Genome.init_from_size(sim_params.pop_size)
        return Population(sim_params, coordinates, orientations, memory, genome, world)

    @staticmethod
    def init_from_genome(old_population, new_genome, new_world):
        sim_params = old_population.sim_params
        coordinates = new_world.generate_population_coordinate(sim_params.pop_size)
        orientations = Population._init_orientations(sim_params.pop_size)
        memory = np.random.randint(0,16,(sim_params.pop_size,), dtype=np.int8)
        return Population(sim_params, coordinates, orientations, memory, new_genome, new_world)

    @staticmethod
    def _init_orientations(size):
        #[right,up,left,down]
        M = [[1,0],[0,1],[-1,0],[0,-1]]
        x = []
        y = []
        for _ in range(size):
            n = r.randint(0,3)
            x.append(M[n][0])
            y.append(M[n][1])
        return concatenate(np.array(x, dtype=np.int8), np.array(y, dtype=np.int8))

    def eat(self):
        bool_arr = self.world.is_food(self.coordinates)
        self.scores[bool_arr] += 1
        self.world.destroy_food(self.coordinates.filter(bool_arr))

    def _watch(self):
        self.item_front = self.world.watch_front(self.coordinates, self.orientations)
      
    def move(self):
        self._watch()
        rotations = self.genome.get_new_orientation(self.memory, self.item_front)
        self.orientations = np.einsum('ijk,ij->ik',rotations,self.orientations)
        can_move = self.world.can_move(rotations, self.item_front)
        self.coordinates = self.coordinates.add(self.orientations, can_move)
        self.world._set_eaters(self.coordinates)

    def update_memory(self):
        self.memory = self.genome.get_new_memory(self.memory, self.item_front)

    def evolve_genome(self, selector, mutation_rate):
        first_parent_list = selector.select(self.scores)
        second_parent_list = selector.select(self.scores)
        new_genome = self.genome.crossover(first_parent_list, second_parent_list)
        new_genome = new_genome.mutate(mutation_rate)
        return new_genome

class World:

    def __init__(self, sim_params):
        self.sim_params = sim_params
        self._init_params(sim_params.world_width , sim_params.world_heigth, sim_params.food_number)
        self._init_env()
        self._init_food()
    
    @staticmethod
    def init_from_other_world(world):
        return World(world.sim_params)

    def _init_params(self, width, heigth, food):
        self.EMPTY = 0
        self.FOOD = 1
        self.WALL = 2
        self.EATER = 3
        self.HEIGTH = heigth
        self.WIDTH = width
        self.WORLD_SIZE =  width * heigth
        self.FOOD_NUMBER = food  

    def _init_env(self):
        self.env =  np.full((self.WIDTH + 2, self.HEIGTH + 2), self.WALL, dtype=np.int8)

    def _init_food(self):
        arr = np.zeros(self.WORLD_SIZE, dtype=np.int8)
        arr[:self.FOOD_NUMBER] = self.FOOD
        np.random.shuffle(arr)
        self.env[1:-1,1:-1] = arr.reshape((self.WIDTH,self.HEIGTH))

    def _set_eaters(self, coordinates):
        c = coordinates.shift(1)
        self.eaters = np.full((self.WIDTH + 2, self.HEIGTH + 2), self.EMPTY, dtype=np.int8)
        self.eaters[c.x(), c.y()] = self.EATER

    # Return a tuple (x,y) where x and y are two numpy array with the x and y coordinates.
    def generate_population_coordinate(self, pop_size):
        arr = np.full(self.WORLD_SIZE, False, dtype=bool)
        arr[:pop_size] = True
        np.random.shuffle(arr)
        arr = arr.reshape((self.WIDTH,self.HEIGTH))
        tup_coord = np.where(arr == True)
        coordinates = Coordinates.build(tup_coord[0], tup_coord[1])
        self._set_eaters(coordinates)
        return coordinates

    def is_food(self, coordinates):
        c = coordinates.shift(1)
        return self.env[c.x(),c.y()] == self.FOOD

    def can_move(self, rotations, item_front):
        return (rotations == np.array([[1,0],[0,1]], dtype=np.int8)).all(axis=(1,2)) & (item_front != self.EATER) & (item_front != self.WALL)

    def watch_front(self, coordinates, orientations):
        c_w = coordinates.add(orientations).shift(1)
        return self.env[c_w.x(),c_w.y()] + self.eaters[c_w.x(),c_w.y()]
    
    def destroy_food(self, coordinates):
        c = coordinates.shift(1)
        self.env[c.x(),c.y()] = self.EMPTY

    def respawn_food(self):
        food_to_respawn = int(self.FOOD_NUMBER - self.env[self.env == self.FOOD].sum())
        empty_coords = np.where(self.env == self.EMPTY)
        rand_coords_indexes = np.random.randint(0, empty_coords[0].size, food_to_respawn)
        choosen_coords = (empty_coords[0][rand_coords_indexes], empty_coords[1][rand_coords_indexes])
        self.env[choosen_coords[0],choosen_coords[1]] = self.FOOD
    
    def get_food_coordinates(self):
        coords_tuple = np.where(self.env == self.FOOD)
        return Coordinates.build(coords_tuple[0], coords_tuple[1]).shift(-1)

class GCoords:

    def __init__(self, coord, orien = None):
        self.CELL_PIXEL_SIZE = 5
        self.coord = coord * self.CELL_PIXEL_SIZE
        if orien is not None:
            self.orientation = orien * self.CELL_PIXEL_SIZE
    
class GEater:
    def __init__(self, pos):
        self.BODY_SIZE = 5
        self.HEAD_SIZE = 2
       
        body_coord = pos.coord
        self.body = Circle(Point(body_coord[0], body_coord[1]), self.BODY_SIZE)
      
        head_coord = body_coord + pos.orientation
        self.head = Circle(Point(head_coord[0], head_coord[1]), self.HEAD_SIZE)
        self.head.setFill(color_rgb(130, 0, 130))
      
        self.body_coord_old = body_coord
        self.head_coord_old = head_coord

        self.is_updated = False

    def update(self, pos):
        body_coord = pos.coord
        delta_body_coord = body_coord - self.body_coord_old
        self.body.move(delta_body_coord[0], delta_body_coord[1])

        head_coord = (body_coord + pos.orientation)
        delta_head_coord = head_coord - self.head_coord_old
        self.head.move(delta_head_coord[0], delta_head_coord[1])

        self.body_coord_old = body_coord
        self.head_coord_old = head_coord

        self.is_updated = True

    def draw(self, graphWinObj):
        if not self.is_updated:
            self.body.draw(graphWinObj)
            self.head.draw(graphWinObj)
    
    def undraw(self):
        self.body.undraw()
        self.head.undraw()

class GFood:
    def __init__(self, pos):
        self.SIZE = 3
        self._build(pos)
    
    def _build(self, pos):
        self.food = Circle(Point(pos.coord[0], pos.coord[1]), self.SIZE)     
        self.food.setFill(color_rgb(20, 50, 60))   

    def update(self, pos):
        self.food.undraw()
        self._build(pos)

    def draw(self, graphWinObj):
        self.food.draw(graphWinObj)
    
    def undraw(self):
        self.food.undraw()

class GList:

    def __init__(self, item_type, g_coord_list):
        self.g_list = list()
        for g_coord in g_coord_list:
            self.g_list.append(GItemFactory.build(item_type, g_coord))
   
    def append(self, item):
        self.g_list.append(item)

    def update(self, g_coord_list):
        for item, g_coord in zip(self.g_list, g_coord_list):
            item.update(g_coord)

    def draw(self, graphWin):
        for item in self.g_list:
            item.draw(graphWin)
    
    def undraw(self):
        for item in self.g_list:
            item.undraw()

class GItemFactory:

    FOOD_KEY = "food"
    EATER_KEY = "eater"

    _ITEMS_MAP = {
            FOOD_KEY: lambda pos: GFood(pos),
            EATER_KEY: lambda pos: GEater(pos)
        }
    
    _ITEMS_KEYS = _ITEMS_MAP.keys()

    @staticmethod
    def build(item_type, gcoord):
        lamda_fn = GItemFactory._ITEMS_MAP.get(item_type, lambda: "Error")
        return lamda_fn(gcoord)

    @staticmethod
    def items():
        return GItemFactory._ITEMS_KEYS

class Graphic:

    def __init__(self, width, heigth):
        self.CELL_PIXEL_SIZE = 5
        self.START = True
        self.win = GraphWin("Life", width*self.CELL_PIXEL_SIZE, heigth*self.CELL_PIXEL_SIZE, autoflush=False)
        self.is_initialized = False
        
    def _init_lists(self, np_coords_map):
        if self.is_initialized == True:
            raise Exception("Already initialized! Call reset() before this method.")
        self.items = {}
        for item_type in GItemFactory.items():
            np_coords_tuple = np_coords_map.get(item_type)
            g_list = GList(item_type, self.build_g_coord_list(np_coords_tuple))
            g_list.draw(self.win)
            self.items[item_type] = g_list
        self.win.update()
        self.is_initialized = True
    
    def _update_lists(self, np_coords_map):
        if self.is_initialized == False:
            raise Exception("Missing initialization!")
        for item_type in GItemFactory.items():
            np_coords_tuple = np_coords_map.get(item_type)
            g_coord_list = self.build_g_coord_list(np_coords_tuple)
            self.items[item_type].update(g_coord_list)
            self.items[item_type].draw(self.win)
        self.win.update()

    def draw(self, np_coords_map):
        if self.is_initialized:
            self._update_lists(np_coords_map)
        else:
            self._init_lists(np_coords_map)
    
    def reset(self):
        if self.is_initialized == False:
            raise Exception("Missing initialization!")
        for item_type in GItemFactory.items():
            self.items[item_type].undraw()
        self.is_initialized = False

    def close(self):
        self.win.close()

    def build_g_coord_list(self, np_coord_tuple):
        g_coord_list = list()
        if np_coord_tuple[1] is None:
            for row_coords in np_coord_tuple[0]:
                item = GCoords(row_coords)
                g_coord_list.append(item)
        else:
            for row_coords, row_orien in zip(*np_coord_tuple):
                item = GCoords(row_coords, row_orien)
                g_coord_list.append(item)
        return g_coord_list


class Game:
    def __init__(self, world, population):
        self.w = world
        self.p = population
        
    @staticmethod
    def build(sim_params):
        w = World(sim_params)
        p = Population.init_from_params(sim_params, w)
        return Game(w, p)

    def do_step(self):
        self.p.eat()
        self.p.move()
        self.p.update_memory()
        self.w.respawn_food()

    def play(self, step):
        for _ in range(step):
            self.do_step()
    
    def get_coordinates(self):
        return {
            GItemFactory.EATER_KEY: (self.p.coordinates.coordinates, self.p.orientations),
            GItemFactory.FOOD_KEY: (self.w.get_food_coordinates().coordinates, None)
        }
    
    def reset(self, world, population):
        self.w = world
        self.p = population

class GraphicGame(Game):

    def __init__(self, sim_params, world, population, fps):
        super().__init__(world, population)
        self.sleep_time = 1.0/fps
        self.graphic = Graphic(sim_params.world_width, sim_params.world_heigth)
    
    @staticmethod
    def build(sim_params, fps):
        world = World(sim_params)
        population = Population.init_from_params(sim_params, world)
        return GraphicGame(sim_params, world, population, fps)

    def play(self, step):
        for _ in range(step):
            super().do_step()
            time.sleep(self.sleep_time)
            self.graphic.draw(super().get_coordinates())
    
    def reset(self, world, population):
        super().reset(world, population)
        self.graphic.reset()

    def exit(self):
        self.graphic.close()

class GeneticAlgorithm:

    def __init__(self, sim_params, selector, mutation_rate):
        self.sim_params = sim_params
        self.world = World(sim_params)
        self.population = Population.init_from_params(sim_params, self.world)
        self.game = self._get_game(self.world, self.population)
        self.selector = selector
        self.mutation_rate = mutation_rate

    def play(self, generations, step):
        for _ in range(generations):
            self.game.play(step)
            print(np.mean(self.population.scores))
            self.evolve()
            
    def evolve(self):           
        new_genome = self.population.evolve_genome(self.selector, self.mutation_rate)
        self.world = World.init_from_other_world(self.world)
        self.population = Population.init_from_genome(self.population, new_genome, self.world)
        self.game.reset(self.world,self.population)

    def _get_game(self, world, population):
        return Game(world, population)
            
class GraphicGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, sim_params, selector, mutation_rate, fps):
        self.fps = fps
        super().__init__(sim_params, selector, mutation_rate)

    def play(self, generations, step):
        super().play(generations, step)
        self.game.exit()

    def _get_game(self, world, population):
        return GraphicGame(self.sim_params, world, population, self.fps)
