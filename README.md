# COEN366_Project_CENRS
CENRS - design and implement an application-layer communication protocol using both UDP and TCP. The system simulates an emergency notification service for a university campus. Typical incidents include fire alarms, security incidents, severe weather, power outages, building closures, and other urgent campus situations.


Person A(Pawan): Server core (UDP) and reliability

UDP receive loop, thread pool, and message dispatch
REGISTER/DE-REGISTER, SUBSCRIBE/UNSUBSCRIBE, and validation and error replies
PUBLISH_ALERT, UPDATE_ALERT, and CLOSE_ALERT handling, including subscription matching with the ALL wildcards
The retransmission engine: a pending-ACK table, a timer thread, 3 attempts, then UNCONFIRMED, plus the packet-loss simulation flag

Person B(Matthew): Persistence, recovery, and server TCP

The SQLite schema and data access layer, shared with Person A, so agree on the interface early
Persisting users, subscriptions, incidents (version and status), attachment metadata, status reports, and the Incident_ID counter
Crash recovery and re-registration after a restart
The TCP server for GET_ACTIVE_ALERTS and ACTIVE_ALERTS, with its record encoding
STATUS_REPORT handling on the server side

Person C(Hala): Client (subscriber side)

The client UDP listener and command-line interface
Registration, subscribing, and status reports
Duplicate detection with (Incident_ID, Version) and re-ACKing duplicates
The ATTACH_REQ flow, and the TCP download client with checksum verification and ATTACH_OK/ATTACH_ERROR
The client side of GET_ACTIVE_ALERTS sync on reconnect

Person D(Larry): Publisher side and the P2P file server

Client publisher commands: publish, update, and close
The TCP listener thread that spawns a thread per download, serves GET_ATTACHMENT, and sends the header, then the exact bytes, then the checksum
ATTACH_REQ/ATTACH_INFO/ATTACH_DENIED handling on the server (coordinate with Person A)
Error cases: file missing, publisher gone, transfer cut short, bad checksum

Shared, assigned by name

Protocol spec doc (message formats, encoding, error codes): everyone drafts it, and one person (I’d say Person A) owns the final version. Do this first, before anyone codes.
Logging module: Person A writes a tiny shared one, and everyone uses it.
Test scripts and failure demos: each person writes tests for their own slice. For example, B kills and restarts the server, C and D run concurrent downloads, and A demonstrates packet loss.
Report: each person writes the sections matching their component, plus their own line in the contributions section. One person does final assembly and editing.
