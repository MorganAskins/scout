#define DEBUG true
//
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
//#include "../library/SLMarsDetector_16.h"

// TODO: add the PMT's from the orphan tree and muon paddles
typedef std::map<double, int> EventMap;
typedef std::pair<double, int> EventPair;

class SLMarsDetector_16;
class SLMarsDetector_2;
class SLSis3316EventHeader_ROOT;

//void fillgates(double pmt[], SLMarsDetector_16* detector, int it);
void fillgates(double pmt[], SLSis3316EventHeader_ROOT header[], int it);
void fillgates(double pmt[], double errorcharge);
void addslowtree(TTree* slow);
void addconfigtree(TTree* config);
//void fillgates(double pmt[], SLMarsDetector_2* detector, int it);
// some typedefs for my maps
// map will be map<time, eventnum>

// Changing from adc time to ns
unsigned long long adc2ns = 1;

void simplify(string input_name)
{
  gSystem->Load("../library/libRN.so");

  TFile* file = new TFile(input_name.c_str());
  TTree* tree = (TTree*)file->Get("fastTree");
  TTree* orphan1 = (TTree*)file->Get("orphanTree1");
  TTree* orphan2 = (TTree*)file->Get("orphanTree2");

  string outname = "helloworld.root";
  // Setup the output file
  TFile* output = new TFile(outname.c_str(), "RECREATE");

  // Add in the slow tree information
  addslowtree((TTree*)file->Get("slowTree"));
  addconfigtree((TTree*)file->Get("configTree"));
  //TTree* smartTree = new TTree("data", "Simplified Data Structure");
  // Declare Needed branches here:
  unsigned long long event_time;
  // double target_pmt_charge[16];
  // double veto_pmt_charge[36];
  // double target_summed_charge;
  // double veto_summed_charge;
  // smartTree->Branch("target_pmt_charge", target_pmt_charge, "target_pmt_charge[16]/D");
  // smartTree->Branch("veto_pmt_charge", veto_pmt_charge, "veto_pmt_charge[36]/D");
  // smartTree->Branch("target_summed_charge", &target_summed_charge);
  // smartTree->Branch("veto_summed_charge", &veto_summed_charge);
  // smartTree->Branch("time", &event_time);

  // Tree with pure gate information
  double target_gate_charge[16][8];
  unsigned long long target_time[16];
  double veto_gate_charge[36][8];
  unsigned long long veto_time[36];
  TTree* gateTree = new TTree("pureData", "Contains all of the data from each gate");
  gateTree->Branch("target_pmt", target_gate_charge, "target_pmt[16][8]/D");
  gateTree->Branch("target_time", target_time, "target_time[16]/l");

  SLMarsDetector_16* detector;
  SLMarsDetector_2* orphan_det1;
  SLMarsDetector_2* orphan_det2;

  // SLMarsDetector_16 contains an array of SLSis3316EventHeader_ROOT

  tree->SetBranchAddress("detector_event.", &detector);

  SLSis3316EventHeader_ROOT* header = detector->channels;

  double prev_time = 0;
  double current_time = 0;
  int events = tree->GetEntries();

  //tree->GetEvent(start_event);

  cout << "Beginning to loop over events from file" << endl;

  for(int i=0; i<events; i++)
  {
    tree->GetEvent(i);
    for( int j=0; j<16; j++ )
    {
      fillgates(target_gate_charge[j], header, j);
      target_time[j] = header[j].Timestamp*adc2ns;
    }
    gateTree->Fill();
  }

  cout << "\nfinished the main loop\n";
  cout << "\nWriting to file" << endl;

  output->Write("", TObject::kOverwrite);
  output->Close();
  delete tree;
  delete file;

  return;
}



void fillgates(double pmt[], SLSis3316EventHeader_ROOT header[], int it)
{
  pmt[0] = header[it].AccumSumGate1;
  pmt[1] = header[it].AccumSumGate2;
  pmt[2] = header[it].AccumSumGate3;
  pmt[3] = header[it].AccumSumGate4;
  pmt[4] = header[it].AccumSumGate5;
  pmt[5] = header[it].AccumSumGate6;
  pmt[6] = header[it].AccumSumGate7;
  pmt[7] = header[it].AccumSumGate8;

  return;
}

void fillgates(double pmt[], double errorcharge)
{
  for(int i=0; i<8; i++)
    pmt[i]=errorcharge;

  return;
}

void addslowtree(TTree* slow)
{
  // Slow tree has two events, one at the beginning
  // of a run, and another at the end
  TTree* tree = new TTree("slowTree", "Detector information at run start/end");

  double target_voltages[16],
    target_currents[16],
    veto_voltages[36],
    veto_currents[36];

  // Gate widths in ns
  double target_gate_start[8]={ adc2ns * 0, adc2ns * 12, adc2ns * 12, adc2ns * 12,
				adc2ns * 12, adc2ns * 72, adc2ns * 72, adc2ns * 72 };
  double target_gate_end[8]={ adc2ns * 12, adc2ns * 32, adc2ns * 42, adc2ns * 52,
			      adc2ns * 72, adc2ns * 102, adc2ns * 112, adc2ns * 122 };
  double target_gate_width[8];

  double veto_gate_start[8]={ adc2ns * 0, adc2ns * 12, adc2ns * 12, adc2ns * 12,
				adc2ns * 12, adc2ns * 72, adc2ns * 72, adc2ns * 72 };
  double veto_gate_end[8]={ adc2ns * 12, adc2ns * 42, adc2ns * 52, adc2ns * 72,
			      adc2ns * 102, adc2ns * 102, adc2ns * 112, adc2ns * 122 };
  double veto_gate_width[8];

  for(int i=0; i<8; i++)
  {
    target_gate_width[i] = target_gate_end[i] - target_gate_start[i];
    veto_gate_width[i] = veto_gate_end[i] - veto_gate_start[i];
  }

  tree->Branch("target_voltages", &target_voltages, "target_voltages[16]/D");
  tree->Branch("target_currents", &target_currents, "target_currents[16]/D");
  tree->Branch("veto_voltages", &veto_voltages, "veto_voltages[36]/D");
  tree->Branch("veto_currents", &veto_currents, "veto_currents[36]/D");
  tree->Branch("target_gate_start", &target_gate_start, "target_gate_start[8]/D");
  tree->Branch("target_gate_end", &target_gate_end, "target_gate_end[8]/D");
  tree->Branch("target_gate_width", &target_gate_width, "target_gate_width[8]/D");
  tree->Branch("veto_gate_start", &veto_gate_start, "veto_gate_start[8]/D");
  tree->Branch("veto_gate_end", &veto_gate_end, "veto_gate_end[8]/D");
  tree->Branch("veto_gate_width", &veto_gate_width, "veto_gate_width[8]/D");

  // There are two formats that the tree may be in depending on the high
  // voltage power supply configuration
  // For earlier data it's this:
  if( slow->GetLeaf("ISEG0.channel.measuredVoltage") )
  {
    cout << "#### in ISEG0.channel.measuredVoltage" << endl;


    // Voltages in this leaf setup are as follows:
    // ISEG0 (V16-V31, excluding V20 & V27)
    // ISEG1 (V0 - V15)
    // ISEG2 (T0-T15)
    // ISEG3 {32,33,34,35,20,27}

    TLeaf* VoltLeaf0 = slow->GetLeaf("ISEG0.channel.measuredVoltage");
    TLeaf* VoltLeaf1 = slow->GetLeaf("ISEG1.channel.measuredVoltage");
    TLeaf* VoltLeaf2 = slow->GetLeaf("ISEG2.channel.measuredVoltage");
    TLeaf* VoltLeaf3 = slow->GetLeaf("ISEG3.channel.measuredVoltage");
    TLeaf* CurrLeaf0 = slow->GetLeaf("ISEG0.channel.measuredCurrent");
    TLeaf* CurrLeaf1 = slow->GetLeaf("ISEG1.channel.measuredCurrent");
    TLeaf* CurrLeaf2 = slow->GetLeaf("ISEG2.channel.measuredCurrent");
    TLeaf* CurrLeaf3 = slow->GetLeaf("ISEG3.channel.measuredCurrent");

    for(int ent=0; ent<slow->GetEntries(); ent++)
    {
      slow->GetEvent(ent);
      for(int slot=0; slot<16; slot++)
      {
	if (VoltLeaf2!=0) target_voltages[slot] = VoltLeaf2->GetValue(slot);
	if (CurrLeaf2!=0) target_currents[slot] = CurrLeaf2->GetValue(slot);
	if (VoltLeaf1!=0) veto_voltages[slot] = VoltLeaf1->GetValue(slot);
	if (CurrLeaf1!=0) veto_currents[slot] = CurrLeaf1->GetValue(slot);
	if( slot!=4 && slot!=11 )
	{
	  if (VoltLeaf0!=0) veto_voltages[slot+16] = VoltLeaf0->GetValue(slot);
	  if (CurrLeaf0!=0) veto_currents[slot+16] = CurrLeaf0->GetValue(slot);
	}
      }
      // Now the less straigt forward pmts
      if (VoltLeaf3!=0) veto_voltages[32] = VoltLeaf3->GetValue(0);
      if (VoltLeaf3!=0) veto_voltages[33] = VoltLeaf3->GetValue(1);
      if (VoltLeaf3!=0) veto_voltages[34] = VoltLeaf3->GetValue(2);
      if (VoltLeaf3!=0) veto_voltages[35] = VoltLeaf3->GetValue(3);
      if (VoltLeaf3!=0) veto_voltages[20] = VoltLeaf3->GetValue(4);
      if (VoltLeaf3!=0) veto_voltages[27] = VoltLeaf3->GetValue(5);
      if (CurrLeaf3!=0) veto_currents[32] = CurrLeaf3->GetValue(0);
      if (CurrLeaf3!=0) veto_currents[33] = CurrLeaf3->GetValue(1);
      if (CurrLeaf3!=0) veto_currents[34] = CurrLeaf3->GetValue(2);
      if (CurrLeaf3!=0) veto_currents[35] = CurrLeaf3->GetValue(3);
      if (CurrLeaf3!=0) veto_currents[20] = CurrLeaf3->GetValue(4);
      if (CurrLeaf3!=0) veto_currents[27] = CurrLeaf3->GetValue(5);
      tree->Fill();
    }
  } // End ISEG style

  //if(slow->GetLeaf("VHS_4_1.VM.0"))
  else {

    const std::string target_card[16]={"12_3", "12_3", "12_3", "12_3", "12_3", "12_3",
				       "12_3", "12_3", "12_3", "12_3", "12_3", "12_3",
				       "4_1", "4_1", "4_1", "4_1"};
    const std::string target_channel[16]={"0", "1", "0", "3", "2", "5", "6", "7", "8",
					  "9", "10", "11", "0", "1", "2", "3"};
    const std::string veto_card[36]={"12_1", "12_1", "4_3", "12_1", "12_1", "12_1", "12_1",
				     "12_1", "12_1", "12_1", "12_1", "4_3", "12_1", "4_2",
				     "4_2", "12_1", "12_2", "12_2", "12_2", "12_2", "4_2",
				     "12_2", "4_2", "12_2", "12_2", "12_2", "12_2", "12_2",
				     "12_2", "12_2", "12_2", "12_2", "12_2", "12_2", "12_3", "12_3"};
    const std::string veto_channel[36]={"0", "6", "3", "2", "3", "4", "5",
					"1", "8", "7", "9", "2", "10", "3",
					"2", "11", "0", "4", "4", "1", "0",
					"2", "1", "6", "5", "3", "8", "9",
					"6", "7", "10", "11", "0", "0", "4", "4"};

    for(int evt=0; evt<slow->GetEntries(); evt++)
    {
      slow->GetEvent(evt);
      for(int slot=0; slot<16; slot++)
      {
	TLeaf* vleaf = slow->GetLeaf(("VHS_"+target_card[slot]+".VM."+target_channel[slot]).c_str());
	if (vleaf!=0) target_voltages[slot]=vleaf->GetValue(0);
	TLeaf* ileaf = slow->GetLeaf(("VHS_"+target_card[slot]+".IM."+target_channel[slot]).c_str());
	if (ileaf!=0) target_currents[slot]=ileaf->GetValue(0);
      }	// Filled Target

      for(int slot=0; slot<36; slot++)
      {
	if(veto_card[slot]=="4_3")
	{
	  veto_voltages[slot]=-1;
	  veto_currents[slot]=-1;
	} // Card 4_3 is a problem card in terms of reporting information
	else
	{
	  TLeaf* vleaf = slow->GetLeaf(("VHS_"+veto_card[slot]+".VM."+veto_channel[slot]).c_str());
	  if (vleaf!=0) veto_voltages[slot]=vleaf->GetValue(0);
	  TLeaf* ileaf =slow->GetLeaf(("VHS_"+veto_card[slot]+".IM."+veto_channel[slot]).c_str());
	  if (ileaf!=0) veto_currents[slot]=ileaf->GetValue(0);
	}
      }	// Filled Veto
      tree->Fill();
    } // Beginning and End Event Filled
  } // End VHS style

  return;
}

void addconfigtree(TTree* config)
{
  TTree* tree = config->CloneTree(config->GetEntries());
  return;
}
