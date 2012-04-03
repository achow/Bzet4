#  Python 3 64-bit interface for Quad Bzet implementation
#  that uses link traversal and variable bottom level encodings.

# Version of 2012 Jan 28

from   ctypes import *
import ctypes
import sys
import struct
from   os.path import dirname

bzetv = "v2.1"
vdate = "12-01-29"

python_v = sys.version_info.major
python_64bit = 8 * struct.calcsize("P") == 64
                                                # __file__ gets the full path of this pgm
dlldir = dirname(__file__)                      # this strips it to the directory only
dlldir.replace( '\\', '\\\\' )                  # Replaces \ with \\ in dlldir
lib = cdll.LoadLibrary(dlldir+'\\Bzet4.dll') # Loads from the full path to your module.

c_bzet = c_void_p       # Really a pointer to the c bzet structure.
                        # We never do anything with c_bzet except
                        # pass it to the c library functions.
                        # So it just has to be big enough for a 64-bit pointer.

# Ctypes Function Definitions for C Procedures

#  Create a new empty bzet                                     
# lib.Bzet4_newEmpty.argtypes = []
lib.Bzet4_newEmpty.restype  = c_bzet

#  Get Binary Repr of bzet      bzet     addr(result)
lib.Bzet4_repr.argtypes = [c_bzet, c_char_p]

#  Make bzet from Binary Repr       len(brepr)   addr(brepr)
# lib.Bzet4_EatBrepr.argtypes = [c_ulonglong, c_void_p]
# lib.Bzet4_EatBrepr.restype  = c_bzet

#  Get String of bzet            indent addr(brepr)
lib.Bzet4_HEX.argtypes = [c_bzet, c_int, c_void_p]

# Generate patterns of bits  start    length            
lib.Bzet4_RANGE.argtypes = [c_bzet, c_ulonglong, c_ulonglong ]
# ORs pattern into the bzet

# Get the size in bytes of the compressed bzet
lib.Bzet4_size.argtypes = [c_bzet]
lib.Bzet4_size.restype  = c_int

# How many T bits?
lib.Bzet4_COUNT.argtypes = [c_bzet]
lib.Bzet4_COUNT.restype  = c_longlong

##### Retrieve, Set and Unset a bit at some index

lib.Bzet4_TEST.argtypes = [c_bzet, c_ulonglong]
lib.Bzet4_TEST.restype  = c_bool

lib.Bzet4_SET.argtypes = [c_bzet, c_ulonglong]
lib.Bzet4_SET.restype  = c_bzet

lib.Bzet4_UNSET.argtypes = [c_bzet, c_ulonglong]
lib.Bzet4_UNSET.restype  = c_bzet

# Deep copy of a bzet, building a new one with same value
lib.Bzet4_clone.argtypes = [c_bzet]
lib.Bzet4_clone.restype  = c_bzet

##### Boolean Operations on bzets

# NOT inplace, changes argument value
lib.Bzet4_INVERT.argtypes = [c_bzet]

# And Or and Xor creates new bzet
lib.Bzet4_AND.argtypes = [c_bzet, c_bzet]
lib.Bzet4_AND.restype  = c_bzet

lib.Bzet4_OR.argtypes = [c_bzet, c_bzet]
lib.Bzet4_OR.restype  = c_bzet

lib.Bzet4_XOR.argtypes = [c_bzet, c_bzet]
lib.Bzet4_XOR.restype  = c_bzet

# lib.normalize.argtypes = [c_bzet]

# Get the Level of this Bzet
lib.Bzet4_LEV.argtypes = [c_bzet]
lib.Bzet4_LEV.restype  = c_ulonglong

# Release storage allocated to a bzet
lib.Bzet4_destroy.argtypes = [c_bzet]

# Treat a bzet a string of bits and compare
lib.Bzet4_COMPARE.argtypes = [c_bzet, c_bzet]
lib.Bzet4_COMPARE.restype  = c_bool

# Test for an empty bzet
lib.Bzet4_EMPTY.argtypes = [c_bzet]
lib.Bzet4_EMPTY.restypes = c_bool

# Bit Search of                       bzet    count        result    index   curr-location  
#lib.Bzet4_FindNthBit.argtypes = [c_bzet, c_ulonglong, c_void_p, c_void_p, c_void_p]
#lib.Bzet4_FindNthBit.restype  = c_bool

# Find the last bit in a bzet
lib.Bzet4_LAST.argtypes = [c_bzet]
lib.Bzet4_LAST.restype  = c_longlong

# Find the first bit in a bzet
lib.Bzet4_FIRST.argtypes = [c_bzet]
lib.Bzet4_FIRST.restype  = c_longlong


# Typedefs for later use
tcfun   = type(lib.Bzet4_AND)
tint    = type(3)
ttuple  = type( (0,0) )
tlist   = type( [0,0] )
tbarray = type( bytearray( [0,0] ) )

def mk_Brepr( crepr ):
    # take code for char repr of bzet and
    # create a Brepr from it.
    # This waits on running code so we can see what
    # a crepr really looks like.
    r = crepr
    return r

def complain( complaint, item ):
    print( 'Error: ' + complaint + ' (' + str(item) + ')' )
    print( 'Fix your program and try again.' )
    raise error

def syserr( complaint, item ):
    print( 'System Error: ' + complaint + ' (' + str(item) + ')' )
    print( 'Complain to your administrator.' )
    raise sys_error


class BZET:
    MT        = 0  # replaced with a Bzet of no bits

    @classmethod
    def BLevel(mymethod):
        return 1
    
    @classmethod
    def NewBLevel(mymethod,n):
        return
    
    @classmethod
    def Version(mymethod):        
        bv = "32"
        if python_64bit:
            bv = "64"
        return "Bzet4-" + bv + " " + bzetv + " BL1" + " " + vdate
            
    def __init__(self, x):
        self.obj = lib.Bzet4_newEmpty()
        if x == None: return
        elif type(x) == tint:      
            if x < 0: complain( "Set value negative in a BZET", x )
            lib.Bzet4_SET(self.obj, x)
        elif type(x) == tlist:
            for ix in x:                
                if type(ix) == tint:
                    if ix < 0: complain( "Set value negative in a BZET", ix )
                    lib.Bzet4_SET(self.obj, ix)
                elif type(ix) == ttuple:
                    nix = len(ix)
                    if nix >= 2:
                        s = ix[0] if ix[0] < ix[1] else ix[1]
                        if s < 0: complain( "Start value negative in a BZET", s )                            
                        n = abs( ix[1] - ix[0] ) + 1
                        if nix == 2:
                            lib.Bzet4_RANGE( self.obj, s, n )
                        else:
                            complain( "More than 2 Range Parameters in a BZET", nix )
                else:
                    print( "Error: Unknown type in specification list." )
                    print( repr(ix), "is of type", type(ix) )                       
                    raise error                
        elif type(x) == tbarray:
            xx = mk_Brepr( x )
            r = lib.Bzet4_EatBrepr(len(xx),xx[0])            
        else:
            complain( "Unknown type in BZET constructor", type(x) )
            raise error
        return
        
    @staticmethod
    def RANGE(start, nbits):
        return BZET( [(start, start+nbits),] )

    @staticmethod
    def INT(index):
        if index < 0: complain( "Index Value Error", index )
        return BZET(index)

    @staticmethod
    def BzetFromPtr(ptr):    # Create a new bzet and set its pointer to another bzet
        newBzet = BZET(None)
        lib.Bzet4_destroy(newBzet.obj)
        newBzet.obj = ptr
        return newBzet
    
    def Copy(self):
        return BZET.BzetFromPtr(lib.Bzet4_clone(self.obj))
    
    def __del__ (self):
        lib.Bzet4_destroy(self.obj)
		
    def size(self):
        return lib.Bzet4_size(self.obj)

    def COUNT(self):
        return lib.Bzet4_COUNT(self.obj)
        
    def SET(self, index):
        if index < 0: complain( "Index Value Error", index )
        lib.Bzet4_SET(self.obj, index)
        return self
        
    def UNSET(self, index):
        if index < 0: complain( "Index Value Error", index )
        lib.Bzet4_UNSET(self.obj, index)
        return self
        
    def get(self, index):
        if index < 0: complain( "Index Value Error", index )
        return lib.Bzet4_TEST(self.obj, index)

    def getBit(self, index):
        if index < 0: complain( "Index Value Error", index )
        return lib.Bzet4_TEST(self.obj, index)
    
    def __getitem__(self, key):
        return self.get(key)
        
    def __setitem__(self, key, value):
        if value:
            self.SET(key)
        else:
            self.UNSET(key) 
        
    def NOT(self):
        return BZET.BzetFromPtr(lib.Bzet4_NOT(self.obj))
        
    def AND(self, other):
        return BZET.BzetFromPtr(lib.Bzet4_AND(self.obj,other.obj))  
            
    def OR(self, other):
        return BZET.BzetFromPtr(lib.Bzet4_OR(self.obj,other.obj))

    def XOR(self, other):
        return BZET.BzetFromPtr(lib.Bzet4_XOR(self.obj,other.obj))

    def FLIP( self, n ):
        # Sets a bitset with the nth bit inverted
        if n < 0: complain( "Index Value Error", n )
        if self[n]:
            self.UNSET( n )
        else:
            self.SET( n )
        return self
    
    def INVERT( self ):
        # NOTs an entire bitset in place
        lib.Bzet4_INVERT(self.obj)        
        return self

    def CLEAR( self ):
        # Zeros a bitset.
        lib.Bzet4_destroy(self.obj)
        self.obj = lib.Bzet4_newEmpty()
        return self

    def LEV(self):
        return lib.Bzet4_LEV(self.obj)

    def BLEV(self):
        return 1
        
#    def Normalize(self):
#        return lib.Bzet4_Normalize(self.obj)
        
    def __bool__(self):
        # Test for any bit on returns True
        # All zeros returns False
        return not lib.Bzet4_EMPTY(self.obj)

    def __len__(self):
        # Returns the conceptual length of bitset
        return pow(4,(self.LEV()+1))

    def __str__(self):
        cstring = create_string_buffer(2000)
        lib.Bzet4_HEX(self.obj, cstring, 2000)
        return str(cstring.raw.rstrip(b'\x00'))[2:-2]
        
    def __repr__(self):
        size = self.size()
        crepr = create_string_buffer(size)
        lib.Bzet4_repr(self.obj,crepr)
        out = 'L'+ levelc[crepr.raw[0]]
        i = 0
        for c in crepr.raw[1:]:          
            if i & 0x07 == 0: out += ' '
            i += 1
            cx = hex( c )[2:]
            if len(cx) == 1: cx = '0'+cx
            out += cx       
        return out

    def compare(self, other):
        return lib.Bzet4_COMPARE(self.obj,other.obj)
        
    def __eq__(self,other):
        return lib.Bzet4_COMPARE(self.obj,other.obj)
                
    def __ne__(self,other):
        return not lib.Bzet4_COMPARE(self.obj,other.obj)
        
    def __or__    (self,other): return self.OR(other)
    def __and__   (self,other): return self.AND(other)
    def __xor__   (self,other): return self.XOR(other)
    def __invert__(self):       return self.NOT()
    def __ior__   (self,other): return self.OR(other)
    def __iand__  (self,other): return self.AND(other)
    def __ixor__  (self,other): return self.XOR(other)

    def LIST_T( self, dstart=0, limit=None ):
        # state = create_string_buffer(12)
        # A generator that returns a list of bit positions that are set
        if self == BZET.MT: return
        # Copy bzet for safty if use modifies self while processing
        nBzet = self.Copy()    

        # Set search parameters
        if dstart < 0: complain( "Start Value Error", dstart )        
        if limit  == None: limit = len(self)
        if limit < 0: complain( "Limit Value Error", limit )
        if dstart > 0:
            # Get the bits we are intererested in
            nbBzet &= BZET([(dstart,limit)])
        # Generate List
        for i in range(dstart,limit):
            pos = nBzet.FIRST()  # Find next bit
            if pos <= 0: break   # No more bits
            nBzet.UNSET(pos)     # Turn bit off in copy
            yield pos            # Give back control to caller     
        return

    def FIRST( self ):
        return lib.Bzet4_FIRST(self.obj)
                               
    def LAST( self ):
        return lib.Bzet4_LAST(self.obj)

    def HEX(self):
        lib.Bzet4_HEX(self.obj)

BZET.MT = BZET(None)
tbzet = type(BZET.MT) 
