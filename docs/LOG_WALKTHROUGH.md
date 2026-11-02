# Understanding one recorded reading

These events come from the earlier fixed-rate experiment:
experiments/fixed-vs-adaptive/fixed-timebased-5s.txt

## Recorded events

    00:14.333 ID:3 BIN_TX BIN seq=0 fill=40 bytes=17
    00:14.359 ID:1 BIN_RX bytes=17 payload='BIN seq=0 fill=40' from fd00::203:3:3:3

Logging prefixes and whitespace are shortened here for readability.

## Interpretation

- At 14.333 simulated seconds, bin node 3 logs an application send.
- Its payload contains sequence number 0 and synthetic fill of 40%.
- The payload contains 17 bytes; this excludes the UDP header.
- At 14.359 seconds, gateway node 1 logs reception.
- In this controlled address scheme, the sender address identifies node 3.
- Match the reading by sender node ID and sequence number.

## Delay calculation

    Delay = receive time - send-log time
          = 14.359 - 14.333
          = 0.026 seconds
          = 26 milliseconds

This is application-log-to-application-log simulated delay.
It is not a measurement of radio propagation alone.

## Contribution to byte accounting

This reading has 17 application payload bytes.
Reconstructed UDP accounting adds an 8-byte UDP header:

    Application payload = 17 bytes
    UDP datagram accounting = 17 + 8 = 25 bytes

IPv6/MAC headers, routing messages, acknowledgements and retransmissions
are excluded from this accounting.

## Why this example is absent from the comparison table

The example occurs before 120 seconds. It explains the log format but is
excluded from the published measurement window.

The comparison selects transmissions at 120 <= t < 600 seconds and
allows their matching deliveries through 610 seconds. Data rates instead
use unique first receptions at 120 <= t < 600 seconds.

## Important distinctions

A BIN_TX entry does not prove delivery. A matching BIN_RX provides
reception evidence. A repeated sequence number from a different sender
is a different reading.

These application logs do not reveal every radio hop. Preferred-parent
snapshots also do not establish the exact path of an individual packet.
