#!/usr/bin/env python 3.10
import sys
import numpy as np


def gen_key(old_key_path, new_key_path, True_):

  #read just 1st line of the file = subkey
  if True_:
    def split_8(filename):
        with open(filename, "r") as file:
            content = file.readline().strip()
            return [content[i:i+8] for i in range(0, len(content), 8)]
    list_of_8_chars = split_8(old_key_path)

  #read the key that we generated in last step  
  if not True_:
      text = old_key_path
      list_of_8_chars = [text[i:i+8] for i in range(0, len(text), 8)]
      
  #asign value
  w0 = list_of_8_chars[0]
  w1 = list_of_8_chars[1]
  w2 = list_of_8_chars[2]
  w3 = list_of_8_chars[3]

#shifting =================================================================================
#Shift w3 to left with 1 byte —> 
#w3 after shifting
  w3_ = w3[2:] + w3[0:2]

#Subbytes ==================================================================================
  sbox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
          ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
          ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
          ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
          ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
          ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
          ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
          ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
          ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
          ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
          ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
          ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
          ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
          ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
          ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
          ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
  # the index of the rows & colums
  def find_index(number):
    frame = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    index = frame.index(number)
    return index
  #use sbox and go by 2 chrecter the 1st chr is for row# and 2end cher for clum# 
  one_ = 0
  two_ = 1
  Subbytes = ''    
  for i in range(4):
       one = find_index(w3_[one_])
       two = find_index(w3_[two_])
       Subbytes += sbox[one][two]
       one_ = one_ + 2
       two_ = two_ + 2

# XOR round constant 01, 00, 00, 00 ==========================================================================
  if True_: # for 1st key
   round_constant = '01000000'
  if not True_: # for 2ed key
   round_constant = '02000000'

   #convert binary to hex
  def bin_hex(value1):
    bstr1 = str(value1)
    hstr1 = '%0*X' % ((len(bstr1) + 3) // 4, int(bstr1, 2))
    return(hstr1)

  #convert hex to binary
  def hex_to_binary(value1, value2):
    cc = '' 
    my_hexdata1 = value1
    a = bin(int(my_hexdata1, 16))[2:].zfill(8)
    my_hexdata2 = value2
    b = bin(int(my_hexdata2, 16))[2:].zfill(8)
    for i in range(len(a)):
      aa = int(a[i])
      bb = int(b[i])
      cc += str((aa^bb))
      dd = bin_hex(cc)
    return dd[1:]
    
  # caleculate g(w3)
  g_w3 = ''
  for i in range(len(Subbytes)):
    g_w3 += hex_to_binary(round_constant[i], Subbytes[i]).lower()
   
#w4 = w0 + g(w3) ========================================
  w4 = ''
  for i in range(len(w0)):
    w4 += hex_to_binary(w0[i], g_w3[i]).lower()  
  if True_:
    print("w4 = :", w4)

#w5 = w4 + w1  ========================================
  w5 = ''
  for i in range(len(w0)):
    w5 += hex_to_binary(w4[i], w1[i]).lower()
  if True_:  
    print("w5 = :", w5)

#w6 = w5 + w2 ========================================
  w6 = ''
  for i in range(len(w0)):
    w6 += hex_to_binary(w5[i], w2[i]).lower()  
  if True_:
     print("w6 = :", w6)

#w7 = w6 + w3  ========================================
  w7 = ''
  for i in range(len(w0)):
    w7 += hex_to_binary(w6[i], w3[i]).lower()   
  if True_:
     print("w7 = :", w7)

   
#• Subkey1 --> w4 + w5 + w6 + w7:
  Subkey1_ = ''
  Subkey1_ += w4+w5+w6+w7
  print()
  
  #empity the contain of the file
  if True_:         
    with open(new_key_path, "w") as file:
          file.write("")
          
  #write into the file and keep it open         
  with open(new_key_path, "a") as file:
         file.write(Subkey1_)
         file.write('\n')
         file.close()  
   #orginize the outputs in the tremenal  
  if True_:
    print("Subkey0 ->", Subkey1_)
    print()
  else:
      print("Subkey1 ->", Subkey1_)
  
  #call the function again to generate  Subkey1   
  if True_:
    gen_key(Subkey1_, new_key_path, False)
    

#======================================================
def aes_algorithm(plaintext, subkey_example, results_):

  #convert 1D array to 2D array
  def arrTo2Darr_print(oneD_Darry):
    rows, cols = (4, 4)
    two_Darry  = [[i for i in range(cols)] for j in range(rows)]
    value = 0
    for i in range(rows):
      for j in range(cols):
         two_Darry[j][i] = oneD_Darry[value]
         value += 1
       
    for i in range(rows):
      for j in range(cols):
         print(two_Darry[i][j], end = ' ')
      print()
    return two_Darry

  #to read the keys
  def get_key(file_name, key_number):
    my_file = open(file_name, "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    key = []
    one = 0
    end = 2
    for x in range(16):
      key.append(data_into_list[key_number][one:end])
      end += 2
      one += 2
    return key
  
  #open file to read plaintext
  f = open(plaintext,'r')
  p_text = f.read()
  f.close()

  print("The plaintext :", p_text)

  Initial_State_1D = []
  for i in range(len(p_text)):
    string = p_text[i].encode('ASCII')
    s = string.hex()
    Initial_State_1D.append(s)
  

#dispaly 1D array into 2D array
  def arrTo2Darr_print(oneD_Darry):
    rows, cols = (4, 4)
    two_Darry  = [[i for i in range(cols)] for j in range(rows)]
    value = 0
    for i in range(rows):
      for j in range(cols):
         two_Darry[j][i] = oneD_Darry[value]
         value += 1
       
    for i in range(rows):
      for j in range(cols):
         print(two_Darry[i][j], end = ' ')
      print()
    return two_Darry
#convert 1D to 2D 
  def arrTo2Darr_print2(oneD_Darry):
    rows, cols = (4, 4)
    two_Darry  = [[i for i in range(cols)] for j in range(rows)]
    value = 0
    for i in range(rows):
      for j in range(cols):
         two_Darry[i][j] = oneD_Darry[value]
         value += 1
       
    for i in range(rows):
      for j in range(cols):
         print(two_Darry[i][j], end = ' ')
      print()
    return two_Darry
  
       
#print Initial_State
  print('• The Initial_State :')
  Initial_State = arrTo2Darr_print(Initial_State_1D)
  print()


#get key#0 and print it
  print('• The Subkey0 :')
  Subkey0 = arrTo2Darr_print(get_key(subkey_example, 0))
  print()

  #convert bin to hex
  def bin_hex(value1):
    bstr1 = str(value1)
    hstr1 = '%0*X' % ((len(bstr1) + 3) // 4, int(bstr1, 2))
    return(hstr1)

  #convert hex to bin
  def hex_to_binary(value1, value2):
    cc = '' 
    my_hexdata1 = value1
    a = bin(int(my_hexdata1, 16))[2:].zfill(8)
    my_hexdata2 = value2
    b = bin(int(my_hexdata2, 16))[2:].zfill(8)
    for i in range(len(a)):
      aa = int(a[i])
      bb = int(b[i])
      cc += str((aa^bb))
      dd = bin_hex(cc)
    return dd


  #the caleculation to generate Current_State_after_AddKey
  rows, cols = (4, 4)
  AddKey = []
  for i in range(cols):
    for j in range(rows):
      y = hex_to_binary(Initial_State[j][i], str(Subkey0[j][i]))
      AddKey.append(y.lower())
    
  print('• Current State (after AddKey with Subkey0): ')
  Current_State_after_AddKey = arrTo2Darr_print(AddKey)
  print()

#SubBytes ==========================================================================================

  sbox = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
        ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
        ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
        ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
        ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
        ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
        ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
        ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
        ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
        ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
        ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
        ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
        ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
        ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
        ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
        ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]


  def find_index(number):
    frame = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    index = frame.index(number)
    return index

  Current_State_after_Round_1_SubBytes = []
  for i in range(rows):
    for j in range(cols):
       value = Current_State_after_AddKey[j][i]
       one = find_index(value[0])
       two = find_index(value[1])
       Current_State_after_Round_1_SubBytes.append(sbox[one][two])

    
  print('• Current State (after Round 1 SubBytes):')
  Current_State_after_SubBytes = arrTo2Darr_print(Current_State_after_Round_1_SubBytes)
  print()

#shifting ==========================================================================================
# Importing Numpy module
  import numpy as np

#function to call the order
  def the_order(value_):
      if value_ == 0:
        myorder_0 = [0, 1, 2, 3]
        return myorder_0
      if value_ == 1:
        myorder_1 = [1, 2, 3, 0]
        return myorder_1 
      if value_ == 2:
        myorder_2 = [2, 3, 0, 1]
        return myorder_2 
      if value_ == 3:
        myorder_3 = [3, 0, 1, 2]
        return myorder_3 


  arr = np.array(Current_State_after_SubBytes)
# Access row of array
  counter= 0
  ShiftRows = []
  for x in range(4):
      myorder = the_order(counter)
      res_arr = arr[x]
      mylist = [res_arr[i] for i in myorder]
      for j in range (4):
         ShiftRows.append(mylist[j])
      counter +=1

  print('• Current State (after Round 1 ShiftRows): ')
  Current_State_after_ShiftRows = arrTo2Darr_print2(ShiftRows)

#MixColumn ==========================================================================================

  def mixColumns1(a, b, c, d , mixColumns_output):
      printHex(gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1), mixColumns_output)
      printHex(gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1), mixColumns_output)
      printHex(gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3), mixColumns_output)
      printHex(gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2), mixColumns_output)
      print()

  def gmul(a, b):
      if b == 1:
          return a
      tmp = (a << 1) & 0xff
      if b == 2:
          return tmp if a < 128 else tmp ^ 0x1b
      if b == 3:
          return gmul(a, 2) ^ a

  def printHex(val, mixColumns_output):
      return mixColumns_output.append('{:02x}'.format(val))

 #caleculate MixColumn 
  rows,cols = (4,4)
  mixColumns_output = []
  for i in range(rows):
    colum = []
    for j in range(cols):
       element_as_int = int(Current_State_after_ShiftRows[j][i], base=16)
       colum.append(element_as_int)
    mixColumns1(colum[0], colum[1], colum[2], colum[3], mixColumns_output)

  print('• Current State (after Round 1 MixColumn):')
  Current_State_after_MixColumn = arrTo2Darr_print(mixColumns_output)
  print()

#MixColumn ==========================================================================================

#get key#0 and print it
  print('• The Subkey1 : ----------------------------------->')
  Subkey1 = arrTo2Darr_print(get_key(subkey_example, 1))
  print()

  
  rows, cols = (4, 4)
  AddKey = []
  for i in range(cols):
    for j in range(rows):
      y = hex_to_binary(Current_State_after_MixColumn[j][i], str(Subkey1[j][i]))
      AddKey.append(y.lower())
      
  #print the Current_State_after_AddKey_1  
  print('• Current State (after Round 1 AddKey 1):')
  Current_State_after_AddKey_1 = arrTo2Darr_print(AddKey)
  print()

  #this is just for printing the data into file
  rows, cols = (4, 4)
  AddKey = []
  for i in range(cols):
    for j in range(rows):
      y = hex_to_binary(Current_State_after_MixColumn[i][j], str(Subkey1[i][j]))
      AddKey.append(y.lower())
      
    
#• The output from round 1 AES 
  rows, cols = (4, 4)
  AddKey = []
  AddKey.append("0x")
  for i in range(cols):
    for j in range(rows):
      y = hex_to_binary(Current_State_after_MixColumn[j][i], str(Subkey1[j][i]))
      AddKey.append(y.lower())
  AddKey__ = ''  
  
  
  print("• The output from round 1 AES :\n")   
  for x in AddKey:
      AddKey__ += x
      print(x, end = '')    
      
  #Write into file      
  with open(results_, "w") as file:
          file.write(AddKey__)

      
#fetching data ========================================================================================


if sys.argv[1] == 'gen_key':
  old_key_path = sys.argv[2]
  new_key_path = sys.argv[3]
  gen_key(old_key_path, new_key_path, True)


if sys.argv[1] == 'aes':
  plaintext = sys.argv[2]
  subkey_example = sys.argv[3]
  results_ = sys.argv[4]
  aes_algorithm(plaintext, subkey_example, results_)
  













