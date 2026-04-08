# GA Data and Messaging Platform Rollout

Helix GA depends on a resilient data and messaging layer that complements the observability rollout. This document groups the foundational work tracked in issues #146, #147, and #148 into a single execution plan.

## Capability Overview

| Capability            | Description                                                                         | Linked Issues                                          |
| --------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Redis Platform        | High-availability caching, session storage, and vector search via Redis Stack.      | [#146](https://github.com/Sinless777/Helix/issues/146) |
| CockroachDB Platform  | Globally resilient SQL backing Helix transactional workloads.                       | [#147](https://github.com/Sinless777/Helix/issues/147) |
| NATS Messaging Fabric | Lightweight publish/subscribe, request/reply, and JetStream persistence for events. | [#148](https://github.com/Sinless777/Helix/issues/148) |

## Delivery Waves

### Wave 1: Unified Data Control Plane

- Align persistent storage classes, TLS defaults, and secret rotation for Redis and CockroachDB.
- Stand up staging clusters with automated failover and backup validation.
- Integrate platform observability exporters to land metrics and logs in the GA telemetry stack.
- Reference issues: [#146](https://github.com/Sinless777/Helix/issues/146), [#147](https://github.com/Sinless777/Helix/issues/147)

### Wave 2: Messaging Fabric Enablement

- Deploy the NATS cluster with JetStream and baseline account permissions for Helix services.
- Validate messaging latency, persistence, and failover with synthetic workloads.
- Document migration steps from ad-hoc queues to the managed NATS service.
- Reference issue: [#148](https://github.com/Sinless777/Helix/issues/148)

## Cross-Cutting Checkpoints

- Secrets, certificates, and connection info delivered through `/libs/config` with rotation guidance.
- Runbooks for backup, restore, and failover recorded in `Docs/infra/` ahead of cutover.
- Platform SLO dashboards include Redis, CockroachDB, and NATS health before GA launch.
- Partnerships with application teams scheduled so consumers onboard as each wave exits.
