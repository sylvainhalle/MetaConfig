class DeviceParameter:
    def __init__(self, xmlNode, ref_param=None, name=None):
        if xmlNode==None:
            self.name = name
            self.ref_param = ref_param
            self.values = []
        else:
            self.ref_param = xmlNode.attributes['ref_param'].value
            self.name = xmlNode.attributes['name'].value
            self.values = []
            for value in xmlNode.getElementsByTagName("Value"):
                for v in value.childNodes:
                    self.values.append(v.data)

        """from IOSReference import printLog
        printLog("Created "+self.toString())"""


    def __str__(self):
        return "DeviceParameter [name='"+str(self.name)+", ref_param="+str(self.ref_param)+", values="+str(self.values)+"]"
