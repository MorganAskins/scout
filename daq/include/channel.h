#ifndef CHANNEL_h
#define CHANNEL_h

#include <cstdint>
#include <vector>
#include <fstream>


class channel
{
  public:
  channel();
  int channel_size_in_bytes;
  unsigned char format;
  uint16_t channel_id;
  uint64_t timestamp;

  // Format bit 1
  uint16_t peakhigh_value;
  uint16_t idx_phv;
  uint16_t info;
  uint32_t gate1;
  uint32_t gate2;
  uint32_t gate3;
  uint32_t gate4;
  uint32_t gate5;
  uint32_t gate6;
  // Format bit 2
  uint32_t gate7;
  uint32_t gate8;
  // Format bit 3
  uint32_t maw_max;
  uint32_t maw_before;
  uint32_t maw_after;
  // Format bit 4
  uint32_t start_energy_value;
  uint32_t max_energy_value;

  uint32_t sample_tag;
  std::vector<uint16_t> waveform;

  void read_channel(std::ifstream& file);
  void write_channel(std::ofstream& file);
  void apply_tzero(uint64_t);
};

#endif
