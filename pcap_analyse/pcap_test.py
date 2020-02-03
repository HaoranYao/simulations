from scapy.all import *
import sys

def print_res(dic):
    with_opt = 0
    tot = 0
    for opts,nb in dic.items():
        tot += nb
        if "Timestamp" in opts:
            with_opt+= nb
    for opts,nb in sorted(dic.items(), key=lambda kv: -kv[1]):
        print(opts+' : '+str(100*float(nb)/tot)+'%' + ((' / '+str(100*float(nb)/with_opt)+'%') if ("Timestamp" in opts) else ""))
    print ('Percentage of TCP packet with options is '+str(100*float(with_opt)/tot)+'%')



def print_info():
    print ('-----------------------for SYN packet the layout for TCP options------------------------- ')
    print_res(syn_dic)
    print ('-----------------------for SYN-ACK packet the layout for TCP options is----------------------- ')
    print_res(synack_dic)
    print ('-----------------------for non-SYN packet the layout for TCP options is----------------------- ')
    print_res(other_dic)

files = sys.argv[1:]
temp_count = 0
tcp_count = 0
tsval_count = 0
syn_dic = {}
synack_dic = {}
other_dic = {}
for file_name in files:
  for each_packet in PcapReader(str(file_name)):
    if 'TCP' in each_packet:
        tcp_count += 1
        # s = (repr(each_packet))
        # print (s)
        if each_packet['TCP'].flags=='S':
            # print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            string = ' '
            for field in each_packet['TCP'].options:
                string=string+str(field[0])+' '
            if string in syn_dic.keys():
                syn_dic[string]+=1
            else:
                syn_dic[string]=1
            # print (each_packet['TCP'].options)
            # if tcp_count == 50:
            #     break
        elif each_packet['TCP'].flags=='SA':
            # print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

            string = ' '
            for field in each_packet['TCP'].options:
                string=string+str(field[0])+' '
            if string in synack_dic.keys():
                synack_dic[string]+=1
            else:
                synack_dic[string]=1
            # print (each_packet['TCP'].options)
            # if tcp_count == 50:
            #     break
        else:
            string = ' '
            for field in each_packet['TCP'].options:
                string = string + str(field[0]) + ' '
            if string in other_dic.keys():
                other_dic[string] += 1
            else:
                other_dic[string] = 1
            # print (each_packet['TCP'].options)
            # if tcp_count == 50:
            #     break
        if tcp_count%20000 == 0:
            print_info()
        #if tcp_count > 1000000:
        #    break
print_info()


