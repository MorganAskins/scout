#ifndef EVENT_h
#define EVENT_h 

#include <cstdint>
#include <vector>
#include <fstream>
#include "channel.h"

class channel;

class event
{
public:
  event();
  std::vector<channel> channels;
  void sort();
  void add_channel(channel);
};

#endif
