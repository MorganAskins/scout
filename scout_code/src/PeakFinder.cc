#include <PeakFinder.h>

PeakFinder::PeakFinder(std::string iname)
{
  this->infile.open(iname, std::ios::in | std::ios::binary);
}
