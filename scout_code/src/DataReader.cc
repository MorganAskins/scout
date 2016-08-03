#include <DataReader.h>
#include <binreader.h>
#include <stdexcept>

DataReader::DataReader(std::string iname)
{
  this->infile.open(iname, std::ios::in | std::ios::binary);
  read_header();
}

void DataReader::read_header()
{
  this->num_events = binreader::readu32(this->infile);
  this->num_channels = binreader::readu32(this->infile);
  this->channel_bytes = binreader::readu32(this->infile);
  this->format = binreader::readu32(this->infile);
  this->current_event_num = 0;
  this->eof = false;
}

void DataReader::find_event(int ev)
{
  const int header_offset = 16; //bytes
  int location = ev*this->channel_bytes + header_offset;
  this->infile.seekg(location);
  if( static_cast<uint32_t>(ev) >= this->num_events )
    throw std::invalid_argument("event out of bounds");
  load_current_event();
  this->current_event_num = ev;
}

void DataReader::load_current_event()
{
  event current_event;
  for(uint32_t i=0; i<num_channels; i++)
  {
    channel mychan = channel();
    mychan.read_channel(this->infile);
    current_event.add_channel(mychan);
  }
  this->currentevent = current_event;
}

void DataReader::next_event()
{
  this->current_event_num++;
  load_current_event();
  this->current_event_num++;
  if( this->current_event_num >= this->num_events )
    this->eof = true;
  //printf("Event: %i\r", this->current_event_num);
}
