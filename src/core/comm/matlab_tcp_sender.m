% === Configuration ===
ip = "127.0.0.1";   % RS_Pi IP
port = 5005;

% === Establish TCP Connnection ===
t = tcpclient(ip, port);

% === Test data ===
angle1 = [pi/2, pi/2, pi/2, pi/2, pi/2, pi/2];
angle2 = [0, pi/2, pi/2, pi/2, pi/2, pi/2];

% === Sending Format ===
msg1 = sprintf('%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n', angle1);
msg2 = sprintf('%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n', angle2);

write(t, msg1, "string");
fprintf("Sent: %s", msg1);
pause(1);  % Pause for 1s

write(t, msg2, "string");
fprintf("Sent: %s", msg2);

% === Close connection ===
clear t
