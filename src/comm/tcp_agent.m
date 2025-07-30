ip = "192.168.137.45";
port = 5005;

t = tcpclient(ip, port);

control_variable_list = [0, pi/2, pi/2, pi/2, pi/2, pi/2];

for index = 0:1:180
    control_variable_list(1) = index;
    write(t, control_variable_list, "string");
    fprintf("Sent: %s", msg1);
    pause(0.1);  % Pause for 1s
end

write(t, msg1, "string");
fprintf("Sent: %s", msg1);
pause(0.1);  % Pause for 1s

write(t, msg2, "string");
fprintf("Sent: %s", msg2);

% === Close connection ===
clear t
