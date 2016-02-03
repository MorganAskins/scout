/// @file $SLMOD_PATH/common/sis3316/SLSis3316FastData.h
/** @file $SLMOD_PATH/common/sis3316/SLSis3316FastData.h 
 *  @brief -*-*-*- TODO: Enter Description Here -*-*-*- 
 */
//Begin SLSis3316FastData.h
#ifndef SLSis3316_FAST_DATA
#define SLSis3316_FAST_DATA

#include <stdio.h>
#ifdef ROOT_FILE_OUTPUT
	#include "Rtypes.h"
#endif

#ifndef SLERR_OK
#define SLERR_OK 0
#endif

#ifndef ROOT_FILE_OUTPUT
#define ROOT_FILE_OUTPUT 
#endif

/** @class SLSis3316FastData
 *  @brief sis3316 Fast Data Container
 *
 *  Provides storage for Fast data.
 *
 *  Format flag in SLSis3316EventHeaderA determines which other headers are present
 */

#pragma pack(push,2)

#include "TObject.h"
class SLSis3316EventHeaderA{
public:
	unsigned int FormatBits            : 4;
	unsigned int ChannelID             : 12;
	unsigned int TimestampH            : 16;
	unsigned int TimestampL            : 32;

	SLSis3316EventHeaderA(){}     ///< Default Constructor
	~SLSis3316EventHeaderA(){}	  ///< Destructor
	
	int Sprint(const char* options=""){
		printf(
			"\nSLSis3316 Fast Data Header\n"
			"----------------------------------\n"
			"ChannelID              :: %X\n"
			"FormatBits             :: 0x%01X\n"
			"Timestamp             :: 0x%04X%08X\n"
			, ChannelID
			, FormatBits
			, TimestampH, TimestampL
			);
		return SLERR_OK;
	}
};
#pragma pack(pop)
#pragma pack(push,2)
class SLSis3316EventHeaderB{
	// If FormatBit[0] = 1
public:
	unsigned int PeakHighValue         : 16;
	unsigned int IndexPeakHighValue    : 16;
	unsigned int AccumSumGate1         : 24;
	unsigned int InformationReserved   : 4;
	unsigned int OverFlowFlag          : 1;
	unsigned int UnderFlowFlag         : 1;
	unsigned int RePileupFlag          : 1;
	unsigned int PileUpFlag            : 1;
	unsigned int AccumSumGate2         : 32;
	unsigned int AccumSumGate3         : 32;
	unsigned int AccumSumGate4         : 32;
	unsigned int AccumSumGate5         : 32;
	unsigned int AccumSumGate6         : 32;
	SLSis3316EventHeaderB(){}     ///< Default Constructor
	~SLSis3316EventHeaderB(){}	  ///< Destructor
	int Sprint(const char* options=""){
		printf(
			"==== SLSis3316 Event Header B ====\n"
			"IndexPeakHighValue      :: 0x%04X\n"
			"PeakHighValue           :: 0x%04X\n"
			"OverFlowFlag            :: 0x%01X\n"
			"UnderFlowFlag           :: 0x%01X\n"
			"RePileupFlag            :: 0x%01X\n"
			"PileUpFlag              :: 0x%01X\n"
			"AccumSumGate1           :: 0x%04X\n"
			"AccumSumGate2           :: 0x%04X\n"
			"AccumSumGate3           :: 0x%04X\n"
			"AccumSumGate4           :: 0x%04X\n"
			"AccumSumGate5           :: 0x%04X\n"
			"AccumSumGate6           :: 0x%04X\n"
			, IndexPeakHighValue
			, PeakHighValue
			, OverFlowFlag
			, UnderFlowFlag
			, RePileupFlag
			, PileUpFlag
			, AccumSumGate1
			, AccumSumGate2
			, AccumSumGate3
			, AccumSumGate4
			, AccumSumGate5
			, AccumSumGate6
			);
		return SLERR_OK;
	}
};
#pragma pack(pop)
#pragma pack(push,2)
class SLSis3316EventHeaderC{
public:
	// If FormatBit[1] = 1
	unsigned int AccumSumGate7         : 32;
	unsigned int AccumSumGate8         : 32;
	SLSis3316EventHeaderC(){}     ///< Default Constructor
	~SLSis3316EventHeaderC(){}	  ///< Destructor
	int Sprint(const char* options=""){
		printf(
			"==== SLSis3316 Event Header C ====\n"
			"AccumSumGate7           :: 0x%04X\n"
			"AccumSumGate8           :: 0x%04X\n"
			, AccumSumGate7
			, AccumSumGate8
			);
		return SLERR_OK;
	}
};
#pragma pack(pop)
#pragma pack(push,2)
class SLSis3316EventHeaderD{
public:	
	// If FormatBit[2] = 1
	unsigned int MawMaxValue           : 32;
	unsigned int MawValueAfterTrig     : 32;
	unsigned int MawValueBeforeTrig    : 32;
	SLSis3316EventHeaderD(){}     ///< Default Constructor
	~SLSis3316EventHeaderD(){}	  ///< Destructor
	int Sprint(const char* options=""){
		printf(
			"==== SLSis3316 Event Header D ====\n"
			"MawMaxValue             :: 0x%04X\n"
			"MawValueBeforeTrig      :: 0x%04X\n"
			"MawValueAfterTrig       :: 0x%04X\n"
			, MawMaxValue
			, MawValueBeforeTrig
			, MawValueAfterTrig
			);
		return SLERR_OK;
	}
};
#pragma pack(pop)
#pragma pack(push,2)
class SLSis3316EventHeaderTrailer{
public:
	unsigned int NumberRawSamples      : 26;
	unsigned int Zero                  : 1;
	unsigned int MawTestFlag           : 1;
	unsigned int FooterHeader          : 4;
	SLSis3316EventHeaderTrailer(){}     ///< Default Constructor
	~SLSis3316EventHeaderTrailer(){}	  ///< Destructor
	int Sprint(const char* options=""){
		printf(
			"==== SLSis3316 Event Header Trailer ====\n"
			"FooterHeader (0xE)     :: 0x%01X\n"
			"MawTestFlag            :: 0x%01X\n"
			"Zero (0x0)             :: 0x%01X\n" 
			"NumberRawSamples       :: %d\n"
			, FooterHeader
			, MawTestFlag
			, Zero
			, NumberRawSamples
			);
		return SLERR_OK;
	}
};
#pragma pack(pop)


#ifdef ROOT_FILE_OUTPUT
#pragma pack(push,2)
class SLSis3316EventHeader_ROOT{
	
	public:
	unsigned long long Timestamp       ;
	unsigned int ChannelID             ;
	unsigned int FormatBits            ;
	// If FormatBit[0] = 1			   ;
	unsigned int IndexPeakHighValue    ;
	unsigned int PeakHighValue         ;
	unsigned int OverFlowFlag          ;
	unsigned int UnderFlowFlag         ;
	unsigned int RePileupFlag          ;
	unsigned int PileUpFlag            ;
	unsigned int InformationReserved   ;
									   ;
	unsigned int AccumSumGate1         ;
	unsigned int AccumSumGate2         ;
	unsigned int AccumSumGate3         ;
	unsigned int AccumSumGate4         ;
	unsigned int AccumSumGate5         ;
	unsigned int AccumSumGate6         ;
	// If FormatBit[1] = 1			   ;
	unsigned int AccumSumGate7         ;
	unsigned int AccumSumGate8         ;
	// If FormatBit[2] = 1			   ;
	unsigned int MawMaxValue           ;
	unsigned int MawValueAfterTrig     ;
	unsigned int MawValueBeforeTrig    ;
									   ;
	// Footer						   ;
	unsigned int FooterHeader          ;
	unsigned int MawTestFlag           ;
	unsigned int Zero                  ;
	unsigned int NumberRawSamples      ;
	
	SLSis3316EventHeader_ROOT(){}     ///< Default Constructor
	~SLSis3316EventHeader_ROOT(){}	  ///< Destructor

	int Sprint(const char *options="")
	{
		//TODO: Parse timestamp for display
		printf(
			"\nSLSis3316 Fast Data Header\n"
			"----------------------------------\n"
			"ChannelID              :: %X\n"
			"FormatBits             :: 0x%01X\n"
			"Timestamp              :: %lld ticks\n"
			, ChannelID
			, FormatBits
			, Timestamp
			);
		if(FormatBits & (1 << 0)){
			printf(
			"IndexPeakHighValue      :: 0x%04X\n"
			"PeakHighValue           :: 0x%04X\n"
			"OverFlowFlag            :: 0x%01X\n"
			"UnderFlowFlag           :: 0x%01X\n"
			"RePileupFlag            :: 0x%01X\n"
			"PileUpFlag              :: 0x%01X\n"
			"AccumSumGate1           :: 0x%04X\n"
			"AccumSumGate2           :: 0x%04X\n"
			"AccumSumGate3           :: 0x%04X\n"
			"AccumSumGate4           :: 0x%04X\n"
			"AccumSumGate5           :: 0x%04X\n"
			"AccumSumGate6           :: 0x%04X\n"
			, IndexPeakHighValue
			, PeakHighValue
			, OverFlowFlag
			, UnderFlowFlag
			, RePileupFlag
			, PileUpFlag
			, AccumSumGate1
			, AccumSumGate2
			, AccumSumGate3
			, AccumSumGate4
			, AccumSumGate5
			, AccumSumGate6
			);
		}
		if(FormatBits & (1 << 1)){
			printf(
			"AccumSumGate7           :: 0x%04X\n"
			"AccumSumGate8           :: 0x%04X\n"
			, AccumSumGate7
			, AccumSumGate8
			);
		}
		if(FormatBits & (1 << 2)){
			printf(
			"MawMaxValue             :: 0x%04X\n"
			"MawValueBeforeTrig      :: 0x%04X\n"
			"MawValueAfterTrig       :: 0x%04X\n"
			, MawMaxValue
			, MawValueBeforeTrig
			, MawValueAfterTrig
			);
		}
		printf(
			"FooterHeader (0xE)     :: 0x%01X\n"
			"MawTestFlag            :: 0x%01X\n"
			"Zero (0x0)             :: 0x%01X\n" 
			"NumberRawSamples       :: %d\n"
			, FooterHeader
			, MawTestFlag
			, Zero
			, NumberRawSamples
			);
		return SLERR_OK;
	}
	
  ClassDef(SLSis3316EventHeader_ROOT,1)
};

#pragma pack(pop)
#endif

#endif
//End SLSis3316FastData.h
