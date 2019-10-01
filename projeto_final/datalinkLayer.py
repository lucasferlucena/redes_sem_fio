import time
import copy
from physcalLayer import Physical
import logging
import numpy as np

class DataLink(Physical):
    def mediumAccessControl(self, pkg, nos):
        while(True):
            bToneNeighbors = 0
            for neighbor in nos[pkg.dl_header[0]].neighbors:
                bToneNeighbors += nos[neighbor.id].busy_tone
            
            if bToneNeighbors:                                                    #canal ocupado
                time.sleep(2.0*np.random.random_sample())              
            else:                                                                 #canal liberado
                for neighbor in nos[pkg.dl_header[0]].neighbors:
                    pkg_send = copy.deepcopy(pkg)
                    pkg_send.rec_node = neighbor.id 
                    nos[pkg.dl_header[0]].dataLinkSend(pkg_send, nos)
                break
        pass

    def dataLinkSend(self, pkg, nos):
        nos[pkg.rec_node].busy_tone = 1
        super().send(pkg, nos)
        pass

    def dataLiknkReceive(self, pkg, nos):
        nos[pkg.rec_node].busy_tone = 0
        if(pkg.rec_node == pkg.dl_header[1]) or (pkg.dl_header[1] == -1):
            nos[pkg.rec_node].networkReceive(pkg, nos)
        pass