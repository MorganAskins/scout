import bpy
import math
from scout_constants import *
from scout_tools import *
import pmt, shield, pmt_holder, av, room, splitter

## Todo
# Add pmt mounts
# Add acrylic legs (or pvc)
# Add BNC connectors
# Add quick-connects
# Add stirring vessel


# clear mesh and object
for item in bpy.context.scene.objects:
    if item.type == 'MESH' or item.type == 'LAMP':
        bpy.context.scene.objects.unlink(item)
for item in bpy.data.objects:
    if item.type == 'MESH':
        bpy.data.objects.remove(item)
for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)
for item in bpy.data.materials:
    bpy.data.materials.remove(item)

def main():
    prettyRender()
    print('Detector volume: %g' % av_volume_litres, 'litres')
    start_spot = pmt_length + pmt_bottom_clearance
    pmt.draw((pmt_location,pmt_location,start_spot), (1,0,0), 0*math.pi)
    pmt.draw((-pmt_location,pmt_location,start_spot), (1,0,0), 0*math.pi)
    pmt.draw((pmt_location,-pmt_location,start_spot), (1,0,0), 0*math.pi)
    pmt.draw((-pmt_location,-pmt_location,start_spot), (1,0,0), 0*math.pi)
    shield.draw((0,0,0), (1,0,0), 0)
    pmt_holder.draw((0,0,start_spot), (1,0,0), 0)
    av.draw((0,0,start_spot), (1,0,0), 0)
    room.draw((0,0,0), (1,0,0), 0)
#    splitter.split()

def prettyRender():
    # Ceiling light
    bpy.ops.object.add( type='LAMP', location = (2, -2, 20) )
    lamp1 = bpy.context.object
    lamp1.name = 'scout_sun'
    lamp = lamp1.data
    lamp.name = 'SUN'
    lamp.type = 'POINT'
    lamp.energy = 20
    # Little light inside (origin plus an inch)
    bpy.ops.object.add( type='LAMP', location = (0, 0, 1*inches) )
    lamp2 = bpy.context.object
    lamp2.name = 'scout_led'
    lamp = lamp2.data
    lamp.name = 'Led'
    lamp.type = 'POINT'
    lamp.energy = 1

if __name__ == '__main__':
    main()
