#ifndef ROOTMAKER_h
#define ROOTMAKER_h

#include <TTree.h>
#include <TFile.h>
#include <DataReader.h>
#include <string>
#include <sstream>
#include <channel.h>
#include <event.h>
#include <iostream>

class event;
class channel;

class RootMaker
{
  TFile* ofile;
  TTree* dataTree;
  TTree* headerTree;
  event current_event;
  // In Tree
  ULong64_t timestamp; // Holds 64-bit timestamp (adc counts)
  UInt_t** gate;      // gate[num_channels][num_gates]
  int** waveform; // Number of samples
  //uint64_t timestamp;
  //uint32_t** gate;
  //uint16_t** waveform;
  // Header info
  uint32_t evts;
  uint32_t chans;
  uint32_t format;
  uint32_t samples;
  uint32_t num_gates;
  // private member functions
  void header_tree();
public:
  RootMaker(std::string oname);
  ~RootMaker();
  void setup_tree(uint32_t, uint32_t, uint32_t, uint32_t);
  void load_event(event&);
};

#endif
