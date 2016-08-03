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

int main(int argc, char** argv)
{
  if( argc != 2 )
  {
    printf("format is input.dat" );
    return 1;
  }

  //sort_data(argv[1], argv[2]);
  sorter* data_sorter = new sorter(argv[1]);
  data_sorter->perform_sort();
  delete data_sorter; // free up that memory

  // Sorted file in now argv[2]
  // string sorted_data = argv[2];
  // printf("Finished sorting to %s\n", argv[2]);

  // Take sorted data and process
  //DataReader dr(sorted_data);
  //uint64_t last_time = 0;
  //vector<uint64_t> deltaT;
  ////while( !dr.eof )
  //for(int i=0; i<dr.num_events; i++)
  //{
  //  dr.next_event();
  //  deltaT.push_back(dr.currentevent.channels[0].timestamp - last_time);
  //  last_time = dr.currentevent.channels[0].timestamp;
  //}
  //double avg = accumulate(deltaT.begin(), deltaT.end(), 0) / deltaT.size();
  //printf("events actual vs vector: %i : %i\n", dr.num_events, deltaT.size());
  //printf("average dt: %f\n", avg);

  return 0;
}
