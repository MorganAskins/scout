#ifndef BINREADER_h
#define BINREADER_h

#include <fstream>
#include <string>
#include <cstdint>
//using namespace std;

namespace binreader{
  uint32_t readu32(std::ifstream& file);
  uint16_t readu16(std::ifstream& file);
  void writeu32(std::ofstream& file, uint32_t val);
  void writeu16(std::ofstream& file, uint16_t val);
}

#endif
