classdef TcpAgent

    properties
        ip
        port
        connection
        S_TRJ = 101   % Server send trajectory
        C_COR = 201   % Client send coordinate
    end

    methods
        function obj = TcpAgent(ip, port, connectionTimeout)
            obj.ip = ip;
            obj.port = port;
            if nargin < 3
                connectionTimeout = 10;
            end
            timeStart = tic;
            connected = false;
            while toc(timeStart) < connectionTimeout
                try
                    obj.connection = tcpclient(ip, port);
                    connected = true;
                    break;
                catch
                    fprintf("Target host cannot be reached. Reconnecting...\n")
                    pause(1);
                end
            end

            if ~connected
                error("Connection timeout");
            end
        end

        function [stat, msg] = receive(obj)
            header = read(obj.connection, 4, 'uint8');
            payloadLength = swapbytes(typecast(uint8(header), 'uint32'));
            payload = read(obj.connection, payloadLength, 'uint8');
            payloadJsonstr = char(payload);
            payloadStruct = jsondecode(payloadJsonstr);
            stat = payloadStruct.stat;
            msg = payloadStruct.msg;
            return;
        end

        function send(obj, stat, msg)
            payloadStruct = struct();
            payloadStruct.stat = stat;
            payloadStruct.msg = msg;
            payloadJsonstr = jsonencode(payloadStruct);
            payload = uint8(payloadJsonstr);
            payloadLength = length(payload);
            header = typecast(swapbytes(uint32(payloadLength)), 'uint8');
            write(obj.connection, header, "uint8")
            write(obj.connection, payload, "uint8")
        end

        function msg  = waitState(obj, targetState, timeout)
            if nargin < 3
                timeout = -1;
            end
            timeStart = tic;
            while true
                [stat, msg] = obj.receive();
                if isequal(stat, targetState)
                    return;
                end
                if timeout > 0 && toc(timeStart) > timeout
                    msg = [];
                    return;
                end
                pause(0.01);
            end
        end
    end
end