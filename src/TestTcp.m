addpath("./comm/");
tcpAgent = TcpAgent("127.0.0.1", 5005);
msg = "This message is send by MATLAB.";
fprintf("Sent: %s\n", msg);
tcpAgent.send(tcpAgent.S_TRJ, msg);
msg = tcpAgent.waitState(tcpAgent.C_COR);
fprintf("Received: %s\n", msg);