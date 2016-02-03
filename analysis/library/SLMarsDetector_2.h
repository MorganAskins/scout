#ifndef SLMARSDETECTOR2_h
#define SLMARSDETECTOR2_h

#include <vector>
//#include "./SLSis3316EventHeader_ROOT.h"
#include "SLSis3316FastData.h"
#include "./SLSis3316FastData_linkdef.h"
#include "TObject.h"

/*!
  @class SLMarsDetector_2
  @brief Contains the data for each 2 channel adc
*/

class SLSis3316EventHeader_ROOT;

class SLMarsDetector_2
{
public:
  SLSis3316EventHeader_ROOT channels[2];
  std::vector<unsigned short> samples[2];
  //int valid;
  SLMarsDetector_2(){};
  ~SLMarsDetector_2(){};
  ClassDef(SLMarsDetector_2,1); // Comment =)
};

#endif
