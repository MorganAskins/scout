import ctypes
import os, sys, time

class pycaen():
    def __init__(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib/libcaen.so'))
        self._ccaen = ctypes.CDLL(path)
        self._getparameterinfo()

    def _reinit_caen(self):
        self._ccaen.force_init_caen()

    def GetParameter(self, channel, param):
        # This will try both built in functions for float and toggle
        # status is not supported yet ... #TODO
        ret = self._GetFloatParameter(channel, param)
        if type(ret) is not str:
            return ret
        ret = self._GetToggleStatus(channel, param)
        if type(ret) is not str:
            return ret
        return 'Parameter not accessible'

    def SetParameter(self, channel, param, value):
        ret = self._SetFloatParameter(channel, param, value)
        if type(ret) is not str:
            return ret
        ret = self._SetToggleStatus(channel, param, value)
        if type(ret) is not str:
            return ret
        return 'Parameter not accessible'

    def _GetFloatParameter(self, channel, param):
        if param not in self.param_list:
            return "Parameter Not Found"
        if self.param_type_dict[param] != 'PARAM_TYPE_NUMERIC':
            return "Parameter Not Float"
        cfunc= self._ccaen.GetFloatParameter
        cfunc.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char))
        array_type = ctypes.c_char * len(param)
        cfunc.restype = ctypes.c_float
        return cfunc( ctypes.c_int(channel), array_type(*param) )

    def _SetFloatParameter(self, channel, param, value):
        if param not in self.param_list:
            return "Parameter Not Found"
        if self.param_type_dict[param] != 'PARAM_TYPE_NUMERIC':
            return "Parameter Not Float"
        cfunc = self._ccaen.SetFloatParameter
        cfunc.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_float)
        cfunc(channel, param, value)
        #if self._GetFloatParameter(channel, param) is not value:
        #    print 'Get and set values dont match'

    def _GetToggleStatus(self, channel, param):
        if param not in self.param_list:
            return "Parameter Not Found"
        if self.param_type_dict[param] != 'PARAM_TYPE_ONOFF':
            return "Parameter Not Bool"
        cfunc = self._ccaen.GetToggleStatus
        cfunc.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char))
        array_type = ctypes.c_char * len(param)
        #cfunc.restype = ctypes.c_ulong
        ret_value = -1
        ret_value = cfunc( ctypes.c_int(channel), array_type(*param) )
        return ret_value

    def _SetToggleStatus(self, channel, param, status):
        if param not in self.param_list:
            return "Parameter Not Found"
        if self.param_type_dict[param] != 'PARAM_TYPE_ONOFF':
            return "Parameter Not Bool"
        param = ctypes.c_char_p(param)
        channel = ctypes.c_int(channel)
        status = ctypes.c_ulong(status)
        cfunc = self._ccaen.SetToggleStatus
        cfunc.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_ulong)
        cfunc(channel, param, status)


    def _getparameterinfo(self):
        self.num_param = self._ccaen.NumParameter()
        cfunc = self._ccaen.ChParamInfo
        cfunc.argtype = ctypes.c_int
        cfunc.restype = ctypes.c_char_p
        self.param_list = [ cfunc(i) for i in range(self.num_param) ]
        self.param_type_dict = {}
        cfunc = self._ccaen.ChParamProp
        cfunc.argtype = ctypes.c_char_p
        cfunc.restype = ctypes.c_char_p
        for p in self.param_list:
            self.param_type_dict[p] = cfunc(p)
            

if __name__ == '__main__':
    hv = pycaen()
    time.sleep(1)
    print hv.param_list
    print hv.param_type_dict
    #hv._SetFloatParameter(3, "VSet", 120)
    print 'Pw:', hv._GetToggleStatus(0, 'Pw')
    print 'Pw:', hv._GetToggleStatus(0, 'Pw')
    print 'Pw:', hv._GetToggleStatus(0, 'Pw')
    print 'VMon:', hv._GetFloatParameter(0, 'VMon')
    print 'VMon:', hv._GetFloatParameter(0, 'VMon')
    print 'VMon:', hv._GetFloatParameter(0, 'VMon')
    print 'Pw:', hv._SetToggleStatus(0, 'Pw', 1)
    #print 'VMon:', hv._GetFloatParameter(0, 'VMon')
    print 'Pw:', hv._GetToggleStatus(0, 'Pw')
    #print 'VMon:', hv._GetFloatParameter(0, 'VMon')
