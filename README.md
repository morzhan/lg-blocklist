# LG TV blocklist

Exact-domain Pi-hole blocklists for LG webOS TVs, with German country coverage.
Start with the ads list. The optional lists block LG services and can break TV
features. These lists have not yet been validated through Pi-hole on a real TV.

| File | Purpose | Impact |
| --- | --- | --- |
| [01-ads-and-telemetry.txt](01-ads-and-telemetry.txt) | Advertising and telemetry hosts, plus `static.doubleclick.net` | Recommended starting point; test the apps normally used |
| [02-optional-lg-services.txt](02-optional-lg-services.txt) | Additional LG platform, account, Content Store, ThinQ, UEI and Google push endpoints | Can break sign-in, Content Store, ThinQ, LG Channels, Alexa, push messages and content/update delivery |
| [03-optional-clock-sensitive.txt](03-optional-clock-sensitive.txt) | SDP and WiseLG hosts used by LG's service platform and clock synchronization | Leave unused by default: blocking can prevent clock synchronization after a power cut and cause HTTPS certificate errors |

The lists are separate additions. List 02 does not include list 01, and list 03
does not include either of the others. Together they initially contain 187 names.
No wildcards or regular expressions are used. A bare domain does not block all
its subdomains.

## Add to Pi-hole

Create an `LG-TV` group and associate the TV's clients with it. Cover both IPv4
and IPv6, checking which client identities appear in the query log. The TV can
remain in the Default group to retain existing general-purpose blocking.

Add the desired raw URLs below as **blocking lists** under Lists/Adlists. Assign
each subscription only to `LG-TV`, removing its Default assignment, then update
Gravity. Begin with list 01 and add list 02 only if its service losses are
acceptable. Leave list 03 unused until a working alternative way of setting the
TV's clock has been established.

```text
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/01-ads-and-telemetry.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/02-optional-lg-services.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/03-optional-clock-sensitive.txt
```

Alternatively, copy the names into Pi-hole's domain management page as exact
deny entries. Assign those entries only to `LG-TV` and remove their Default
assignment. Pi-hole documents [group-based blocking](https://docs.pi-hole.net/group_management/example/).

Pi-hole cannot reproduce Glasshouse's clock-sync grace period. A list entry is
blocked whenever that list is active, including immediately after a power cut.
If the clock or certificates fail after enabling list 03, disable that list,
update Gravity and verify that the TV's time recovers.

## What to expect

Blocked queries still appear in Pi-hole's log, marked blocked. These lists do
not stop the TV generating its LAN PTR discovery sweep. Queries sent through a
different DNS service, direct IP connections and existing cached connections
are outside their coverage. DNS blocking does not reliably remove YouTube ads.

Streaming domains, connectivity checks, local proxy discovery and shared Google
service hosts are intentionally excluded. The initial review also left out
`de.emp.lgsmartplatform.com` and `eligibility-panelresearch.googlevideo.com`
because their purpose on the tested TV had not been established.

## Maintain the lists

Edit the `.txt` files directly. Use one lowercase domain per line, without an IP
address, URL, comment or wildcard. Keep each file sorted, unique and free of
domains already present in another list. The validator enforces domain syntax,
separation of known clock-sensitive families, sorting and uniqueness.

```sh
python3 scripts/check-lists.py
```

For each addition, record its source and expected service impact in the commit
or pull request. A DNS lookup alone does not establish advertising or telemetry.
Test normal app use, reboot, cold boot and IPv4/IPv6 behavior. Record the model,
webOS version and observed result when reporting a problem. GitHub Actions runs
the validator on pushes and pull requests.

Raw URLs follow `main`, so changes become available to subscribers at their
next Gravity update. There is no automatic synchronization with Glasshouse;
updates here are maintained independently.

## Sources and license

The initial lists were derived on 13 November 2026 from
[Glasshouse's privacy module at commit 681736d5](https://github.com/rorygallagher2024/glasshouse/blob/681736d595ef0a0cefd8695f0f666ae07c42551a/server/lib/privacy.js),
with country `de`. They initially cover its generated Everything list plus
`static.doubleclick.net`, which appeared in a TV query log and is documented
in [Google's advertising reference](https://support.google.com/campaignmanager/table/6096962?hl=en-VC).
Some inherited endpoints are inferred regional coverage or firmware-listed
names, rather than traffic observed on every model.

See Glasshouse's [privacy documentation](https://github.com/rorygallagher2024/glasshouse/blob/681736d595ef0a0cefd8695f0f666ae07c42551a/docs/dashboard/privacy.md)
and [TV research](https://github.com/rorygallagher2024/glasshouse/blob/681736d595ef0a0cefd8695f0f666ae07c42551a/docs/development/TV-RESEARCH.md)
for the source's evidence and limitations. [provenance.json](provenance.json)
records the initial snapshot, not necessarily the current list counts.

MIT licensed. The original Glasshouse copyright notice is preserved in
[LICENSE](LICENSE).
