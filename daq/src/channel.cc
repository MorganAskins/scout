#include "channel.h"
#include <fstream>
#include <string>
#include <cstdint>
#include <vector>
#include <binreader.h>
//using namespace std;

channel::channel(){};

void channel::read_channel(std::ifstream& file)
{
  // Channel size is based upon format bit so read the first uint32;
  this->channel_size_in_bytes = 12;
  uint16_t header = binreader::readu16(file);
  this->format = (header & 0xF);
  this->channel_id = header >> 4;
  uint16_t ts_hi = binreader::readu16(file);
  uint16_t ts_low = binreader::readu16(file);
  uint16_t ts_mid = binreader::readu16(file);
  this->timestamp = (static_cast<uint64_t>(ts_hi) << 32) + (static_cast<uint64_t>(ts_mid) << 16) + ts_low;
  if( this->format & 0b0001 )
  {
    this->peakhigh_value = binreader::readu16(file);
    this->idx_phv = binreader::readu16(file);
    uint32_t g1_info = binreader::readu32(file);
    this->info = (g1_info >> 24);
    this->gate1 = (g1_info & 0xffffff);
    this->gate2 = binreader::readu32(file);
    this->gate3 = binreader::readu32(file);
    this->gate4 = binreader::readu32(file);
    this->gate5 = binreader::readu32(file);
    this->gate6 = binreader::readu32(file);
    this->channel_size_in_bytes += 7*4; 
  }
  if( this->format & 0b0010 )
  {
    this->gate7 = binreader::readu32(file);
    this->gate8 = binreader::readu32(file);
    this->channel_size_in_bytes += 8;
  }
  if( this->format & 0b0100 )
  {
    this->maw_max = binreader::readu32(file);
    this->maw_before = binreader::readu32(file);
    this->maw_after = binreader::readu32(file);
    this->channel_size_in_bytes += 12;
  }
  if( this->format & 0b1000 )
  {
    this->start_energy_value = binreader::readu32(file);
    this->max_energy_value = binreader::readu32(file);
    this->channel_size_in_bytes += 8;
  }
  this->sample_tag = binreader::readu32(file);
  uint32_t num_samples = 2*(this->sample_tag & 0x3ffffff);
  this->channel_size_in_bytes += num_samples*2;

  for(uint32_t i=0; i<num_samples; i++)
    waveform.push_back(binreader::readu16(file));

}

void channel::write_channel(std::ofstream& file)
{
  // Channel size is based upon format bit so read the first uint32;
  uint16_t header = this->format + (this->channel_id << 4);
  binreader::writeu16(file, header);
  uint16_t ts_hi = (this->timestamp >> 32);
  uint16_t ts_low = (this->timestamp & 0xFFFF);
  uint16_t ts_mid = (this->timestamp >> 16) & 0xFFFF;
  binreader::writeu16(file, ts_hi);
  binreader::writeu16(file, ts_low);
  binreader::writeu16(file, ts_mid);
  if( this->format & 0b0001 )
  {
    binreader::writeu16(file, this->peakhigh_value);
    binreader::writeu16(file, this->idx_phv);
    uint32_t g1_info = this->gate1 + (this->info << 24);
    binreader::writeu32(file, g1_info);
    binreader::writeu32(file, this->gate2);
    binreader::writeu32(file, this->gate3);
    binreader::writeu32(file, this->gate4);
    binreader::writeu32(file, this->gate5);
    binreader::writeu32(file, this->gate6);
  }
  if( this->format & 0b0010 )
  {
    binreader::writeu32(file, this->gate7);
    binreader::writeu32(file, this->gate8);
  }
  if( this->format & 0b0100 )
  {
    binreader::writeu32(file, this->maw_max);
    binreader::writeu32(file, this->maw_before);
    binreader::writeu32(file, this->maw_after);
  }
  if( this->format & 0b1000 )
  {
    binreader::writeu32(file, this->start_energy_value);
    binreader::writeu32(file, this->max_energy_value);
  }
  binreader::writeu32(file, this->sample_tag);
  uint32_t num_samples = 2*(this->sample_tag & 0x3ffffff);
  for(uint32_t i=0; i<num_samples; i++)
    binreader::writeu16(file, waveform[i]);
}

void channel::apply_tzero(uint64_t tzero)
{
    this->timestamp = this->timestamp - tzero;
}
