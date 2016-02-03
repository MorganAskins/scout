#ifndef SLMARSDETECTOR16_h
#define SLMARSDETECTOR16_h

#include <vector>
//#include "./SLSis3316EventHeader_ROOT.h"
#include "SLSis3316FastData.h"
#include "./SLSis3316FastData_linkdef.h"
#include "TObject.h"

/*!
  @class SLMarsDetector_16
  @brief Contains the data for each 16 channel adc
*/

class SLSis3316EventHeader_ROOT;

class SLMarsDetector_16
{
public:
  SLSis3316EventHeader_ROOT channels[16];
  std::vector<unsigned short> samples[16];
  int valid;
  SLMarsDetector_16(){ valid = 0x0; }
  ~SLMarsDetector_16(){};
  ClassDef(SLMarsDetector_16,1); // Comment =)
};

#endif

