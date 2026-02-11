# Security Policy
Important to understand the client module of this application can be run on multiple computers in multiple locations uploading to a single server module of the application.
It is extremely important to maintain control of server user accounts and IP addresses the accounts can connect to the server from.

Information below is from link. Please visit for more information: https://dev.mysql.com/doc/refman/8.0/en/load-data-local-security.html

8.1.6 Security Considerations for LOAD DATA LOCAL
The LOAD DATA statement loads a data file into a table. The statement can load a file located on the server host, or, if the LOCAL keyword is specified, on the client host.

The LOCAL version of LOAD DATA has two potential security issues:

Because LOAD DATA LOCAL is an SQL statement, parsing occurs on the server side, and transfer of the file from the client host to the server host is initiated by the MySQL server, which tells the client the file named in the statement. In theory, a patched server could tell the client program to transfer a file of the server's choosing rather than the file named in the statement. Such a server could access any file on the client host to which the client user has read access. (A patched server could in fact reply with a file-transfer request to any statement, not just LOAD DATA LOCAL, so a more fundamental issue is that clients should not connect to untrusted servers.)

In a Web environment where the clients are connecting from a Web server, a user could use LOAD DATA LOCAL to read any files that the Web server process has read access to (assuming that a user could run any statement against the SQL server). In this environment, the client with respect to the MySQL server actually is the Web server, not a remote program being run by users who connect to the Web server.

To avoid connecting to untrusted servers, clients can establish a secure connection and verify the server identity by connecting using the --ssl-mode=VERIFY_IDENTITY option and the appropriate CA certificate. To implement this level of verification, you must first ensure that the CA certificate for the server is reliably available to the replica, otherwise availability issues will result. For more information, see Command Options for Encrypted Connections.

To avoid LOAD DATA issues, clients should avoid using LOCAL unless proper client-side precautions have been taken.

For control over local data loading, MySQL permits the capability to be enabled or disabled. In addition, as of MySQL 8.0.21, MySQL enables clients to restrict local data loading operations to files located in a designated directory.
