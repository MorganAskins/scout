MAIN := $(wildcard *.cpp)
PROGRAM := $(patsubst %.cpp, %, $(MAIN))

OPTIONS = $(shell root-config --cflags)
CXX = g++
CC = g++
CPPLIBS = -L/usr/lib -lhdf5 -lhdf5_cpp $(shell root-config --libs)
INCLUDES = -Iinclude 
SRC = src
ODIR = objects

BOOST = -I/usr/include/python3.5m -I/usr/include
BOOSTLIB = -L/usr/lib -lboost_python3 -L/usr/lib/python3.5m/config -lpython3

_OBJS = $(PROGRAM).o $(patsubst $(SRC)/%.cc, %.o, $(wildcard $(SRC)/*.cc))
OBJS = $(patsubst %, $(ODIR)/%, $(_OBJS))
ALL = --std=c++11 $(OPTIONS) $(INCLUDES) $(CPPLIBS)

all: standard

clean:
	rm -rf $(ODIR)/*.o $(PROGRAM)

standard: $(OBJS)
	g++ $(ALL) $(OBJS) -o $(PROGRAM)

shared: $(PROGRAM)
	g++ -Wl,--no-undefined -shared $(ALL) -fPIC $(OBJS) -o scout_builder.so

$(ODIR)/%.o: $(SRC)/%.cc
	g++ $(ALL) -shared -c -fPIC $(SRC)/$*.cc -o $(ODIR)/$*.o

$(ODIR)/%.o: %.cpp
	g++ $(ALL) -shared -c -fPIC $*.cpp -o $(ODIR)/$*.o

scout:

