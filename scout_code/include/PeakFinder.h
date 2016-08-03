#ifndef PEAKFINDER_h
#define PEAKFINDER_h

#include <event.h>
#include <channel.h>
#include <string>
#include <fstream>

class event;
class channel;

class PeakFinder
{
  std::ifstream infile;
public:
  PeakFinder(std::string);

};

#endif
