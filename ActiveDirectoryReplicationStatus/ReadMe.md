Plugin to monitor Active Dorectory Replication status  Monitoring
===========

A plugin to monitor Active Directory replication's metadata for a set of one or more replication partner with data 
describing an Active Directory replication failure.

The following metrics are provided for this plugin:
### Active Directory Replication metadata metrics -
* InboundLastAttempt: The last inbound attempted.
* InboundLastAttemptPartner: The last inbound attempted by a partner.
* InboundLastSuccess: The last inbound succeeded.
* InboundLastSuccessPartner: The last inbound succeeded by a partner
* InboundLastResult: The last inbound resulted.
* OutboundLastAttempt: The last outbound attempted.
* OutboundLastAttemptPartner: The last outbound attempted by a partner.
* OutboundLastSuccess: The last outbound succeeded.
* OutboundLastSuccessPartner: The last outbound succeeded by a partner.
* OutboundLastResult: The last outbound resulted.

### Active Directory Replication failure metrics - 
* FailureCount: The number of failure count in Replication
* FailureType: The type of failure in Replication.
* FirstFailureTime: The time which first failure happened.
* LastError: The last error occurred in Replication.
* ErrorPartner: The Replication error which thrown for partner.
* ErrorServer: The Replication error which thrown for server.
