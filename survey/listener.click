//tap :: KernelTun(192.168.10.1/24)
FromDevice($IN)
    -> Classifier(12/0800)
    -> CheckIPHeader(CHECKSUM false, OFFSET 14)
    -> IPClassifier(tcp dst port 90) // && tcp syn)
    // -> IPPrint()
    -> have_opt :: HasTCPOption;
    //IPClassifier(tcp timestamp, -);

elementclass Register { $value |
  [0]->ipc :: IPClassifier(tcp syn, -) -> Script(print >>/tmp/survey "$value") -> IPPrint($value) -> [0];
  ipc[1]->[0];
}


tap :: KernelTun(192.168.10.1/24);
end :: ToDump(/tmp/survey.pcap)
   // -> IPPrint(END)
    -> tap; // -> Discard;

t :: IPRewriter(pattern 192.168.10.2 - 192.168.10.1 9090 0 1, pattern 192.168.10.2 - 192.168.10.1 9091 0 1)


t[1] -> Queue
//-> IPPrint(RETURN)
    -> EtherEncap(SRC 8c:ec:4b:7f:af:14, DST 1c:e6:c7:53:f9:40, ETHERTYPE 0x0800) -> ToDevice($IN);
tap -> CheckIPHeader(OFFSET 0)
//-> IPPrint(TAPIN)
-> IPClassifier(tcp)
    //-> IPPrint()
    -> [1]t;


have_opt[0] -> Register(yes) -> [0]t -> end;
have_opt[1] -> Register(no) -> [1]t -> end;
