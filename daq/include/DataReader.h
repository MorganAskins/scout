#ifndef DATAREADER_h
#define DATAREADER_h

#include <channel.h>
#include <event.h>
#include <string>
#include <cstdint>

class channel;
class event;

// Iterator to load in events from file

class DataReader
{
  std::ifstream infile;
public:
  event currentevent;
  bool eof;
  uint32_t num_events;
  uint32_t num_channels;
  uint32_t channel_bytes;
  uint32_t format;
  uint32_t current_event_num;
  DataReader(std::string);
  void read_header();
  void find_event(int);
  void load_current_event();
  void next_event();
};

#endif
