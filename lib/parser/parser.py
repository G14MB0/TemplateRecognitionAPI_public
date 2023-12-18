# -*- coding: utf-8 -*-
"""
@author: Gianmaria Castaldini
"""
# setup.py>

import pandas as pd
import numpy as np
#import sys

# from alive_progress import alive_bar; import time
        #%%
        
# Questa classe di funzioni elabora il file .dbc e crea una struttura dati
# la struttura dati ha come colonne:
# ["ECU","MSG","msg_ID","msg_LEN","Signal","Range","Factor-Offset","Length_Bit","Unit"]    
class Gateway:  
    """This class is able to load a .dbc file and parse it in a Pandas dataFrame

    Returns:
        _type_: _description_
    """    
    del_BU = 'BU_'      #lista centraline
    del_BO = 'BO_'      #messaggio
    del_SG = 'SG_'      #segnale
    del_BA = 'BA_'      #attributi del messaggio
    del_VAL = 'VAL_'    #descrizione dei valori
    del_BO_TX_BU = 'BO_TX_BU_'
    del_EMP = ""        #delimitatore vuoto
    
    colnames = ["ECU","MSG","msg_ID","msg_LEN","Signal","Range","Factor-Offset","Length_Bit","Unit"]
    ECU_LIST_GLOBAL_DF = pd.DataFrame(columns = colnames)
    ECU_LIST = []
    ECU_LIST_GLOBAL = []
    last_ECU = ""
    msg_ID = ""
    msg_LEN = ""
    msg_ = ""
    sg_ECU_dest = []
    sg_RAN = []
    sg_FO = []
    sg_LB = ""
    sg_ = ""
    sg_UI = ""
    
    warning_list = []
    
    can_name = ""
    
    flag_BO_TX_BU = False
    
    
    
    # This function load the .dbc
    def _init(self, GW_dbc_name):
        """Load the .dbc file and parse it

        Args:
            GW_dbc_name (string): file path

        Returns:
            dataFrame: the dbc parsed into a pandas dataframe
        """        
        self.warning_list = []
        try:
            with open(GW_dbc_name, 'r') as f:
                fp = f.readlines()
        except:
            from lib.utils import global_var
            global_var.log_file += "\n [GW_elaboration.py][_init] Error opening "+ str(GW_dbc_name if GW_dbc_name is not None else "")
            print (global_var.log_file)
        
        # try:
        Database = self._elab(fp)
        self.Search_CRC_MC(Database)
        return Database
        # except Exception as inst:
            # print('\n****** Error ******')
            # print(str(inst))
            # print('****** Error ******\n')
    
    #this function reset some values referred to signal
    def reset_sg(self):
        """Reset certain attributes used during the dbc rows loop
        """        
        # self.msg_ID = ""
        # self.msg_LEN = ""
        # self.msg_ = ""
        self.sg_ECU_dest = []
        self.sg_RAN = []
        self.sg_FO = []
        self.sg_LB = ""
        self.sg_ = ""
        self.sg_UI = ""
    
    #this function reset some values referred to message
    def reset_msg(self):
        """reset some attribute used during the dbc rows loop
        """        
        self.msg_ID = ""
        self.msg_LEN = ""
        self.msg_ = ""        
    
    
    #this function search for CRC and message_counter signals inside messages
    def Search_CRC_MC(self, Database):
        """this methd iterates over all the signal in the DBC dataframe and search for the message counter and the crc.
        it sets the column "CRC" or "MC" to 1 respectively.
        At the moment it is studied to search for the string 'MessageCounter_' or "MC_" or 'CRC_' accordingly to italian database format

        usually is called after the database has been parsed

        Args:
            Database (dataFrame): the parsed database into pandas dataframe
        """        

        Signals = Database.Signal.tolist()
        index_crc = []
        index_mc = []
        for line in Signals:
            if (len(line) >= 15 and line[0:15] == 'MessageCounter_') or line[0:3] == "MC_":
                index_mc.append(1)
                index_crc.append(0)
            elif len(line) >= 4 and line[0:4] == 'CRC_':
                index_crc.append(1)
                index_mc.append(0)
            else:
                index_mc.append(0)
                index_crc.append(0)
                
        Database["CRC"] = index_crc
        Database["MC"] = index_mc
        self.ECU_LIST_GLOBAL_DF["CRC"] = index_crc
        self.ECU_LIST_GLOBAL_DF["MC"] = index_mc
    
    # #This function returns list of signals given a message
    # def Give_signals(self, message, Database):
    #     return self.Database.Signal.where(self.Database_DF.Signal==SG_temp).dropna().index.values.astype(int)[0]
    
    
    
    
    #This function elaborate the dbc text and create Database.class object, then store it
    #in the list ECU_LIST_GLOBAL
    def _elab(self, fp):
        """This function elaborate the dbc text and create Database.class object, then store it
            in the list ECU_LIST_GLOBAL
            other elabs are made after this so this is the first "skeleton" of DBC dataframe

            # more comment can be found in the code lines #
        Args:
            fp (readline instance): the instance of the .dbc file opened with readlines()

        Returns:
            DBC: the dbc parsed as a dataframe with the main column.
        """        
              
        i = 0
        for l_no, line in enumerate(fp):
            temp = line.lstrip().split()    #la funzione lstrip() elimina gli spazi a sinistra        
            #gli if di qesta sezione sono impostati che: se il primo valore della riga coincide con uno 
            #specifico delimitatore (definiti sopra), allora ci troviamo in un determinato tratto del DBC 
            #che esplica una determinata cosa. A quel punto chiama le funzioni di formattazione
            if temp != []:
                if temp[0].removesuffix(":") == self.del_BU: 
                    self.ECU_LIST = line.removeprefix("BU_: ").removesuffix("\n").split(" ") #Get the ECU list from DBC BU_ list
                    # try:
                    #     #remove unwanted ECUs
                    #     self.ECU_LIST.remove("DIAG_TEST")
                    # except: 
                    #     pass
            
                if temp[0].replace(" ","") == self.del_BO: #Get the message and loop all the signals until the next message
                    self.BO(temp)
                    
                if temp[0] == self.del_SG: #Get all the msg info (signals)
                    temp = [t.strip() for t in temp]
                    if self.last_ECU == self.del_EMP: # in last_ECU there is the ECU of the message
                        i = i+1
                    else:   
                        self.SG(temp, line) #Done for each signal of the message
                        self.Structurize() #save the signal inside the dataframe
                        self.reset_sg() #reset all the global variables
                if temp[0].removesuffix(":") == self.del_BO_TX_BU: 
                    if len(temp) > 1:
                        self.BO_TX_BU(temp) #delimiter used to duplicate the message between ECUs -> BO_TX_BU_ 1448 : ECM,VDCM; -> Msg with id 1448 defined for ECM is also tx from VCDCM
        
        #Aggiungo alcune colonne 
        self.ECU_LIST_GLOBAL_DF["Numeric_value"] = np.nan
        self.ECU_LIST_GLOBAL_DF["Numeric_value"] = self.ECU_LIST_GLOBAL_DF["Numeric_value"].astype(object)
        self.ECU_LIST_GLOBAL_DF["Description"] = np.nan
        self.ECU_LIST_GLOBAL_DF["Description"] = self.ECU_LIST_GLOBAL_DF["Description"].astype(object)
        #  with alive_bar(0) as bar:      
        for l_no, line in enumerate(fp):             
            temp = line.lstrip().split()
            #uguale a prima ma rifaccio il ciclo for perchè mi serve il dataframe completo
            #al quale aggiungere valori specifici
            if len(temp) > 1:
                
                if temp[0] == self.del_BA:
                        self.BA(temp,line)
                        
                if temp[0] == self.del_VAL:
                        # try:
                        self.VALUE(temp, line, l_no)
                        # except ValueError:
                        #     print(Exception.message)
                        #     return -1
        
        import math
        for i in range(len(self.ECU_LIST_GLOBAL_DF.Signal)):
            # print(self.ECU_LIST_GLOBAL_DF.SignalLong[i])
            if 'SignalLong' in self.ECU_LIST_GLOBAL_DF:
                if str(self.ECU_LIST_GLOBAL_DF.SignalLong[i]) != "nan":
                    self.ECU_LIST_GLOBAL_DF.Signal[i] = self.ECU_LIST_GLOBAL_DF.SignalLong[i]
            
            if int(self.ECU_LIST_GLOBAL_DF.Length_Bit[i]) > 64:
                self.ECU_LIST_GLOBAL_DF = self.ECU_LIST_GLOBAL_DF.drop([i])
            
        return self.ECU_LIST_GLOBAL_DF.reindex()
            
    
    ###############
    ###############
    
    #formatta le definizioni dei valori dei segnali
    def VALUE(self, temp, line, l_no):
        """cicciopanza

        Args:
            temp (_type_): _description_
            line (_type_): _description_
            l_no (_type_): _description_

        Raises:
            Exception: _description_
        """        
        def_list = []
        num_list = []
        num_list_int = []
        SG_temp = temp[2]
        if len(temp) > 3:
            if temp[3].removeprefix("-").isnumeric() == False:
                raise Exception("Error in VAL_secition, no integer found as first value description. line number: "+str(l_no+1)+
                                '\nTry to check if in that line the 4th value is a number or, otherwise, is a DBC error'+
                                '\nDBC correct format:  VAL_ ID Sgn_name Num1 "---" Num2 "---" ...')
                # return -1
            # line_temp = line.removesuffix("\n").split(" ")
            line_temp = line.removesuffix("\n").split()
            line_temp = " ".join(line_temp[3:])
            line_temp = line_temp.split("\"")
            for i in range(0,len(line_temp)-1,2):
                # if line_temp[i].strip().isnumeric():
                # print(line_temp[i], l_no)
                if not(int(line_temp[i]) in num_list_int):
                    num_list.append(line_temp[i])
                    def_list.append(line_temp[i+1])
                    num_list_int.append(int(line_temp[i]))

            try:
                index = self.ECU_LIST_GLOBAL_DF.Signal.where(self.ECU_LIST_GLOBAL_DF.Signal==SG_temp).dropna().index.values.astype(int)[0]
                self.ECU_LIST_GLOBAL_DF.at[index, "Numeric_value"] = num_list
                self.ECU_LIST_GLOBAL_DF.at[index, "Numeric_value"] = [eval(i) for i in num_list]
                self.ECU_LIST_GLOBAL_DF.at[index, "Description"] = def_list
            except:
                pass
    
    ###############
    #formatta alcuni attributi dei segnali
    def BA(self, temp, line):
        try:
            if line.split("\"")[1] == "GenSigStartValue":
                SG_temp = temp[-2]
                init_value = int(temp[-1].removesuffix("\n").removesuffix(";"))
                index = self.ECU_LIST_GLOBAL_DF.Signal.where(self.ECU_LIST_GLOBAL_DF.Signal==SG_temp).dropna().index.values.astype(int)[0]
                self.ECU_LIST_GLOBAL_DF.loc[index, "InitValue"] = init_value
            if line.split("\"")[1] == "SystemSignalLongSymbol":
                SG_temp = temp[-1].removesuffix("\n").removesuffix(";").removesuffix("\"").removeprefix("\"")
                signal_temp = temp[-2]
                # print(signal_temp)
                # print(signal_temp)
                filter1 = self.ECU_LIST_GLOBAL_DF["Signal"]==signal_temp
                filter2 = self.ECU_LIST_GLOBAL_DF["msg_ID"]==temp[-3]                    
                index = (self.ECU_LIST_GLOBAL_DF["Signal"].where(filter1 & filter2).dropna().index.values.astype(int))[0]
                # index = self.ECU_LIST_GLOBAL_DF.Signal.where(self.ECU_LIST_GLOBAL_DF.Signal==signal_temp).dropna().index.values.astype(int)[0]     
                # self.ECU_LIST_GLOBAL_DF.signal
                    # init_value = int(temp[-1].removesuffix("\n").removesuffix(";"))
                # index = self.ECU_LIST_GLOBAL_DF.Signal.where(self.ECU_LIST_GLOBAL_DF.Signal==SG_temp).dropna().index.values.astype(int)[0]
                self.ECU_LIST_GLOBAL_DF.loc[index, "SignalLong"] = SG_temp
            if line.split("\"")[1] == "DBName":
                self.can_name = temp[-1].replace(";","").replace("'","").replace('"',"").replace('.', '')
            if line.split("\"")[1] == "Period [ms]":
                SG_temp = temp[-2] #Message ID
                period_value = int(temp[-1].removesuffix("\n").removesuffix(";"))
                # Find all indexes where msg_ID matches SG_temp
                indexes = self.ECU_LIST_GLOBAL_DF.index[
                    self.ECU_LIST_GLOBAL_DF["msg_ID"] == SG_temp
                ].tolist()
                # Assign period_value to all matching indexes
                self.ECU_LIST_GLOBAL_DF.loc[indexes, "period"] = period_value
        except Exception as e:
            print('error on' + str(line.split("\"")[1]) + "where line is: " + str(line))
            print(e)

            
    
    ###############
    #formatta il messaggio
    def BO(self, temp):
        self.last_ECU = temp[-1].removesuffix("\n")
        self.msg_LEN = temp[-2]
        self.msg_ = temp[2].removesuffix(":")
        self.msg_ID = temp[1]
        
        
    def BO_TX_BU(self, temp):
        msg_ID_to_copy = temp[1]
        involved_ecu = temp[-1].removesuffix(";").split(",")
        if len(involved_ecu) > 1:
            filter1 = self.ECU_LIST_GLOBAL_DF["msg_ID"]==str(msg_ID_to_copy)
            from_ecu = ""
            df_temp = pd.DataFrame()
            for ecu in involved_ecu:      
                filter2 = self.ECU_LIST_GLOBAL_DF["ECU"]==str(ecu)
                df_temp = self.ECU_LIST_GLOBAL_DF.where(filter1 & filter2).dropna()
                if len(df_temp) > 0:
                    if not self.flag_BO_TX_BU:
                        self.ECU_LIST_GLOBAL_DF["duplicatedEcu"] = ['']*len(self.ECU_LIST_GLOBAL_DF)
                        self.ECU_LIST_GLOBAL_DF["toSkip"] = [False]*len(self.ECU_LIST_GLOBAL_DF)
                        self.flag_BO_TX_BU = True
                    from_ecu = ecu
                    from_df_temp = self.ECU_LIST_GLOBAL_DF.where(filter1 & filter2).dropna()
                    break
            if from_ecu =="":
                self.warning_list.append("Message with ID "+str(msg_ID_to_copy)+ " is duplicated within " +str(involved_ecu)+" but any from ecu is found. Skipped")
            else:
                involved_ecu.remove(from_ecu)
                #string of involved ecu separated by %%
                involved_ecu_str = '%%'.join(involved_ecu)
                #add the duplicated ecu in the "master" ecu 
                self.ECU_LIST_GLOBAL_DF.loc[from_df_temp.index,"duplicatedEcu"] = involved_ecu_str
                #mark as to skip messages that will be duplicated
                from_df_temp["toSkip"] = [True]*len(from_df_temp)
                for ecu in involved_ecu:
                    from_df_temp.ECU = str(ecu)
                    # print(from_df_temp)
                    self.ECU_LIST_GLOBAL_DF = pd.concat([self.ECU_LIST_GLOBAL_DF, from_df_temp], ignore_index=True)
                    # print(ecu,msg_ID_to_copy)
                    
        
        
    
    ###############    
    #formatta il segnale
    def SG(self, temp, line):
        self.sg_ECU_dest = temp[-1].removesuffix("\n").split(",")             
        self.sg_ECU_dest[-1] = self.sg_ECU_dest[-1].removesuffix("\n")
        self.sg_UI = line.split("\"")[2]
        temp = " ".join(line.split("\"")[:1]).split()
        self.sg_RAN = temp[-1].replace("[","").replace("]","").split("|")
        self.sg_RAN = [eval(i) for i in self.sg_RAN]  #convert in list of integer
        self.sg_FO = temp[-2].replace("(","").replace(")","").split(",")
        self.sg_FO = [eval(i) for i in self.sg_FO]  #convert in list of integer
        if self.sg_FO[0] == 0:
            self.sg_FO[0] = 1
        #self.sg_LB = temp[-3].split("|")[-1].removesuffix("@0+").removesuffix("@1+").removesuffix("@1-")
        self.sg_LB = temp[-3].split("|")[-1].split("@")[0]
        self.sg_ = temp[1]
        return self.sg_
    ###############   
    #crea la struttura e la carica su un DF                  
    def Structurize(self):
        # SG_temp = Database(self.last_ECU, self.msg_, self.msg_LEN, self.msg_ID, self.sg_, self.sg_RAN, self.sg_FO, self.sg_LB, self.sg_UI)
        duplicated_signal_msg_list = self.SearchF("MSG","Signal",self.sg_)
        # print(self.msg_)
        if duplicated_signal_msg_list is not None: #list of msg with self.sg_
            if self.msg_ in duplicated_signal_msg_list: #if self.msg_ is already in the msg list means the signal is duplicated
               self.warning_list.append("Message "+self.msg_+ " has signal " +self.sg_+" more than one time. Only the first one taken.") #skip the signal saving
            else: #if the signal is already present but in other messages do the usual saving
                if self.last_ECU in self.ECU_LIST:
                    list_temp = [self.last_ECU, self.msg_, self.msg_ID, 
                                                           self.msg_LEN, self.sg_, self.sg_RAN, 
                                                           self.sg_FO, self.sg_LB, self.sg_UI]
                    self.ECU_LIST_GLOBAL.append(list_temp) 
                    df_temp = pd.DataFrame(data=list_temp).T
                    df_temp.columns = self.colnames
                    self.ECU_LIST_GLOBAL_DF = pd.concat([self.ECU_LIST_GLOBAL_DF, df_temp], ignore_index=True)
                    
        else: #if the signal is saved for the first time
            if self.last_ECU in self.ECU_LIST:
                list_temp = [self.last_ECU, self.msg_, self.msg_ID, 
                                                       self.msg_LEN, self.sg_, self.sg_RAN, 
                                                       self.sg_FO, self.sg_LB, self.sg_UI]
                self.ECU_LIST_GLOBAL.append(list_temp) 
                df_temp = pd.DataFrame(data=list_temp).T
                df_temp.columns = self.colnames
                self.ECU_LIST_GLOBAL_DF = pd.concat([self.ECU_LIST_GLOBAL_DF, df_temp], ignore_index=True)
        
    ###############    
    #funzione di ricerca per valori precisi       
    def SearchF(self, Column1, Column2, Item, Column3 = "", Item1 = "" ):
        try:
            filter1 = self.ECU_LIST_GLOBAL_DF[Column2]==Item
            if Column3 !="" and Item1 != "":
                filter2 = self.ECU_LIST_GLOBAL_DF[Column3]==Item1
                searched = self.ECU_LIST_GLOBAL_DF[Column1].where(filter1 & filter2).dropna().values
            else:
                searched = self.ECU_LIST_GLOBAL_DF[Column1].where(filter1).dropna().values
            
            # if  not np.any(searched):
            if searched.size == 0:
                raise Exception('No element found among '+str(Column1)+' that satisfies the requirements --- item searched: '+str(Item))
            return searched
        except Exception as inst:
            return
            #print('\n****** Warning ******')
            print(str(inst))
            #print('****** Warning ******\n')
        
    
    ###############
    #ritorna la lista centraline
    def _ECU_List(self):
        # print(list(dict.fromkeys(self.ECU_LIST_GLOBAL_DF.ECU)))
        return list(dict.fromkeys(self.ECU_LIST_GLOBAL_DF.ECU))
        # return self.ECU_LIST
    
    def _MSG_List(self):
        # MSG_List = []
        # for ecu in list(dict.fromkeys(self._ECU_List())):
        #     for msg in list(dict.fromkeys(self.SearchF("MSG", "ECU", ecu))):
        #         MSG_List.append(msg)
        # return MSG_List
        MSG_ECU_List = self._ECU_MSG_List()
        MSG_List = [item[1] for item in MSG_ECU_List]
        return MSG_List
        
    
    def _ECU_MSG_List(self):
        MSG_ECU_List = []
        for ecu in self._ECU_List():
            for msg in list(dict.fromkeys(self.SearchF("MSG", "ECU", ecu))):
                MSG_ECU_List.append([ecu,msg])
        return MSG_ECU_List
    
    def _ECU_MSG_ID_List(self):
        MSG_ECU_ID_List = []
        for ecu in self._ECU_List():
            for msg in list(dict.fromkeys(self.SearchF("MSG", "ECU", ecu))):
                filter1 = self.ECU_LIST_GLOBAL_DF["MSG"]==msg
                msg_ID = self.ECU_LIST_GLOBAL_DF["msg_ID"].where(filter1).dropna().values[0]
                MSG_ECU_ID_List.append([ecu,msg, msg_ID])
        return MSG_ECU_ID_List
    
    
    ###############
    #ritorna la centralina corrispondente al messaggio
    def _ECU_MSG(self, MSG):
        try:
            searched = self.SearchF("ECU", "MSG", MSG)
            return searched[0]
        except:
            raise Exception('Probably the signal inserted is not in this database...')
    
    
    ###############
    #ritorna il range fisico
    def _RAN_F(self, Signal, Message = ""):
        try:
            _RAN = self.SearchF("Range", "Signal", Signal, "MSG", Message)
            _FACT = self.SearchF("Factor-Offset", "Signal", Signal, "MSG", Message)
            _INIT = self.SearchF("InitValue", "Signal", Signal, "MSG", Message)
            if _INIT == None:
                _INIT = 0
            _INIT_P = _INIT*_FACT[0][0]+_FACT[0][1]
            # print(_INIT_P,_INIT)
            # print(_FACT[0])
            R_min = (_RAN[0][0] - _FACT[0][1])/_FACT[0][0]
            R_max = (_RAN[0][1] - _FACT[0][1])/_FACT[0][0]
            return [_RAN[0][0], _RAN[0][1], _FACT[0][0], float(_INIT_P), _FACT[0][1], R_min, int(R_max)] #phis_min,phis_max,factor,init fisico, offset,minRAW,maRAW
        except:
            print(Signal,_RAN,_FACT,_INIT)
            raise Exception('Probably the signal inserted is not in this database...')
            return [0 for i in range(7)]
    
    ###############
    #ritorna CRC e MC se ci sono, altrimenti ritorna [] 
    def _R_CRC_MC(self, Message):
        try:
            _Signals_crc = self.SearchF("CRC", "MSG", Message)
            _Signals_mc = self.SearchF("MC", "MSG", Message)
            if sum(_Signals_crc) > 0:
                filter1 = self.ECU_LIST_GLOBAL_DF["CRC"]==1           
                filter2 = self.ECU_LIST_GLOBAL_DF["MSG"]==Message  
                CRC = (self.ECU_LIST_GLOBAL_DF["Signal"].where(filter1 & filter2).dropna().values)[0]
            if sum(_Signals_mc) > 0:
                filter1 = self.ECU_LIST_GLOBAL_DF["MC"]==1  
                filter2 = self.ECU_LIST_GLOBAL_DF["MSG"]==Message                      
                MC = (self.ECU_LIST_GLOBAL_DF["Signal"].where(filter1 & filter2).dropna().values)[0]
            return [CRC, MC]
            
        except: 
            # raise Exception('Probably the signal inserted is not in this database...')
            return []
    #da finire, non funziona
    
    
    def _isTable(self, signal):
        DES = self.SearchF("Numeric_value", "Signal", signal)
        LEN = self._RAN_F(signal)
        # print(LEN[6] - LEN[5])
        # print(len(DES[0]))
        try:
            if LEN[6] - LEN[5] > len(DES[0]) and len(DES[0]) < 3:
                return False
            else:
                return True
        except:
            #raise Exception("Description table = ", DES)
            return False
        
    
    def _isSNA(self,signal):
        try:
            val_descr = self.SearchF("Description", "Signal", signal)[0]
            val = self.SearchF("Numeric_value", "Signal", signal)[0]
            for i in range(len(val_descr)):
                if val_descr[i] == 'SNA':
                    return val[i]
            return []
        except:
            return []
    
    
    class ValError(Exception):
        pass           
                
    
    