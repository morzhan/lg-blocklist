# LG TV blocklist for Pi-hole

This is my personal blocklist for my own LG TVs and Pi-hole setup. I'm fairly
paranoid about what LG TVs send over the network, so I started collecting domains
from LG privacy projects, existing blocklists and my own DNS logs. I'm willing
to lose smart TV features to reduce unwanted network activity.

I'm sharing the lists publicly in case they are useful to someone else. Feel
free to use, copy, fork or adapt them. They reflect my preferences and the
features I can live without; test them against the features that matter to you.
I maintain it for my own setup, and compatibility with other models and app
combinations is untested.

The lists include German endpoints and country variants from the source
projects. Some entries are service infrastructure rather than proven tracking
hosts. Inclusion reflects a blocking choice; a DNS lookup alone does not show
what data a service sends. The expanded lists have not yet been validated
through Pi-hole on a real TV.

| File | Purpose | Impact |
| --- | --- | --- |
| [01-ads-and-telemetry.txt](01-ads-and-telemetry.txt) | Advertising, ACR, reporting and telemetry hosts, plus `static.doubleclick.net` | Suggested starting point; includes regional variants and still needs app testing |
| [02-optional-lg-services.txt](02-optional-lg-services.txt) | LG Home, recommendations, account, Content Store, ThinQ, UEI and Google push endpoints | Can break Home features, sign-in, Content Store, ThinQ, Alexa, push messages and content/update delivery |
| [03-optional-clock-sensitive.txt](03-optional-clock-sensitive.txt) | SDP and WiseLG hosts used by LG's service platform and clock synchronization | Leave unused by default: blocking can prevent clock synchronization after a power cut and cause HTTPS certificate errors |
| [04-optional-lg-channels.txt](04-optional-lg-channels.txt) | LG Channels and its Pluto/Xumo backends | Can stop LG Channels and affect related Pluto features |
| [05-optional-firmware-updates.txt](05-optional-firmware-updates.txt) | LG firmware update checks and downloads | Blocks firmware updates, including security updates |

Each file is a separate addition; none includes the others. All names are exact
domains, with no wildcards or regular expressions. A bare domain does not block
all its subdomains. `lgchhomeapp.lgtvcommon.com`, previously in list 02, now lives
in list 04 so LG Channels can be selected separately.

## Add to Pi-hole

Create an `LG-TV` group and associate the TV's clients with it. Cover both IPv4
and IPv6, checking which client identities appear in the query log. The TV can
remain in the Default group to retain existing general-purpose blocking.

Add the desired raw URLs below as **blocking lists** under Lists/Adlists. Assign
each subscription only to `LG-TV`, removing its Default assignment, then update
Gravity. Begin with list 01 and add list 02 only if its service losses are
acceptable. Leave list 03 unused until a working alternative way of setting the
TV's clock has been established. Add lists 04 and 05 only if blocking LG Channels
or firmware updates is intended.

```text
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/01-ads-and-telemetry.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/02-optional-lg-services.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/03-optional-clock-sensitive.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/04-optional-lg-channels.txt
https://raw.githubusercontent.com/morzhan/lg-blocklist/main/05-optional-firmware-updates.txt
```

Alternatively, copy the names into Pi-hole's domain management page as exact
deny entries. Assign those entries only to `LG-TV` and remove their Default
assignment. Pi-hole documents [group-based blocking](https://docs.pi-hole.net/group_management/example/).

Pi-hole blocks a list entry whenever that list is active, including immediately
after a power cut. If the clock or certificates fail after enabling list 03,
disable that list, update Gravity and verify that the TV's time recovers.

## What to expect

Blocked queries still appear in Pi-hole's log, marked blocked. These lists do
not stop the TV generating its LAN PTR discovery sweep. Queries sent through a
different DNS service, direct IP connections and existing cached connections
are outside their coverage. DNS blocking does not reliably remove YouTube ads.

Netflix, Prime Video and YouTube delivery domains, connectivity checks, local
proxy discovery and shared Google service hosts are left out. List 04 deliberately
targets LG Channels, including some Pluto/Xumo domains. `de.emp.lgsmartplatform.com`
and `eligibility-panelresearch.googlevideo.com` are also left out because their
purpose has not been established for this blocklist.

## Maintain the lists

I maintain the `.txt` files directly as I review sources and my TV's network
activity. There is no automatic synchronization with another project.

When updating a list or maintaining a fork, use one lowercase domain per line,
without an IP address, URL, comment or wildcard. Keep each file sorted, unique and free of
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
next Gravity update. The lists are maintained directly in this repository.

## Sources

The initial collection came from [Glasshouse](https://github.com/rorygallagher2024/glasshouse/tree/681736d595ef0a0cefd8695f0f666ae07c42551a),
with German country coverage, and a domain observed in my own DNS logs. The
collection was expanded using all 604 unique names in
[Life's Good Without Spying's domain files](https://github.com/lewisdoesstuff/lifesgoodwithoutspying/tree/0057ce44d5b4494ad85cf5975d599c58d5f25871/app/init/blocklist.d).
Together with the existing names, the expanded import contained 730 domains.

Upstream categories are a starting point for review. API/account names mixed
into an upstream advertising list are placed in optional list 02 here. SDP and
WiseLG names stay in list 03; LG Channels and firmware updates have their own
optional files. Regional variants and firmware-listed endpoints are not all
independently observed on my TV. Google's
[advertising reference](https://support.google.com/campaignmanager/table/6096962?hl=en-VC)
also documents `static.doubleclick.net`.

## License

Free to use and adapt under the [MIT license](LICENSE). Original third-party
MIT notices are retained for [Glasshouse](LICENSES/glasshouse-MIT.txt) and
[Life's Good Without Spying](LICENSES/lifesgoodwithoutspying-MIT.txt).
