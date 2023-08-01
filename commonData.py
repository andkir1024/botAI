

# статус паралельных линий
import enum

class TypeСutout(enum.Enum):
    undifined = 0
    UType0 = 1
    UType1 = 2
    UType2 = 3
    UType3 = 4

class DirectionStatus(enum.Enum):
    dir0 = 0
    dir90 = 1
    dir180 = 2
    dir270 = 3
    dir360 = 8

    dir0_90 = 4
    dir90_180 = 5
    dir180_270 = 6
    dir270_360 = 7
    undifined = 10

    # dir00 = 0
    # dir45 = 1
    # dir90 = 2
    # dir135 = 3
    # dir180 = 4
    # dir225 = 5
    # dir270 = 6
    # dir315 = 7
    # dir360 = 8
    # undifined = 10

class svgCountoure(enum.Enum):
    svgM = 0
    svgL = 1
    svgCHalfCircle = 2
    svgZ = 3
    svgC = 4

class ParallStatus(enum.Enum):
    # не паралельны
    none = 0
    # закругленный угол  
    vert = 1
    vert_left = 2
    vert_right = 3
    # последовательность линий
    hor_down = 4
    hor_up = 5
    hor = 6
    def isCoord(stat):
        if stat == ParallStatus.none:
            return False
        if stat == ParallStatus.vert or stat == ParallStatus.vert_left or stat == ParallStatus.vert_right:
            return False
        if stat == ParallStatus.hor_down or stat == ParallStatus.hor_up or stat == ParallStatus.hor:
            return False
        return True

class LineStatus(enum.Enum):
    round = 0
    sequest = 1
    parallel = 2
    undefined = 3

class Corner:
    cross = ParallStatus.none
    minX = minY =maxX =maxY=0
    linesFig = None
    pointsFig = None
    cornerFig = None
    dirFig = None
    def __init__(self, minX,minY,maxX,maxY,linesFig,cross, pointsFig):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.cross = cross
        self.linesFig = linesFig
        self.pointsFig = pointsFig
