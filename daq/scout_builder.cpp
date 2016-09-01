#include <fstream>
#include <string>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <numeric>
#include <map>
#include "channel.h"
#include "event.h"
#include "sorter.h"
#include "DataReader.h"
using namespace std;

// This is simply a test for the library
int main(int argc, char** argv)
{
  if( argc != 2 )
  {
    printf("format is input.dat" );
    return 1;
  }

  try {
    sorter* data_sorter = new sorter(argv[1]);
    data_sorter->perform_sort();
    delete data_sorter; // free up that memory
  }
  catch (const std::bad_alloc&) {
      return -1;
  }

  return 0;
}
