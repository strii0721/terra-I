from comm.tcp_agent import TcpAgent
from dk.logger.log4p import Log4P
from comm.enums.state_code import StateCode

logger = Log4P()
tcp_agent = TcpAgent()
logger.info(f"Waiting for connection on port {tcp_agent.port}")
address = tcp_agent.wait_connection()
logger.info(f"Connected established by {address}")

msg = tcp_agent.wait_state(StateCode.S_TRJ, 10)
# stat, msg = tcp_agent.receive()
logger.info(f"Received: {msg}")

tcp_agent.send(StateCode.C_COR, 
               "This message is send by Yahboom.")