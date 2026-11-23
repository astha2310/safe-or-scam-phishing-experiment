# The 8 Scenarios

Each scenario has two parts:
- **What participants saw:** the message, exactly as shown in the quiz
- **Analyst write-up:** how a Tier-1 SOC analyst would investigate it, as a 7-step story: what, where, when, clues, intel, verdict, action

**Setup shown to participants:** *Imagine you work at a company called Brightline Corp. Your work email ends in @brightline.example. Your coworkers, IT team and vendors are real people you work with.*

All companies, people, phone numbers and links are fictional. `.example` domains can never be real websites.

| # | Message | Answer | People correct | ATT&CK |
|---|---|---|---|---|
| [1](#scenario-1--fake-it-password-email) | Fake IT password email | Scam | 86% | T1566.002 |
| [2](#scenario-2--mfa-prompt-you-started) | MFA prompt you started | Safe | 73% | — |
| [3](#scenario-3--delivery-text) | Delivery text | Scam | 50% | T1566.002 / T1660 |
| [4](#scenario-4--hacked-coworker-invoice) | Hacked coworker invoice | Scam | 45% | T1566.001, T1534 |
| [5](#scenario-5--it-maintenance-notice) | IT maintenance notice | Safe | 82% | — |
| [6](#scenario-6--sign-in-from-an-unknown-device) | Sign-in from an unknown device | Suspicious | 82% | T1078 |
| [7](#scenario-7--vendor-invoice) | Vendor invoice | Safe | 82% | — |
| [8](#scenario-8--one-calm-mfa-prompt) | One calm MFA prompt | Scam | 55% | T1621 |

---

## Scenario 1 — Fake IT password email

**What participants saw**
> **Email**
> **From:** IT Service Desk `<support@brightline-it-helpdesk.example>`
> **Subject:** ACTION REQUIRED: Your password expires today
>
> Your Brightline password expires in 2 hours. To avoid losing access to email and files, verify your account now. Accounts not verified by 9:00 PM will be locked.
>
> **Link:** `http://brightline-it-helpdesk.example/verify`

**Answer: Scam** · ATT&CK T1566.002 Spearphishing Link

**Analyst write-up**
1. **What:** an email impersonating IT asks users to "verify" their password through a link
2. **Where:** sent to 40 employees in Finance and HR
3. **When:** Friday 6:40 PM, after IT has left for the weekend
4. **Clues:** the sender domain is `brightline-it-helpdesk.example`, not the real `brightline.example` · a rushed deadline and a threat · the link leads to an outside login page · real IT never asks for passwords by email
5. **Intel:** URL reputation lookup (e.g. VirusTotal) · PhishGuard: phishing (98.5%) · Email Analyzer: phishing (76.9%)
6. **Verdict:** true positive
7. **Action:** purge the email from all inboxes · block the domain · check proxy logs for who clicked · reset passwords for anyone who entered credentials · escalate to L2

---

## Scenario 2 — MFA prompt you started

**What participants saw**
> **Phone pop-up**
> **Situation:** You just typed your password into the Brightline employee portal on your laptop. Your laptop screen shows the number **42**.
>
> **From:** Brightline Authenticator app
> "Are you trying to sign in? Location: Phoenix, AZ. Enter the number shown on your screen to approve."
> [Approve] [Deny]

**Answer: Safe**

**Analyst write-up**
1. **What:** an MFA approval request following a user-initiated sign-in
2. **Where:** the user's phone and laptop
3. **When:** seconds after the user entered their password
4. **Why it's safe:** the user started the sign-in · the number on the phone matches the laptop · the location is the user's own
5. **Intel:** sign-in logs show the user's usual device and location
6. **Verdict:** benign (false positive if reported)
7. **Action:** close. **Lesson:** number matching ties the approval to the screen in front of you, which defeats MFA fatigue attacks (compare with Scenario 8). Some participants thought typing a number was suspicious, which shows that users need to be taught what this control looks like.

---

## Scenario 3 — Delivery text

**What participants saw**
> **Text message (SMS)**
> **Situation:** You ordered a jacket online 3 days ago and you're waiting for it to arrive.
>
> **From:** +1 (480) 555-0147
>
> ParcelGo: ACTION REQUIRED. We attempted to deliver your package today but were unsuccessful. Please verify your delivery information by Nov 23 at parcelgo-redelivery.example. If not resolved by the deadline, your package will be returned to the sender.

**Answer: Scam** · ATT&CK T1566.002 Spearphishing Link (Mobile: T1660 Phishing)

**Analyst write-up**
1. **What:** a fake delivery notice with a link to "verify" details (smishing)
2. **Where:** the user's phone
3. **When:** Friday 7:15 PM, when it's hard to call the carrier to check
4. **Clues:** a regular 10-digit number instead of a carrier short code · a made-up domain, not the carrier's site · a deadline plus a threat · no tracking number and no name
5. **Intel:** PhishGuard: phishing (98.3%) · Email Analyzer: phishing (77.3%) · the domain was registered days ago
6. **Verdict:** true positive
7. **Action:** don't click; report as junk. On a work phone: check whether the domain was visited, block it, and warn staff if others received it

**Why it worked on half the participants:** expecting a real package turns a suspicious text into a believable one. Attackers time these around holidays and sales for exactly this reason.

---

## Scenario 4 — Hacked coworker invoice

**What participants saw**
> **Email**
> **Situation:** You work in the Finance team.
>
> **From:** Priya Shah `<priya.shah@brightline.example>` (your coworker in Marketing)
> **Subject:** RE: Invoice
>
> Hi, please review the attached invoice and approve it today. The file is password-protected for security. Password: 1234. Thanks
>
> **Attachment:** `Invoice_Nov.zip`

**Answer: Scam** · ATT&CK T1566.001 Spearphishing Attachment + T1534 Internal Spearphishing

**Analyst write-up**
1. **What:** an email from a real internal account with a password-protected .zip "invoice"
2. **Where:** sent from Priya's account to 15 people in Finance
3. **When:** Tuesday 2:30 PM, during normal hours, which makes it blend in
4. **Clues:** Marketing doesn't send invoices · "RE:" with no earlier thread · password-protected archives hide their contents from virus scanners · short and pushy, unlike how Priya normally writes
5. **Intel:** Email Analyzer: **legitimate (86.2%)**, so the model missed it · a sandbox opens the archive and finds malware · sign-in logs show Priya's account was accessed from an unfamiliar location the day before
6. **Verdict:** true positive. The account is compromised
7. **Action:** purge the email · reset Priya's password and revoke her sessions · check her mailbox for forwarding or deletion rules · identify who opened the file · escalate to L2 as an account compromise

**The hardest scenario in the study** (45% correct). The sender address is genuine, so the usual "check the sender" advice fails. Most people who trusted it were confident they were right.

---

## Scenario 5 — IT maintenance notice

**What participants saw**
> **Email**
> **From:** Brightline IT `<it@brightline.example>`
> **Subject:** Scheduled maintenance: Saturday 10 PM–2 AM
>
> Email and the employee portal will be unavailable Saturday, Nov 28, from 10 PM to 2 AM ET while we install updates. You don't need to do anything. Questions? Contact the IT Service Desk through the usual portal or call ext. 4357.

**Answer: Safe**

**Analyst write-up**
1. **What:** a planned-maintenance announcement
2. **Where:** sent to all employees
3. **When:** Thursday 10:00 AM, during business hours and with notice ahead of time
4. **Why it's safe:** the real `brightline.example` domain · no link and no request for credentials · asks the user to do nothing · points to the usual support channels
5. **Intel:** SPF, DKIM and DMARC pass · the IT change calendar lists the maintenance · Email Analyzer: legitimate (96.4%)
6. **Verdict:** benign
7. **Action:** close. If a user reports it, thank them for checking

---

## Scenario 6 — Sign-in from an unknown device

**What participants saw**
> **Account security page**
> **Situation:** You're at home in Phoenix. You only use your MacBook for work. You signed in 10 minutes ago. You open your "Recent sign-ins" page and see:
>
> 9:02 PM – Phoenix, AZ – MacBook – Safari
> 9:11 PM – Phoenix, AZ – Windows PC – Chrome

**Answer: Suspicious** · ATT&CK T1078 Valid Accounts

**Analyst write-up**
1. **What:** a sign-in from an unfamiliar device and browser
2. **Where:** the user's work account
3. **When:** 9 minutes after the user's own sign-in
4. **Clues:** the user doesn't own a Windows PC · a new browser · the matching city is the trick: attackers route through proxies near the victim to avoid "impossible travel" alerts
5. **Intel:** the IP belongs to a residential proxy service, not the user's ISP · the device has never been seen on this account
6. **Verdict:** true positive. Someone has the password
7. **Action:** revoke all sessions · reset the password · review MFA methods for anything the attacker added · check what the session accessed · block the IP · escalate to L2

**Detection idea (KQL, Microsoft Sentinel):** flag a successful sign-in from a device or browser never seen for that user in the last 30 days, even when the location matches.

---

## Scenario 7 — Vendor invoice

**What participants saw**
> **Email**
> **From:** CloudNest Billing `<billing@cloudnest.example>` (a vendor Brightline pays every month)
> **Subject:** Your November invoice #INV-20481
>
> Hi Brightline team, your November invoice ($249.00) is ready. You can view it by signing in to your CloudNest account as usual. No action is needed if you have auto-pay turned on. Questions? Reply to this email or call the number on your contract.

**Answer: Safe**

**Analyst write-up**
1. **What:** a routine monthly invoice notification
2. **Where:** the billing team
3. **When:** the 1st of the month, 8:00 AM, the same time as every month
4. **Why it's safe:** a known vendor · the usual amount · no link or attachment · tells you to sign in yourself
5. **Intel:** SPF, DKIM and DMARC pass · the domain matches past invoices · Email Analyzer: **phishing (62.6%)**, a false alarm triggered by words like *invoice*, *account* and *sign in*
6. **Verdict:** benign
7. **Action:** close. **Lesson:** the safe way to handle any bill is to go to the site you already know, never through a link in the email

---

## Scenario 8 — One calm MFA prompt

**What participants saw**
> **Phone pop-up**
> **Situation:** It's 2:15 PM on a workday. You're in a meeting and not using your computer. You signed in to your work email this morning.
>
> **From:** Brightline Authenticator app
> "Are you trying to sign in? Location: Phoenix, AZ"
> [Approve] [Deny]

**Answer: Scam** · ATT&CK T1621 Multi-Factor Authentication Request Generation

**Analyst write-up**
1. **What:** an MFA request the user didn't start
2. **Where:** the user's phone and work account
3. **When:** mid-afternoon, at a plausible time, with only one prompt, so it doesn't look like an attack
4. **Clues:** the user isn't signing in to anything · a single prompt with the "right" location feels like a glitch, which is exactly why people tap Approve
5. **Intel:** sign-in logs show a correct password followed by an MFA request from an unfamiliar IP
6. **Verdict:** true positive. The attacker already has the password
7. **Action:** deny and report · reset the password immediately · revoke sessions · block the IP · escalate to L2 · recommend number matching (see Scenario 2)

**Detection idea (KQL, Microsoft Sentinel):** alert when a sign-in passes the password step but MFA is denied or times out, especially from an IP not previously seen for that user.
