'''
Neuronal morphology module for Brian.

TODO:
* Maybe str: should give a text representation of the tree
* set_length etc.: should be recursive
* check_consistency: check that lengths, area and coordinates are consistent (and fix)
* rescale: change number of compartments
'''
from brian.group import Group
from scipy import rand
from numpy import *
from brian.units import meter
from brian.stdunits import um
import warnings
from pylab import figure
import copy
try:
    from mpl_toolkits.mplot3d import Axes3D
except:
    warnings.warn('Pylab 0.99.1 is required for 3D plots')

__all__ = ['Morphology', 'Cylinder', 'Soma']


class Morphology(object):
    '''
    Neuronal morphology (=tree of branches).
    '''
    def __init__(self, filename=None, n=None):
        self.children = []
        self._namedkid = {}
        self.iscompressed = False
        if filename is not None:
            self.loadswc(filename)
        elif n is not None: # Creates a branch with n compartments
            # The problem here is that these parameters should have some self-consistency
            self.x, self.y, self.z, self.diameter, self.length, self.area = [zeros(n) for _ in range(6)]

    def set_length(self):
        '''
        Sets the length of compartments according to their coordinates
        '''
        x = hstack((0 * um, self.x))
        y = hstack((0 * um, self.y))
        z = hstack((0 * um, self.z))
        self.length = sum((x[1:] - x[:-1]) ** 2 + (y[1:] - y[:-1]) ** 2 + (z[1:] - z[:-1]) ** 2) ** .5

    def set_area(self):
        '''
        Sets the area of compartments according to diameter and length (assuming cylinders)
        '''
        self.area = pi * self.diameter * self.length

    def set_coordinates(self):
        '''
        Sets the coordinates of compartments according to their lengths (taking a random direction)
        '''
        l = cumsum(self.length)
        theta = rand()*2 * pi
        phi = rand()*2 * pi
        self.x = l * sin(theta) * cos(phi)
        self.y = l * sin(theta) * sin(phi)
        self.z = l * cos(theta)

    def loadswc(self, filename):
        '''
        Reads a SWC file containing a neuronal morphology.
        Large database at http://neuromorpho.org/neuroMorpho        
        Information below from http://www.mssm.edu/cnic/swc.html
        
        SWC File Format
        
        The format of an SWC file is fairly simple. It is a text file consisting of a header with various fields beginning with a # character, and a series of three dimensional points containing an index, radius, type, and connectivity information. The lines in the text file representing points have the following layout. 
        n T x y z R P
        n is an integer label that identifies the current point and increments by one from one line to the next.
        T is an integer representing the type of neuronal segment, such as soma, axon, apical dendrite, etc. The standard accepted integer values are given below.
            * 0 = undefined
            * 1 = soma
            * 2 = axon
            * 3 = dendrite
            * 4 = apical dendrite
            * 5 = fork point
            * 6 = end point
            * 7 = custom
        x, y, z gives the cartesian coordinates of each node.
        R is the radius at that node.
        P indicates the parent (the integer label) of the current point or -1 to indicate an origin (soma). 
        '''
        # 1) Create the list of segments, each segment has a list of children
        lines = open(filename).read().splitlines()
        segment = [] # list of segments
        types = ['undefined', 'soma', 'axon', 'dendrite', 'apical', 'fork', 'end', 'custom']
        previousn = -1
        for line in lines:
            if line[0] != '#': # comment
                numbers = line.split()
                n = int(numbers[0]) - 1
                T = types[int(numbers[1])]
                x = float(numbers[2]) * um
                y = float(numbers[3]) * um
                z = float(numbers[4]) * um
                R = float(numbers[5]) * um
                P = int(numbers[6]) - 1 # 0-based indexing
                if (n != previousn + 1):
                    raise ValueError, "Bad format in file " + filename
                seg = dict(x=x, y=y, z=z, T=T, diameter=2 * R, parent=P, children=[])
                location = (x, y, z)
                if T == 'soma':
                    seg['area'] = 4 * pi * R ** 2
                    seg['length'] = 0 * um
                else: # dendrite
                    locationP = (segment[P]['x'], segment[P]['y'], segment[P]['z'])
                    seg['length'] = (sum((array(location) - array(locationP)) ** 2)) ** .5 * meter
                    seg['area'] = seg['length'] * 2 * pi * R
                if P >= 0:
                    segment[P]['children'].append(n)
                segment.append(seg)
                previousn = n
        # We assume that the first segment is the root
        self.create_from_segments(segment)

    def create_from_segments(self, segment, origin=0):
        """
        Recursively create the morphology from a list of segments.
        Each segment has attributes: x,y,z,diameter,area,length (vectors) and children (list).
        It also creates a dictionary of names (_namedkid).
        """
        n = origin
        if segment[origin]['T'] != 'soma': # if it's a soma, only one compartment
            while (len(segment[n]['children']) == 1) and (segment[n]['T'] != 'soma'): # Go to the end of the branch
                n += 1
        # End of branch
        branch = segment[origin:n + 1]
        # Set attributes
        self.diameter, self.length, self.area, self.x, self.y, self.z = \
            zip(*[(seg['diameter'], seg['length'], seg['area'], seg['x'], seg['y'], seg['z']) for seg in branch])
        self.diameter, self.length, self.area, self.x, self.y, self.z = array(self.diameter), array(self.length), \
            array(self.area), array(self.x), array(self.y), array(self.z)
        self.type = segment[n]['T'] # normally same type for all compartments in the branch
        # Create children (list)
        self.children = [Morphology().create_from_segments(segment, origin=c) for c in segment[n]['children']]
        # Create dictionary of names (enumerates children from number 1)
        for i, child in enumerate(self.children):
            self._namedkid[str(i + 1)] = child
            # Name the child if possible
            if child.type in ['soma', 'axon', 'dendrite']:
                if child.type in self._namedkid:
                    self._namedkid[child.type] = None # two children with the same name: erase (see next block)
                else:
                    self._namedkid[child.type] = child
        # Erase useless names
        for k in self._namedkid.keys():
            if self._namedkid[k] is None:
                del self._namedkid[k]
        # If two kids, name them L (left) and R (right)
        if len(self.children) == 2:
            self._namedkid['L'] = self._namedkid['1']
            self._namedkid['R'] = self._namedkid['2']
        return self

    def branch(self):
        '''
        Returns the current branch without the children.
        '''
        morpho = copy.copy(self)
        morpho.children = []
        morpho._namedkid = {}
        return morpho

    def __getitem__(self, x):
        """
        Returns the subtree named x.
        Ex.: neuron['axon'] or neuron['11213']
        neuron[10*um:20*um] returns the subbranch from 10 um to 20 um.
        neuron[10*um] returns one compartment.
        neuron[5] returns compartment number 5.
        
        TODO:
        neuron[:] returns the full branch.
        """
        if type(x) == type(0): # int: returns one compartment
            morpho = self.branch()
            i = x
            j = i + 1
            morpho.diameter = morpho.diameter[i:j]
            morpho.length = morpho.length[i:j]
            morpho.area = morpho.area[i:j]
            morpho.x = morpho.x[i:j]
            morpho.y = morpho.y[i:j]
            morpho.z = morpho.z[i:j]
            if hasattr(morpho, '_origin'):
                morpho._origin += i
            return morpho
        elif isinstance(x, slice): # neuron[10*um:20*um]
            morpho = self.branch()
            start, stop = x.start, x.stop
            l = cumsum(morpho.length) # coordinate on the branch
            i = searchsorted(l, start)
            j = searchsorted(l, stop)
            morpho.diameter = morpho.diameter[i:j]
            morpho.length = morpho.length[i:j]
            morpho.area = morpho.area[i:j]
            morpho.x = morpho.x[i:j]
            morpho.y = morpho.y[i:j]
            morpho.z = morpho.z[i:j]
            if hasattr(morpho, '_origin'):
                morpho._origin += i
            return morpho
        elif isinstance(x, float): # neuron[10*um]
            morpho = self.branch()
            l = cumsum(morpho.length) # coordinate on the branch
            i = searchsorted(l, x)
            j = i + 1
            morpho.diameter = morpho.diameter[i:j]
            morpho.length = morpho.length[i:j]
            morpho.area = morpho.area[i:j]
            morpho.x = morpho.x[i:j]
            morpho.y = morpho.y[i:j]
            morpho.z = morpho.z[i:j]
            if hasattr(morpho, '_origin'):
                morpho._origin += i
            return morpho
        else:
            x = str(x) # convert int to string
            if (len(x) > 1) and all([c in 'LR123456789' for c in x]): # binary string of the form LLLRLR or 1213 (or mixed)
                return self._namedkid[x[0]][x[1:]]
            elif x in self._namedkid:
                return self._namedkid[x]
            else:
                raise AttributeError, "The subtree " + x + " does not exist"

    def __setitem__(self, x, kid):
        """
        Inserts the subtree and name it x.
        Ex.: neuron['axon'] or neuron['11213']
        If the tree already exists with another name, then it creates a synonym
        for this tree.
        The coordinates of the subtree are relative before function call,
        and are absolute after function call.
        """
        x = str(x) # convert int to string
        if (len(x) > 1) and all([c in 'LR123456789' for c in x]): # binary string of the form LLLRLR or 1213 (or mixed)
            self._namedkid[x[0]][x[1:]] = kid
        elif x in self._namedkid:
            raise AttributeError, "The subtree " + x + " already exists"
        else:
            # Update coordinates
            kid.x += self.x[-1]
            kid.y += self.y[-1]
            kid.z += self.z[-1]
            if kid not in self.children:
                self.children.append(kid)
                self._namedkid[str(len(self.children))] = kid # numbered child
            self._namedkid[x] = kid

    def __delitem__(self, x):
        """
        Removes the subtree x.
        """
        x = str(x) # convert int to string
        if (len(x) > 1) and all([c in 'LR123456789' for c in x]): # binary string of the form LLLRLR or 1213 (or mixed)
            del self._namedkid[x[0]][x[1:]]
        elif x in self._namedkid:
            child = self._namedkid[x]
            # Delete from name dictionary
            for name, kid in self._namedkid.items():
                if kid is child: del self._namedkid[name]
            # Delete from list of children
            for i, kid in enumerate(self.children):
                if kid is child: del self.children[i]
        else:
            raise AttributeError, "The subtree " + x + " does not exist"

    def __getattr__(self, x):
        """
        Returns the subtree named x.
        Ex.: axon=neuron.axon
        """
        return self[x]

    def __setattr__(self, x, kid):
        """
        Attach a subtree and named it x. If the subtree is None then the
        subtree x is deleted.
        Ex.: neuron.axon=Soma(diameter=10*um)
        Ex.: neuron.axon=None
        """
        if isinstance(kid, Morphology):
            if kid is None:
                del self[x]
            else:
                self[x] = kid
        else: # If it is not a subtree, then it's a normal class attribute
            object.__setattr__(self, x, kid)

    def __len__(self):
        """
        Returns the total number of compartments.
        """
        return len(self.x) + sum(len(child) for child in self.children)

    def compress(self, diameter=None, length=None, area=None, x=None, y=None, z=None, origin=0):
        """
        Compresses the tree by changing the compartment vectors to views on
        a matrix (or vectors). The morphology cannot be changed anymore but
        all other functions should work normally.
        
        origin : offset in the base matrix
        """
        self._origin = origin
        n = len(self.x)
        # Update values of vectors
        diameter[:n] = self.diameter
        length[:n] = self.length
        area[:n] = self.area
        x[:n] = self.x
        y[:n] = self.y
        z[:n] = self.z
        # Attributes are now views on these vectors
        self.diameter = diameter[:n]
        self.length = length[:n]
        self.area = area[:n]
        self.x = x[:n]
        self.y = y[:n]
        self.z = z[:n]
        for kid in self.children:
            kid.compress(diameter=diameter[n:], length=length[n:], area=area[n:], x=x[n:], y=y[n:], z=z[n:], origin=n)
            n += len(kid)
        self.iscompressed = True

    def plot(self, axes=None, simple=True, origin=None):
        """
        Plots the morphology in 3D. Units are um.
        axes : the figure axes (new figure if not given)
        simple : if True, the diameter of branches is ignored
        """
        if axes is None: # new figure
            fig = figure()
            axes = Axes3D(fig)
        x, y, z, d = self.x / um, self.y / um, self.z / um, self.diameter / um
        if origin is not None:
            x0, y0, z0 = origin
            x = hstack((x0, x))
            y = hstack((y0, y))
            z = hstack((z0, z))
        if len(x) == 1: # root with a single compartment: probably just the soma
            axes.plot(x, y, z, "r.", linewidth=d[0])
        else:
            if simple:
                axes.plot(x, y, z, "k")
            else: # linewidth reflects compartment diameter
                for n in range(1, len(x)):
                    axes.plot([x[n - 1], x[n]], [y[n - 1], y[n]], [z[n - 1], z[n]], 'k', linewidth=d[n - 1])
        for c in self.children:
            c.plot(origin=(x[-1], y[-1], z[-1]), axes=axes, simple=simple)


class Cylinder(Morphology):
    """
    A cylinder.
    """
    def __init__(self, length=None, diameter=None, n=1, type=None, x=None, y=None, z=None):
        """
        Creates a cylinder.
        n: number of compartments.
        type : 'soma', 'axon' or 'dendrite'
        x,y,z : end point (relative to origin of cylinder)
        length is optional (and ignored) if x,y,z is specified
        If x,y,z unspecified: random direction
        """
        Morphology.__init__(self)
        if x is None:
            theta = rand()*2 * pi
            phi = rand()*2 * pi
            x = length * sin(theta) * cos(phi)
            y = length * sin(theta) * sin(phi)
            z = length * cos(theta)
        else:
            length = (sum(array((x, y, z)) ** 2)) ** .5
        scale = arange(1, n + 1) * 1. / n
        self.x, self.y, self.z = x * scale, y * scale, z * scale
        self.length = ones(n) * length / n
        self.diameter = ones(n) * diameter
        self.area = ones(n) * pi * diameter * length / n
        self.type = type


class Soma(Morphology): # or Sphere?
    """
    A spherical soma.
    """
    def __init__(self, diameter=None):
        Morphology.__init__(self)
        self.diameter = ones(1) * diameter
        self.area = ones(1) * pi * diameter ** 2
        self.length = zeros(1)
        self.x, self.y, self.z = zeros(1), zeros(1), zeros(1)
        self.type = 'soma'

if __name__ == '__main__':
    from pylab import show
    #morpho=Morphology('mp_ma_40984_gc2.CNG.swc') # retinal ganglion cell
    morpho = Morphology('oi24rpy1.CNG.swc') # visual L3 pyramidal cell
    print len(morpho), "compartments"
    morpho.axon = None
    morpho.plot()
    #morpho=Cylinder(length=10*um,diameter=1*um,n=10)
    #morpho.plot(simple=True)
    morpho = Soma(diameter=10 * um)
    morpho.dendrite = Cylinder(length=3 * um, diameter=1 * um, n=10)
    morpho.dendrite.L = Cylinder(length=5 * um, diameter=1 * um, n=10)
    morpho.dendrite.R = Cylinder(length=7 * um, diameter=1 * um, n=10)
    morpho.dendrite.LL = Cylinder(length=3 * um, diameter=1 * um, n=10)
    morpho.axon = Morphology(n=5)
    morpho.axon.diameter = ones(5) * 1 * um
    morpho.axon.length = [1 * um, 2 * um, 1 * um, 3 * um, 1 * um]
    morpho.axon.set_coordinates()
    morpho.axon.set_area()
    morpho.plot(simple=True)
    show()
