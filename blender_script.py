import bpy
import math
import random
import pickle

with open('/Users/arnavbarbaad/Desktop/3d_neural_network/mnist_train_images','rb') as file:
    train_data = pickle.load(file)

layer_counter = 0

class layer():
    def __init__(self, location=(0,0), dimension=(4,4), type="input"):
        global layer_counter 
        layer_counter += 1
        self.layer_no = layer_counter
        self.dimension = dimension
        x, y = location
        width, height = dimension
        if type == "input" or type == "output":
            row = 0
            for k in range(height * 2, 0, -2):
                row += 1
                column = 0
                for i in range(x, x + width * 2, 2):
                    column += 1
                    bpy.ops.mesh.primitive_cube_add(location=(i, y, k), radius=0.5)
                    bpy.context.object.name = "layer_" + str(self.layer_no) + "_cube_" + str(column + (row - 1) * width)
                    mat = bpy.data.materials.new(name="layer_" + str(self.layer_no) + "_cube_" + str(column + (row - 1) * width))
                    bpy.context.object.data.materials.append(mat)
                    
        if type == "hidden":
            row = 0
            for k in range(height * 2, 0, -2):
                row += 1
                column = 0
                for i in range(x, x + width * 2, 2):
                    column += 1
                    bpy.ops.mesh.primitive_uv_sphere_add(location=(i, y, k), size=0.2)
                    bpy.context.object.name = "layer_" + str(self.layer_no) + "_cube_" + str(column + (row - 1) * width)
                    mat = bpy.data.materials.new(name="layer_" + str(self.layer_no) + "_cube_" + str(column + (row - 1) * width))
                    bpy.context.object.data.materials.append(mat)
        
def connect_neurons(neuron1, neuron2):
    def __connect_points(v1, v2):
        midpoint = [(1 / 2) * (v1[0] + v2[0]), (1 / 2) * (v1[1] + v2[1]), (1 / 2) * (v1[2] + v2[2])]
        distance = math.sqrt((v2[0] - v1[0]) ** 2 + (v2[1] - v1[1]) ** 2 + (v2[2] - v1[2]) ** 2)
        z_rotation = math.atan((v2[1] - v1[1]) / ((v2[0] - v1[0]) + 0.00001))
        if (z_rotation > 0):
            y_rotation = math.atan((v2[2] - v1[2]) / math.sqrt((v2[1] - v1[1]) ** 2 + (v2[0] - v1[0]) ** 2))
        else:
            y_rotation = -math.atan((v2[2] - v1[2]) / math.sqrt((v2[1] - v1[1]) ** 2 + (v2[0] - v1[0]) ** 2))
        bpy.ops.curve.primitive_bezier_curve_add(location = midpoint, radius = distance / 2, rotation = [0, y_rotation, z_rotation])      
        bpy.context.object.data.bevel_depth = 0.010
        mat = bpy.data.materials.new(name=neuron1+"_"+neuron2)
        bpy.context.object.data.materials.append(mat)
    point_1 = list(bpy.data.objects[neuron1].location)
    point_2 = list(bpy.data.objects[neuron2].location)
    __connect_points(point_2, point_1)
    
def fire(string, trigger):
    bpy.data.materials[string].emit = trigger*2

def connect_layer(layer_1, layer_2, till_neuron, synapse_percent = 1):
    layer_1_no = layer_1.layer_no
    layer_2_no = layer_2.layer_no
    
    layer_1_size = layer_1.dimension[0]*layer_1.dimension[1]
    layer_2_size = layer_2.dimension[0]*layer_2.dimension[1] 
    total_synapses = layer_1_size*layer_2_size
    synapses_per_neuron = int(round(total_synapses*synapse_percent/100))
    neuron_list = list(range(1,layer_2_size+1))
    for i in range (0, till_neuron):
        for j in range(0, synapses_per_neuron):
            choose = random.choice(neuron_list)
            print("creating synapse"+str(i*synapses_per_neuron+j+1)+'/'+str(synapses_per_neuron*till_neuron))
            connect_neurons('layer_'+str(layer_1_no)+'_cube_'+str(i+1), 
                            'layer_'+str(layer_2_no)+'_cube_'+str(choose))
            
layer_1= layer(location = (0,0), dimension=(2, 2), type="input")
layer_2= layer(location = (6, 10), dimension=(2, 2), type="hidden")
connect_layer(layer_1, layer_2, synapse_percent = 100, till_neuron = 2)  

#neuron_list = list(range(1,784))
#for i in range (101,200):
 #  for _ in range(1, 5):
  #      print("Working on neuron "+str(i))
   #     choose = random.choice(neuron_list)
    #    connect_neurons('layer_1_cube_'+str(i), 'layer_2_cube_'+str(choose))   
   
#for i in range(0, 28):
 #   for j in range (0,28):
  #      activation = train_data[1,i,j]/255
   #     fire('layer_1_cube_'+str(i*28+j+1),activation)
        
print("Script failed successfuly")