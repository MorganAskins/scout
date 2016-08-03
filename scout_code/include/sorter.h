#ifndef SORTER_h
#define SORTER_h 

#include <cstdint>
#include <vector>
#include <fstream>
#include <algorithm>
#include <map>
#include <channel.h>
#include <event.h>
#include <string>
#include <RootMaker.h>

class channel;
class event;
class RootMaker;

class sorter
{
public:
  sorter(std::string);
  std::map<uint64_t, event> all_events;
  ~sorter();
  std::ifstream infile;
  std::ofstream outfile;
  void perform_sort();
  void header();
  void write_sorted();
  uint32_t evts;
  uint32_t chans;
  uint32_t format;
  uint32_t chan_size;
  uint32_t samples;
  RootMaker* rMaker;
};

#endif
