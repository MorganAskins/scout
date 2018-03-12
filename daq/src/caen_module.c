//#include <Python.h>
//#include <iostream>
//#include <string>
//#include <cstdlib>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define UNIX
#include <CAENHVWrapper.h>

int handle = -1;

int init_caen()
{
  if (handle == -1)
  {
    // Init the system
    CAENHV_SYSTEM_TYPE_t system = DT55XX;
    int linktype = LINKTYPE_USB;
    char* arg_string = "0_0_0";
    char* username = "";
    char* password = "";

    // Connect to HV supply
    CAENHVRESULT ret = CAENHV_InitSystem( system, linktype, arg_string,
                                 username, password, &handle );
    return ret;
  }
}

int force_init_caen()
{
    handle = -1;
    init_caen();
}

float GetFloatParameter(int channel, char* param)
{
  init_caen();
  int slot = 0;
  const unsigned short Chlist[1] = {channel};
  float *answer = (float*)malloc(sizeof(float));

  CAENHVRESULT ret = CAENHV_GetChParam(handle, slot, param, 
                                       1, Chlist, answer);
  return answer[0];
}

int SetFloatParameter(int channel, char* param, float value)
{
  init_caen();
  int slot = 0;
  const unsigned short Chlist[1] = {channel};
  CAENHVRESULT ret = CAENHV_SetChParam(handle, slot, param, 1, 
					Chlist, &value);

  return ret;
}

int SetToggleStatus(int channel, char* param, unsigned long status)
{
// Status is 1 or 0, if not then set 0
  if( status != 0 && status != 1 )
    status = 0;
  init_caen();
  int slot = 0;
  const unsigned short Chlist[1] = {channel};
  CAENHVRESULT ret = CAENHV_SetChParam(handle, slot, param, 1,
  					Chlist, &status);
  return ret;
}

unsigned long GetToggleStatus(int channel, char* param)
{
  init_caen();
  int slot = 0;
  const unsigned short Chlist[1] = {channel};
  unsigned long *answer = malloc(sizeof(unsigned long));

  CAENHVRESULT ret = CAENHV_GetChParam(handle, slot, param, 
                                       1, Chlist, answer);
  return answer[0];
}

int NumParameter()
{
  init_caen();
  // Get Channel Parameter info
  char *parNameList = (char *)NULL;
  char (*par)[MAX_PARAM_NAME];
  int parNumber = 0;
  
  CAENHVRESULT ret = CAENHV_GetChParamInfo(handle, 0, 2, 
				&parNameList, &parNumber);
  return parNumber;
}

char* ChParamInfo(int pnum)
{
  init_caen();
  // Get Channel Parameter info
  char *parNameList = (char *)NULL;
  char (*par)[MAX_PARAM_NAME];
  int parNumber = 0;
  
  CAENHVRESULT ret = CAENHV_GetChParamInfo(handle, 0, 2, 
				&parNameList, &parNumber);

  par = (char (*)[MAX_PARAM_NAME])parNameList;

  return par[pnum];
}

char* ChParamProp(char* parname)
{
  init_caen();
  int slot = 0;
  unsigned long type;
  
  CAENHVRESULT ret = CAENHV_GetChParamProp(handle, slot, 0, parname,
  					 "Type", &type);
  if (type == PARAM_TYPE_NUMERIC)
    return "PARAM_TYPE_NUMERIC";
  else if (type == PARAM_TYPE_ONOFF)
    return "PARAM_TYPE_ONOFF";
  else
    return "NONE";
}

int main()
{
  int channel = 0;
  char* param = "Pw";
  unsigned long stat = GetToggleStatus(channel, param);
  printf("pw status: %u\n", stat);
  printf("pw status: %u\n", stat);
  printf("pw status: %u\n", stat);
  int ret = SetToggleStatus(channel, param, 1);
  printf("pw set: %04x\n", ret);
  stat = GetToggleStatus(channel, param);
  printf("pw status: %u\n", stat);
  sleep(2);
  printf("VMon: %10.2f\n", GetFloatParameter(channel, "VMon"));
  printf("VMon: %10.2f\n", GetFloatParameter(channel, "VMon"));
  printf("VMon: %10.2f\n", GetFloatParameter(channel, "VMon"));
  printf("VMon: %10.2f\n", GetFloatParameter(channel, "VMon"));
  printf("VMon: %10.2f\n", GetFloatParameter(channel, "VMon"));

  return 0;
}
