# emma-business — Long-Horizon Backlog

**This file is the project's horizon, not its worklist.** Items here are *abstract
destinations* — where the product is going. They are not executable. When one is ready to
be worked, it gets pulled out, decomposed into concrete steps in `queue.md`, executed, and
deleted from both. Nothing is ever ticked off in place; finished work is a dated entry in
`devlog.md`.

Derived from Emma's description of the product on 2026-08-21. Where an item rests on an
assumption rather than something she said, the assumption is named so it can be corrected
instead of silently inherited.

---

## 1. Deployment and control plane

The customer runs the system. Either it is installed inside their own perimeter, or it runs
on our cloud service with enough control surfaced that "sovereign" is still true. Both paths
have to be real products, and the on-premise path is the harder constraint, so it sets the
architecture.

- A deployment artifact a customer's own operations team can install, upgrade and roll back
  without us in the loop.
- An air-gapped install path: no licence call-home, no telemetry requirement, no model or
  dependency fetch at runtime.
- A control surface that makes the customer's authority concrete — what runs, on what data,
  under what policy, with what retention, and who inside their org may change it.
- The managed-cloud variant of the same control surface, where the difference from
  on-premise is who operates the hardware and nothing else that matters.
- Upgrade without breaking replay: a run recorded under an old version must stay
  reproducible after the system is upgraded.

_Assumption: on-premise and managed cloud are one product with two deployment modes, not two
codebases. If they are meant to diverge, this item splits._

## 2. Audit and reproducibility substrate

The evidence layer. This is the core product claim, so it is infrastructure that everything
else is built on, not a reporting feature bolted to the side.

- A run record that captures inputs, versions, seeds, model identities, retrieved context,
  intermediate reasoning steps and outputs, written where the customer controls it.
- Determinism where determinism is achievable, and an explicit, recorded account of the
  residual non-determinism where it is not — including what sampling and hardware contribute.
- Replay: re-execute a past run from its record and get the same result, or a precise
  account of what changed and why.
- Tamper-evidence, so an audit record is worth something to the customer's own auditors and
  regulators, not just to their engineers.
- Retention, export and deletion under the customer's policy rather than ours.

## 3. Neuro-symbolic reasoning core

The part that makes the audit trail meaningful. If the reasoning is an opaque forward pass,
the record can only ever say what went in and what came out.

- A representation in which the reasoning steps are structures that can be named, stored and
  checked, not just tokens.
- A working division of labour between the neural and symbolic components, and evidence for
  where the boundary belongs rather than an aesthetic preference.
- Verification of symbolic steps, so a claimed chain of reasoning can be checked
  independently of the model that produced it.
- Failure behaviour: what the system does when the symbolic layer cannot justify what the
  neural layer proposes.

## 4. Interpretability surface

In scope as part of auditability — what a customer's own reviewer sees when they ask why an
output came out the way it did.

- Attribution from an output back to the specific inputs, retrieved context and reasoning
  steps that produced it.
- Explanations tied to the recorded run rather than regenerated after the fact, so the
  explanation cannot drift from what actually happened.
- A reviewer-facing view for people who are not engineers, since the audience for an audit
  is compliance and risk as much as it is engineering.

## 5. Enterprise readiness

The things that decide whether an enterprise can actually buy and run it, independent of how
good the reasoning is.

- Identity, access control and multi-tenancy inside a single customer's deployment.
- Security posture and the evidence for it, in the form procurement will ask for.
- Mapping the audit and reproducibility story onto the regimes customers are actually held
  to, once we know which ones they are.
- Operability: observability, capacity planning, failure modes and support boundaries for a
  system we may not be able to see.
- Documentation an outside operations team can run the product from.

_Assumption: the target regimes are unknown. Naming them changes what "audit-ready" means
concretely, and is worth pinning down early._

## 6. Commercial track

Non-code work that this repo still needs to carry, because it constrains the product.

- Who the first customers are, concretely enough to test the product against them.
- Pricing and packaging across on-premise and managed cloud, including how a customer who
  can run it entirely air-gapped is metered.
- Where the boundary sits between what is open and what is proprietary.
- Licensing and IP posture, especially for any third-party models or datasets that end up
  inside a customer's perimeter.
- A design-partner path: the shortest route to a real deployment that produces real feedback.

---

## Pointers

- Concrete in-scope steps: `queue.md`.
- Completed work, chronological: `devlog.md`.
- Project identity and constraints: `CLAUDE.md`, `README.md`.
