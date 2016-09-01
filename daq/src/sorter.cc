#include <sorter.h>
#include <binreader.h>
#include <string>

sorter::sorter(std::string iname) 
{
  size_t lastindex = iname.find_last_of(".");
  std::string oname = iname.substr(0, lastindex) + "_sorted.dat";
  std::string rname = iname.substr(0, lastindex) + ".root";
  this->infile.open(iname, std::ios::in | std::ios::binary);
  this->outfile.open(oname, std::ios::out | std::ios::binary);
  this->rMaker = new RootMaker(rname);
}

sorter::~sorter()
{
  this->infile.close();
  this->outfile.close();
  delete rMaker;
}

void sorter::perform_sort()
{
  int counter = 0;
  while(!this->infile.eof())
  {
    channel mychan = channel();
    mychan.read_channel(this->infile);
    // Look for tzero
    if ( this->tzero.count(mychan.channel_id) == 0 )
        // no tzero yet, so set it
        this->tzero[mychan.channel_id]=mychan.timestamp;
    mychan.apply_tzero(this->tzero[mychan.channel_id]);
    counter++;
    if( infile.eof() )
      break;
    this->all_events[mychan.timestamp].add_channel(mychan);
  }
  header();
  write_sorted();
}

void sorter::header()
{
  // Header at the beginning of the file giving
  // total events, total channels, length of raw data, and format
  // each as 16 bit integers
  event first_event = this->all_events.begin()->second;
  this->evts = this->all_events.size();
  this->chans = first_event.channels.size();
  this->chan_size = first_event.channels[0].channel_size_in_bytes;
  this->format = first_event.channels[0].format;
  this->samples = first_event.channels[0].waveform.size();

  binreader::writeu32(this->outfile, this->evts);
  binreader::writeu32(this->outfile, this->chans);
  binreader::writeu32(this->outfile, this->chan_size);
  binreader::writeu32(this->outfile, this->format);
  binreader::writeu32(this->outfile, this->samples);
}

void sorter::write_sorted()
{
  // This is a test
  rMaker->setup_tree(this->evts, this->chans, this->format, this->samples);
  // Debug, 10 events
  int counter = 0;
  for (auto& kv : this->all_events)
  {
    kv.second.sort();
    if( kv.second.channels.size() == this->chans )
    {
      rMaker->load_event(kv.second);
      for (auto& v : kv.second.channels)
        v.write_channel(this->outfile);
    }
    //counter ++;
    //if ( counter >= 10 )
    //  break;
  }
}
