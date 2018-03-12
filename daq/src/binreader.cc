#include <binreader.h>

namespace binreader{
  uint32_t readu32(std::ifstream& file)
  {
    uint32_t val;
    unsigned char bytes[4];
    file.read( (char*)bytes, 4);
    val = bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24);
    return val;
  }
  
  uint16_t readu16(std::ifstream& file)
  {
    uint16_t val;
    unsigned char bytes[2];
    file.read( (char*)bytes, 2);
    val = bytes[0] | (bytes[1] << 8); 
    return val;
  }
  
  void writeu32(std::ofstream& file, uint32_t val)
  {
    unsigned char bytes[4];
    bytes[0] = (val & 0xFF);
    bytes[1] = ( (val >> 8) & 0xFF );
    bytes[2] = ( (val >> 16) & 0xFF );
    bytes[3] = ( (val >> 24) & 0xFF );
  
    file.write( (char*)bytes, 4);
  }
  
  void writeu16(std::ofstream& file, uint16_t val)
  {
    unsigned char bytes[2];
    bytes[0] = (val & 0xFF);
    bytes[1] = ( (val >> 8) & 0xFF );
  
    file.write( (char*)bytes, 2);
  }
}
