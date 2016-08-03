#include <cstdint>
#include <vector>
#include <fstream>
#include <algorithm>
#include "event.h"

event::event(){};

bool sortByChannel(const channel& lhs, const channel& rhs) { return lhs.channel_id < rhs.channel_id; }

void event::sort() { std::sort( this->channels.begin(), this->channels.end(), sortByChannel ); } 

void event::add_channel(channel ch) { this->channels.push_back(ch); }
