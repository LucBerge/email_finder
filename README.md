# Project Setup and Usage

## Prerequisits

- Install python
- **A network provider that allows outbound connections on port 25.** Email verification relies on direct SMTP (MTA-to-MTA) connections to recipient mail servers on port 25. Most residential ISPs (e.g. SFR, Orange) and cloud providers (AWS, GCP, Azure, OVH...) block outbound port 25 by default, which causes connection timeouts. Run this code from a network (or VPS) where outbound port 25 is open. You can check connectivity with:

  ```sh
  python -c "import socket; socket.create_connection(('gmail-smtp-in.l.google.com', 25), 10); print('port 25 OPEN')"
  ```

|  | Windows | Linux & Mac |
|---|---|---|
| **Setup** | Run `scripts/setup.bat` | Run `scripts/setup.sh` |
| **Run** | Run `scripts/run.bat` | Run `scripts/run.sh` |
