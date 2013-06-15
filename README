Overlord Network Monitoring Framework
============================

Overlord is a network monitoring framework designed to benchmark and return an overview of all network in the nodes. Their are 3 components in the framework.

- Server: Control the monitoring process. Provide data interface and data storage.
- Web: Data display interface
- Agent: Agent  

The server and agent communicate with HTTP protocol. Once the server had been initialzed. It will listen for the agent which will connected to the method '/listen'. The server read data send from the agent and record the results and update scheduling status.  The server then return the monitor job that need to be run back to the agent to perform the task. The agent recieve the tasks and do the benchmark work and return the result to the server and so on.

Web components works seperately from the server. Its access monitoring data via database

Requirement
=============
The target host will need Python runtime to run the components. These components had been develop and test on Ubuntu but should work on others Linux as well with the following requirments for each components.

- Server: bottle framework, 
- Agent:
- Web: bottle framework, 


Server Installation
==============
config files


Web Installation 
============
config files

Agent Installation
==========

Agent node need ping and Iperf installed.
config files


Working Details
==========

Scheduling mechanism can be selected from the 3 of following:
1. Random -
2. Time Table -
3. Idle Host -

