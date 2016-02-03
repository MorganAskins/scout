ROOTCFLAGS := $(shell root-config --cflags) -DUSE_ROOT -fPIC
ROOTLIBS := $(shell root-config --libs)

LIBNAME := RN

ROOTSO := libRN.so
ROOTSRC := SLMarsDetector_2.cpp SLMarsDetector_16.cpp RNDict.cc
ROOTHEAD := SLMarsDetector_2.h SLMarsDetector_16.h
ROOTOBJS := SLMarsDetector_2.o SLMarsDetector_16.o RNDict.o

LINKDEF := LinkDef.h

CPPFLAGS += -I$(ROOTSYS)/include $(ROOTCFLAGS)

all: shared

shared: $(ROOTOBJS)
	g++ -shared -O $(ROOTOBJS) -o $(ROOTSO) $(ROOTLIBS)

%.o: %.cpp
	g++ -c $*.cpp -o $*.o -I$(shell root-config --incdir) $(CPPFLAGS)

rootcint :
	rootcint -f RNDict.cc -c -I$(shell root-config --incdir) $(ROOTHEAD) $(LINKDEF)
	g++ -c RNDict.cc -o RNDict.o -I$(shell root-config --incdir) $(CPPFLAGS)

clean:
	rm -f RNDict.cc libRN.so *.o RNDict.h
