#include <RootMaker.h>
#include <iostream>

RootMaker::RootMaker(std::string oname)
{
  this->ofile = new TFile(oname.c_str(), "RECREATE");
}

RootMaker::~RootMaker()
{
  this->ofile->Write();
  this->ofile->Close();
  //delete this->ofile;
  //delete this->gate;
  //delete this->waveform;
}
void RootMaker::setup_tree(uint32_t evts, std::vector<uint16_t> chan_list, uint32_t format, uint32_t samples)
{
  this->evts = evts;
  this->chans = chan_list.size();
  this->chan_list = chan_list;
  this->format = format;
  this->samples = samples;
  uint32_t num_gates = 0;
  if(format & 0b1)
    num_gates += 6;
  if(format & 0b10)
    num_gates += 2;
  this->gate = new UInt_t*[num_gates];
  this->waveform = new int*[chans];
  for(uint32_t i=0; i<chans; i++)
  {
    this->waveform[i] = new int[this->samples];
  }
  for(uint32_t i=0; i<num_gates; i++)
  {
    this->gate[i] = new UInt_t[chans];
  }
  this->num_gates = num_gates;

  header_tree();
  dataTree = new TTree("Data", "Scout Data");
  dataTree->SetDirectory(this->ofile);
  dataTree->Branch("timestamp", &(this->timestamp), "timestamp/l");

  // Loop over channels to write individual waveform ntuples
  for(uint32_t i=0; i<chans; i++)
  {
    std::string wfname = "waveform" + std::to_string( chidx_flip(this->chan_list[i]) );
    std::string wftype = wfname + "[" + std::to_string(this->samples) + "]/I";
    dataTree->Branch(wfname.c_str(), this->waveform[i], wftype.c_str());
  }
  // Loop over gates to write individual gates
  for(uint32_t i=0; i<num_gates; i++)
  {
    std::string gname = "gate" + std::to_string(i);
    std::string gtype = gname + "[" + std::to_string(chans) + "]/i";
    dataTree->Branch(gname.c_str(), this->gate[i], gtype.c_str());
  }

}

uint16_t RootMaker::chidx_flip( uint16_t chidx )
{
    // This is required due to a weird bug in the struck sis3316
    // where channel pairs are flipped
    uint16_t group_id = static_cast<uint16_t>(chidx / 4);
    uint16_t cid = chidx % 4;
    uint16_t swap_box[4] = { 1, 0, 3, 2 };
    uint16_t swapcid = swap_box[cid];
    return group_id*4 + swapcid;
}

void RootMaker::header_tree()
{
  headerTree = new TTree("Header", "Run Information");
  headerTree->SetDirectory(this->ofile);
  headerTree->Branch("Events", &this->evts);
  headerTree->Branch("Channels", &this->chans);
  headerTree->Branch("Format", &this->format);
  headerTree->Branch("Samples", &this->samples);
  headerTree->Fill();
}

void RootMaker::load_event(event& ev)
{
  for(uint32_t ch=0; ch<this->chans; ch++)
  {
    channel cur_chan = ev.channels[ch];
    uint32_t ele = 0;
    this->timestamp = cur_chan.timestamp;
    if( this->format & 0b1 )
    {
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate1);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate2);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate3);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate4);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate5);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate6);
    }
    if( this->format & 0b10 )
    {
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate7);
      this->gate[ele++][ch] = static_cast<UInt_t>(cur_chan.gate8);
    }
    for(uint32_t sam=0; sam < this->samples; sam++)
    {
      //this->waveform[ch][sam] = static_cast<unsigned long long>(cur_chan.waveform[sam]);
      this->waveform[ch][sam] = static_cast<int>(cur_chan.waveform[sam]);
    }
  }
  dataTree->Fill();
}

