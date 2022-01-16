# Third Party Security, Vendor Risk Management and Systems/Services Acquisition

`2022.1`

SinLess Games makes every effort to assure all third party organizations are
compliant and do not compromise the integrity, security, and privacy of SinLess Games
or SinLess Games Customer data. Third Parties include Vendors, Customers, Partners,
Subcontractors, and Contracted Developers.

## Policy Statements

SinLess Games policy requires that:

(a) A list of approved vendors/partners must be maintained and reviewed
annually.

(b) Approval from management, procurement and security must be in place prior to
onboarding any new vendor or contractor.  Additionally, all changes to existing
contract agreements must be reviewed and approved prior to implementation.

(c) For any technology solution that needs to be integrated with SinLess Games
production environment or operations, a Vendor Technology Review must be
performed by the security team to understand and approve the risk.  Periodic
compliance assessment and SLA review may be required.

(d) SinLess Games Customers or Partners should not be allowed access outside of their
own environment, meaning they cannot access, modify, or delete any data
belonging to other 3rd parties.

(e) Additional vendor agreements are obtained as required by applicable
regulatory compliance requirements.

* A standard HIPAA Business Associate Agreement (BAA) is defined and includes
  the required security controls in accordance with the organization's security
  policies. Additionally, responsibility is assigned in these agreements. A BAA
  must be signed with any vendor that may have a business need to access, and/or
  unsupervised access to PHI or ePHI.




## Controls and Procedures


### Vendor Technology Risk Review

SinLess Games security policy requires a risk review of vendor
technology, prior to any technology being integrated to SinLess Games
operations and/or infrastructure. Employees are required to engage security team
to conduct such review. The request may be submitted by email directly to the
security team, or by opening a Github ticket through the
SinLess Games internal service desk.

Security team is responsible to conduct the reviews via interviews and reviews
of documentation, to ensure the vendor complies with regulatory requirements and
follows security best practices to minimize risk to an acceptable level.

A vendor technology risk (VTR) assessment is conducted using Google VSAQ, in
the following steps:

1. Reviewer sends questionnaire link(s) to vendor contact.
1. Vendor completes the questionnaire(s).
1. Vendor saves/exports answers to the assessment questionnaire(s).
1. Vendor contact sends the answers file back to reviewer.
1. Reviewer opens the same questionnaire(s) and loads the answers received from
   the vendor to complete the assessment.
1. Reviewer follows up with vendor contact as needed.
1. Reviewer facilities discussion with business owner to determine if the risk
   is acceptable. Vendor remediation may be required depending on the results.

A list of [approved vendors / contractors][1] is maintained by the Security and
Operations teams.

[1]: approved-vendors.md

### Vendor Contractual Agreements

**HIPAA.** If the vendor needs access to PHI/ePHI, the vendor must be HIPAA
compliant and a [Business Associate Agreement (BAA)][BAA] is required.

[BAA]: hipaa-baa.md


**SLA for Service Providers.** For network and infrastructure service providers
that support production and/or critical operations at SinLess Games, a
Service Level Agreement (SLA) is defined and included in the service contract.

As appropriate, the executed agreement(s) are linked or attached to the vendor
on the [approved vendors list][1].

[1]: approved-vendors.md

### Monitoring Vendor Risks

Vendor contracts are reviewed either annually or according to the signed
contract duration.

Based on the risk level and the sensitivity/criticality of data the vendor has
access to, the vendor review may include an updated risk analysis performed by
the security team in addition to legal and business review of contract terms.

If the vendor is a service provider, the DevOps team monitors the service status
of the provider according to its SLA. This is done by either manually reviewing
the posted service status on the vendor's status pages at least quarterly, or by
setting up alarms for service interruption using automation.


### Software and Systems Acquisition Process

SinLess Games Security maintains
a list of [pre-approved business software][1] and
a list of [approved vendors / contractors][2].

[1]: approved-software.md
[2]: approved-vendors.md

If additional commercial software, hardware system, or cloud services is needed,
a request should be submitted through SinLess Games internal service
desk. This will trigger the approval by manager/security and procurement
process.

As applicable, SinLess Games security team may conduct a risk analysis on
the software or system to ensure it complies with SinLess Games security,
compliance and legal requirements and does not interfere with the security
controls. If a risk is identified, additional controls should be identified and
implemented (or planned) prior to acquisition. An alternative product may be
considered as a result of the risk analysis.

