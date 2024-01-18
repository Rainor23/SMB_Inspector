
![logo](https://github.com/Rainor23/smb_inspector/assets/45594693/76ca4544-6037-4bba-870d-30862ad8ec03)

SMB Inspector!

 A very early version of SMB Inspector.


Disclaimer.
This tool should only be used on networks that you have authorisation to scan. It is illegal to scan networks without authorisation, and I will not be help responsible for your use of this tool.

This tool is still in active development and I would probably not recommend using it unless it is for a CTF.

Example Scan

![image](https://github.com/Rainor23/SMB_Inspector/assets/45594693/9cd1555d-60ef-46bb-9881-35a7b9cc3f97)

..............

![image](https://github.com/Rainor23/SMB_Inspector/assets/45594693/55d53e38-d962-4c63-8572-a07942128745)

Features:
Scan single IP's, host files or CIDR ranges.
Can search for interesting files based of extensions specified.
Can search for weak file permissions.


TODO:
Use Threads for Async tasks. e,g, each host has its own thread.
Refactor code to reduce the spaghetti and follow OOP.
Create formatted output that can be exported nicely to CSV for reporting tools.
Create filters such as -interesting which allows ONLY interesting files to be outputted.
Search for folder permissions.
