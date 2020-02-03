define( $PREFIX 192.168.20 )

//tap :: KernelTun($PREFIX.1/24)
FromDevice($IN)
    -> Classifier(12/0800)
    -> CheckIPHeader(CHECKSUM false, OFFSET 14)
    -> IPClassifier(tcp dst port 91) // && tcp syn)
    // -> IPPrint()
    -> have_opt :: HasTCPOption;
    //IPClassifier(tcp timestamp, -);

elementclass Register { $value |
  [0]->ipc :: IPClassifier(tcp syn, -) -> Script(print >>/tmp/survey "$value") -> IPPrint($value) -> [0];
  ipc[1]->[0];
}


tap :: KernelTun($PREFIX.1/24);
end :: ToDump(/tmp/survey.pcap)
   // -> IPPrint(END)
    -> tap; // -> Discard;

t :: IPRewriter(pattern $PREFIX.2 - $PREFIX.1 9090 0 1, pattern $PREFIX.2 - $PREFIX.1 9091 0 1)

t[1] -> Queue
//-> IPPrint(RETURN)
    -> EtherEncap(SRC 8c:ec:4b:7f:af:14, DST 1c:e6:c7:53:f9:40, ETHERTYPE 0x0800) -> ToDevice($IN);

tap -> CheckIPHeader(OFFSET 0)
    //-> IPPrint(TAPIN)
    -> IPClassifier(tcp)
    -> Print(BINSERTED,-1)
    -> InsertTCPOption(KIND 6, VALUE \<08091011>)
    -> SetIPChecksum
    -> SetTCPChecksum
    -> Print(AINSERTED,-1)
    //-> IPPrint()
    -> [1]t;


have_opt[0] -> Register(yes) -> [0]t -> end;
have_opt[1] -> Register(no) -> Print(RCV,-1) -> PrintTCPOption(KIND 7) -> [1]t -> end;
