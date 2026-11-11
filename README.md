# CENRS: Campus Emergency Notification and Response System

**COEN 366: Communication Networks and Protocols, Fall 2026, Concordia University**

An application-layer emergency notification protocol built on **UDP** (control and real-time alerts) and **TCP** (reliable data transfer), with a central Emergency Server and peer-to-peer attachment transfer between clients.

---

## Table of Contents

- [Team](#team)
- [System Overview](#system-overview)
- [Task Breakdown](#task-breakdown)
- [Shared Responsibilities](#shared-responsibilities)
- [Development Phases](#development-phases)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Team Workflow](#team-workflow)
- [Deliverables Checklist](#deliverables-checklist)

---

## Team

| Member | Role | Component Owned |
|--------|------|-----------------|
| _Name A (Pawan)_ | Server Core and Reliability | UDP server, alert handling, retransmission engine |
| _Name B (Matthew)_ | Persistence and Recovery | Database, crash recovery, server TCP sync |
| _Name C (Hala)_ | Client (Subscriber) | Client UDP, duplicate detection, attachment download |
| _Name D (Larry)_ | Publisher and P2P | Publisher commands, TCP file server, attachment discovery |

---

## System Overview

```
                 ┌─────────────────────┐
                 │  Emergency Server   │
                 │    UDP  │  TCP      │
                 └─────────────────────┘
                   ▲        ▲        ▲
        UDP / TCP  │        │        │  UDP / TCP
          ┌────────┘        │        └────────┐
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  Subscriber  │  │  Publisher   │  │     BOTH     │
   └──────────────┘  └──────┬───────┘  └──────────────┘
          ▲                 │ TCP (direct file transfer)
          └─────────────────┘
```

| Transport | Used for |
|-----------|----------|
| **UDP** | Registration, subscriptions, alerts, ACKs, updates, ALL_CLEAR, status reports, attachment discovery |
| **TCP** | Peer-to-peer attachment transfer, active-incident synchronization |

**Key requirements:** application-level reliability for CRITICAL alerts (ACK, timeout, up to 3 attempts, then `UNCONFIRMED`), duplicate detection, multi-threaded server and clients, persistent server state, and application-level file checksums.

---

## Task Breakdown

### Member A (Pawan): Server Core (UDP) and Reliability

- [ ] UDP receive loop, thread pool, and message dispatcher
- [ ] `REGISTER` / `DE-REGISTER` with validation and error replies
- [ ] `SUBSCRIBE` / `UNSUBSCRIBE` and subscription matching (including `ALL` wildcards)
- [ ] `PUBLISH_ALERT`, `UPDATE_ALERT`, `CLOSE_ALERT` handling
- [ ] Alert distribution (`ALERT`, `ALERT_UPDATE`, `ALL_CLEAR`)
- [ ] Retransmission engine: pending-ACK table, timer thread, 3 attempts, `UNCONFIRMED`
- [ ] Packet-loss simulation flag for demos
- [ ] Owns the final protocol spec document

### Member B (Matthew): Persistence, Recovery, and Server TCP

- [ ] Database schema and data access layer (agreed with Member A)
- [ ] Persist users, subscriptions, incidents (version and status), attachment metadata, status reports, and the Incident_ID counter
- [ ] Crash recovery and re-registration after server restart
- [ ] TCP server for `GET_ACTIVE_ALERTS` / `ACTIVE_ALERTS` and its record encoding
- [ ] `STATUS_REPORT` handling (`STATUS_RECORDED` / `STATUS_REJECTED`)

### Member C (Hala): Client (Subscriber Side)

- [ ] Client UDP listener thread and command-line interface
- [ ] Registration, subscription, and status-report commands
- [ ] Duplicate detection using `(Incident_ID, Version)`, re-ACK without re-displaying
- [ ] `ATTACH_REQ` flow and TCP download client
- [ ] Checksum verification, `ATTACH_OK` / `ATTACH_ERROR`
- [ ] Client side of `GET_ACTIVE_ALERTS` sync on reconnect

### Member D (Larry): Publisher Side and P2P File Server

- [ ] Publisher commands: publish, update, close
- [ ] TCP listener with one thread per download, serving `GET_ATTACHMENT`
- [ ] `ATTACH_DATA` header, exact `File_Size` bytes, checksum
- [ ] Server-side `ATTACH_REQ` / `ATTACH_INFO` / `ATTACH_DENIED` (coordinate with Member A)
- [ ] Error cases: missing file, publisher unavailable, truncated transfer, bad checksum

---

## Shared Responsibilities

| Item | Owner | Notes |
|------|-------|-------|
| Protocol spec (formats, encoding, error codes) | Everyone drafts, **A** finalizes | Freeze before coding |
| Logging module | **A** writes, all use | Every message sent, received, and failed must be visible |
| Test scripts and failure demos | Each member, for their own slice | See below |
| Report assembly and editing | _TBD_ | Each member writes their own sections |
| Contributions section of report | Everyone | One entry per member |

**Suggested demo and test scenarios**

| Scenario | Lead |
|----------|------|
| Packet loss, retransmission, `UNCONFIRMED` | A |
| Server kill and restart, state recovery | B |
| Duplicate `ALERT` / `ALL_CLEAR` handling | C |
| Concurrent attachment downloads | C and D |
| Publisher offline, corrupted or truncated file | D |

---

## Development Phases

| Phase | Target | Scope |
|-------|--------|-------|
| **1** | Late October | Registration, subscription, basic persistence, logging |
| **2** | Mid-November | Publish, alert, ACK, update, close, ALL_CLEAR, status, timers, retransmission, duplicates, concurrency |
| **3** | Late November | P2P attachments, checksums, `GET_ACTIVE_ALERTS`, recovery, error handling, integrated testing |
| **Final** | Week 13 | Report and demonstration |

---

## Repository Structure

> Adjust to match your chosen language.

```
.
├── README.md
├── docs/
│   ├── protocol_spec.md       # Message formats and encoding
│   └── report/                # Report sources
├── server/
│   ├── main
│   ├── udp_handler
│   ├── tcp_handler
│   ├── reliability            # ACK timers and retransmission
│   └── db                     # Persistence layer
├── client/
│   ├── main
│   ├── udp_listener
│   ├── tcp_file_server        # Publisher side
│   └── tcp_downloader         # Subscriber side
├── common/
│   ├── messages               # Encode and decode
│   └── logger
└── tests/
```

---

## Getting Started

_Fill in once the implementation language is chosen._

```bash
# Start the server
<command>

# Start a client
<command> --name Alice --role SUBSCRIBER --udp 5001 --tcp 6001
```

---

## Team Workflow

- **Freeze message formats and DB interfaces in the first meeting.** Most integration problems come from mismatched formats.
- **Use short-lived feature branches** and open a pull request for each merge. At least one teammate reviews it.
- **Integrate weekly** instead of merging everything near the demo.
- **Write the report as you go**: assumptions, design justifications, and test results.
- **Rehearse the demo** with members rotating who explains which part. Everyone must be able to answer questions on any component.

---

## Deliverables Checklist

- [ ] Client and server implementation (UDP and TCP, multi-threaded)
- [ ] Persistent server state with crash recovery
- [ ] Communication logging (screen or log file)
- [ ] Project report covering:
  - [ ] Assumptions and error-handling decisions
  - [ ] Message encoding and parsing
  - [ ] TCP message and file boundary handling
  - [ ] RQ# and Incident_ID generation
  - [ ] Concurrency design (server and publisher peers)
  - [ ] UDP timers, retransmission, and duplicate detection
  - [ ] Checksum choice and justification
  - [ ] Persistence and recovery
  - [ ] Testing and experimental observations
  - [ ] Code structure
  - [ ] Individual contributions of each member
- [ ] Demonstration (Week 13), all members present
