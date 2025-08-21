> Author: strii0721  
> Email: strii0721@outlook.com  

The source code section is mainly used for the validation work of the design in this project. The project root directory is the "terra-I" folder, and all relative path descriptions below are based on this root directory.All entry points of the functional code are located in the .py and .m files under the src directory.  
- **"dofbot_execute_stereo_capture.py"** is the code used for stereo camera image capture with the Yahboom DofBot.  
- **"dofbot_execute_tcp_ctrl.py"** is a script used to communicate with the host computer via the TCP protocol and control the behavior of the Yahboom DofBot according to the commands from the host.  
- **"simulator_execute.py"** is the entry point for launching the simulation tool mentioned in the paper. Its configuration files and the design files of the robotic arm are stored in the "src/simulation/saves" folder.  
- **"sv_dual_solution.py"** is a script for testing stereo vision with a binocular camera, which is used to obtain the 3D coordinates of a target from the left and right images captured by the camera. 
- **"test_tcp.py"** and **"TestTcp.m"** are scripts for testing synchronous communication between the host computer and the robotic arm, where the .m file needs to be executed in MATLAB. The purpose of this test is to achieve synchronization between the host and the robotic arm through status codes.  
- 
The other source code files under the src directory are specific functions that implement the related features, which will not be elaborated here.