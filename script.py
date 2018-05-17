import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """                                                                                                                             
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p


    else:
        print "Parsing failed."
        return


    # print commands
    for line in commands:
#        print line
        command = line[0]
        # print command
        args = line[1:]
#        print args
        if command == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif command == 'pop':
            stack.pop()

        elif command == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif command == 'rotate':

            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]


        elif command == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]



        elif command == 'box':
            if not isinstance(args[0], float):
                args = args[1:]
            add_box(tmp,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []



        elif command == 'sphere':
             #print 'SPHERE\t' + str(args)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            if not isinstance(args[0], float):
                args = args[1:]
            add_sphere(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []


        elif command == 'torus':
            if not isinstance(args[0], float):
                args = args[1:]
             #print 'TORUS\t' + str(args)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            add_torus(tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []


        elif command == 'line':
            args2 = [x for x in args if isinstance(x, float)]
            args = args2
            add_edge( tmp,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []

        elif command == 'circle':
            add_circle(tmp,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []



        elif command == 'save':
            save_extension(screen, args[0])

        elif command == 'display':
            display(screen)




run("robot.mdl")






