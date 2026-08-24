<p align="center">
  <img src="https://camo.githubusercontent.com/829b5f87e3be45528384ff7a4ceb8f41ebb0c96eb1167c2faefdc6c910c93f6e/68747470733a2f2f6d65646961302e67697068792e636f6d2f6d656469612f76312e59326c6b505463354d4749334e6a45785a446831625752705a446874616e4a36597a59346144423261446874615467334f446c3365486332636d56346247557a6154413362695a6c634431324d563970626e526c636d35686246396e61575a66596e6c666157516d593351395a772f476768474b615a384a65484a7830617051432f67697068792e676966" width="200" alt="" />
</p>

<h1 align="center">Jacob Cook</h1>

<p align="center"><b>Detection &amp; Security Automation Engineer</b></p>

<p align="center"><i>I turn noisy telemetry into detections you can trust — false positives documented before you ask.</i></p>

<p align="center">
  <a href="https://www.linkedin.com/in/jcook-dev"><img src="https://img.shields.io/badge/LinkedIn-jcook--dev-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  &nbsp;
  <a href="https://jacobdcook.com"><img src="https://img.shields.io/badge/Portfolio-jacobdcook.com-4A90D9?style=for-the-badge&logo=vercel&logoColor=white" /></a>
  &nbsp;
  <a href="https://www.jacobdcook.com/resume.pdf"><img src="https://img.shields.io/badge/Resume-Download_PDF-22C55E?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Security%2B-C8202F?style=for-the-badge&logo=comptia&logoColor=white" />
  <img src="https://img.shields.io/badge/CySA%2B-C8202F?style=for-the-badge&logo=comptia&logoColor=white" />
  <img src="https://img.shields.io/badge/PenTest%2B-C8202F?style=for-the-badge&logo=comptia&logoColor=white" />
  <img src="https://img.shields.io/badge/SecurityX-C8202F?style=for-the-badge&logo=comptia&logoColor=white" />
  <img src="https://img.shields.io/badge/CSIE-C8202F?style=for-the-badge&logo=comptia&logoColor=white" />
</p>

```yaml
title: Detection Engineer Activity Observed
id: jacob-cook
status: stable
description: >
  Builds reliable triage from noisy telemetry. Every detection ships with
  documented false-positive scenarios and a repeatable response playbook.
references:
  - https://jacobdcook.com
logsource:
  product: github
  service: jacobdcook
detection:
  selection:
    capabilities:
      - 'behavioral Sigma detections mapped to MITRE ATT&CK'
      - 'Wazuh SIEM deployment and rule tuning'
      - 'identity attack detection (Okta / Azure / AWS)'
      - 'SOAR response automation in Python'
  condition: selection
falsepositives:
  - unlikely — check the repos below
level: high
```

Currently pursuing an **MS in Cybersecurity** at Western Governors University (expected **October 2026**) while working in IT and building a blue-team / detection engineering portfolio in public.

## What I build — and where the proof is

| Claim | Evidence |
| --- | --- |
| **Detection-as-code** — Sigma rules mapped to MITRE ATT&CK, modeled on real incidents | [Stryker / Intune Detection Pack](https://github.com/jacobdcook/stryker-intune-detection-pack) |
| **SIEM deployment & tuning** — Wazuh stack with documented alert triage and rule IDs | [Blue Team SOC Monitoring Lab](https://github.com/jacobdcook/blue-team-soc-monitoring-lab) |
| **Identity attack detection** — MFA fatigue, impossible travel, CloudTrail scenarios | [Okta Detection Engine](https://github.com/jacobdcook/okta-detection-engine) · [AWS Identity Detection Lab](https://github.com/jacobdcook/aws-identity-detection-lab) |
| **SOAR automation** — alert ingestion driving automated response playbooks | [SOAR-lite IR Orchestrator](https://github.com/jacobdcook/soar-incident-orchestrator) |
| **Cloud misconfiguration auditing** — Terraform static analysis + live Azure checks | [Cloud Security Auditor](https://github.com/jacobdcook/cloud-security-auditor) · [Azure Hardening Lab](https://github.com/jacobdcook/Azure-Cloud-Hardening-Lab) |

**How I think about detection:**

- A detection without documented false positives is just future noise.
- Rules live in version control, get tested, and map to ATT&CK — or they don't ship.
- If I'd run the same response twice, it becomes a playbook.

## Tech & tooling

**Languages & frameworks**

<p align="left">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E" alt="JavaScript" />
  <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB" alt="React" />
  <img src="https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white" alt="C" />
</p>

**Security, cloud & infrastructure**

<p align="left">
  <img src="https://img.shields.io/badge/Sigma-Detections-1A73E8?style=for-the-badge" alt="Sigma" />
  <img src="https://img.shields.io/badge/MITRE-ATT%26CK-C0392B?style=for-the-badge" alt="MITRE ATT&CK" />
  <img src="https://img.shields.io/badge/Wazuh-SIEM-005792?style=for-the-badge&logo=wazuh&logoColor=white" alt="Wazuh" />
  <img src="https://img.shields.io/badge/Okta-identity-007DC1?style=for-the-badge&logo=okta&logoColor=white" alt="Okta" />
  <img src="https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />
  <img src="https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white" alt="Azure" />
  <img src="https://img.shields.io/badge/AWS-%23232F3E.svg?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/linux-%23FCC624.svg?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
</p>

## Detection engineering & blue team

**Featured — [Stryker / Intune Detection Pack](https://github.com/jacobdcook/stryker-intune-detection-pack)** — Detection-as-code for Intune MDM abuse, modeled on the 2026 Stryker/Handala attack: Sigma rules, KV-store enrichment, and response playbooks mapped to MITRE ATT&CK.

| <p align="center"><b>Blue Team SOC Monitoring Lab</b></p> | <p align="center"><b>SOAR-lite — IR Orchestrator</b></p> | <p align="center"><b>Network Behavior Analyzer</b></p> |
| :---: | :---: | :---: |
| <p align="center"><a href="https://github.com/jacobdcook/blue-team-soc-monitoring-lab"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/blue-team.png" width="300" height="300" /></a><br>Wazuh SIEM stack (Docker) with Linux log ingestion, brute-force detection, and documented alert triage + rule IDs<br><a href="https://github.com/jacobdcook/blue-team-soc-monitoring-lab">Project Link</a></p> | <p align="center"><a href="https://github.com/jacobdcook/soar-incident-orchestrator"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/soar-incident-orchestrator.png" width="300" height="300" /></a><br>Lightweight SOAR that ingests SIEM alerts and runs automated response playbooks for common threats<br><a href="https://github.com/jacobdcook/soar-incident-orchestrator">Project Link</a></p> | <p align="center"><a href="https://github.com/jacobdcook/network-behavior-analyzer"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/network-behavior-analyzer.png" width="300" height="300" /></a><br>Detects C2 beaconing and data exfiltration through network behavioral analysis (LLM-assisted summaries)<br><a href="https://github.com/jacobdcook/network-behavior-analyzer">Project Link</a></p> |

More detection work:

- **[Okta Detection Engine](https://github.com/jacobdcook/okta-detection-engine)** — Python detections for identity attacks: MFA fatigue, impossible travel, and more.
- **[Phishing Analysis Lab](https://github.com/jacobdcook/Phishing-Analysis-Lab)** — End-to-end phishing triage: header inspection, link extraction, VirusTotal enrichment, analyst reports.
- **[AWS Identity Detection Lab](https://github.com/jacobdcook/aws-identity-detection-lab)** — CloudTrail-style detection scenarios with pytest-backed detection logic.
- **[Security+ Learning Lab](https://github.com/jacobdcook/security-plus-labs)** · **[TCM SOC 101 Notes](https://github.com/jacobdcook/tcm-soc-101-lab-notes)** — Hands-on labs and course notes.

## Cloud & infrastructure security

| <p align="center"><b>Cloud Infrastructure Security Auditor</b></p> | <p align="center"><b>Azure Cloud Hardening Lab</b></p> |
| :---: | :---: |
| <p align="center"><a href="https://github.com/jacobdcook/cloud-security-auditor"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/cloud-security-auditor.png" width="300" height="300" /></a><br>Static analysis + live Azure auditing for Terraform and cloud misconfigurations, with a remediation-oriented workflow<br><a href="https://github.com/jacobdcook/cloud-security-auditor">Project Link</a></p> | <p align="center"><a href="https://github.com/jacobdcook/Azure-Cloud-Hardening-Lab"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/azure-lab.png" width="300" height="300" /></a><br>Hardened, secure Azure infrastructure deployed with Terraform<br><a href="https://github.com/jacobdcook/Azure-Cloud-Hardening-Lab">Project Link</a></p> |

## AI & security tooling

Where I lean on LLMs as a force-multiplier for security and productivity work:

| <p align="center"><b>G3-GPT — Document Retrieval</b></p> | <p align="center"><b>AI Log Auditor</b></p> | <p align="center"><b>Synapse AI Chat</b></p> |
| :---: | :---: | :---: |
| <p align="center"><a href="https://github.com/jacobdcook/G3-GPT"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/g3-gpt.png" width="300" height="300" /></a><br>RAG platform with Azure SSO and role-based access control for enterprise document retrieval<br><a href="https://github.com/jacobdcook/G3-GPT">Project Link</a></p> | <p align="center"><a href="https://github.com/jacobdcook/ai-log-auditor"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/ai-log-auditor.png" width="300" height="300" /></a><br>Log-analysis pipeline with automated PDF reporting and LLM-assisted triage summaries<br><a href="https://github.com/jacobdcook/ai-log-auditor">Project Link</a></p> | <p align="center"><a href="https://github.com/jacobdcook/synapse"><img src="https://raw.githubusercontent.com/jacobdcook/jacobdcook/main/assets/synapse.png" width="300" height="300" /></a><br>Multi-model desktop chat client for local Ollama models<br><a href="https://github.com/jacobdcook/synapse">Project Link</a></p> |

Also: **[Whisper Transcribe](https://github.com/jacobdcook/whisper-transcribe)** (local faster-whisper + CUDA transcription) · **[Claude Code Skills](https://github.com/jacobdcook/claude-skills)** (reusable Claude Code skill packs).

## Education & certifications

| Credential | Issuer | When |
| --- | --- | --- |
| **M.S. Cybersecurity & Information Assurance** | Western Governors University | Expected Oct 2026 |
| **B.S. Computer Science** | California State University, Sacramento | Completed |
| **SecurityX (CAS-005)** | CompTIA | 2026 |
| **PenTest+ (PT0-003)** | CompTIA | 2026 |
| **CySA+ (CS0-003)** | CompTIA | Feb 2026 |
| **Security+ (SY0-701)** | CompTIA | Jan 2026 |
| **CSIE** (Secure Infrastructure Expert) | CompTIA | Stackable credential |

## GitHub stats

<!-- Stats card is generated by .github/workflows/update-stats.yml and stored in-repo so it always loads (no external fetch). -->
![Jacob's GitHub stats](assets/github-stats.svg)

---

<p align="center">
  <a href="https://www.linkedin.com/in/jcook-dev">LinkedIn</a> ·
  <a href="https://jacobdcook.com">Portfolio</a> ·
  <a href="https://www.jacobdcook.com/resume.pdf">Resume</a>
</p>
