---
title: Fixing a Black Screen with macOS Windows App and Ubuntu GNOME Remote Login
date: 2026-08-22
tags:
  - rdp
  - ubuntu
  - gnome
  - macos
  - remote-desktop
categories:
  - infrastructure
---

I recently connected to an Ubuntu desktop from a Mac using Microsoft's Windows App. The connection opened successfully, but the remote window stayed completely black.

<!--more-->

## The cause

Ubuntu's GNOME Remote Login uses RDP server redirection. The first connection reaches the system RDP service, and GNOME then redirects the client to the graphical user session.

The macOS Windows App did not follow that redirect with its default connection profile. The connection therefore appeared to succeed, but no desktop pixels were displayed.

## The fix

Export the connection from Windows App as an RDP file:

1. Open **Windows App** on macOS.
2. Select the remote PC.
3. From the macOS menu bar, choose **Connections → Export to RDP file…**.
4. Open the exported `.rdp` file in a plain-text editor.
5. Find this line:

```text
use redirection server name:i:0
```

Change it to:

```text
use redirection server name:i:1
```

If the line is missing, add it to the file. Save the file, then import it back into Windows App with **Connections → Import from RDP file…**. On some versions of the client, the import command is under **File → Import**.

Open the newly imported connection. Make sure the file still ends in `.rdp` rather than `.rdp.txt`.

## Why this works

The value `i:1` tells the RDP client that it may use the server name supplied during the RDP redirection step. This setting is unrelated to folder, drive, or clipboard redirection.

The important clue in the server logs was the RDP handoff: the server sent a redirection request, and the client failed during the follow-up connection. That pointed to the client profile rather than a general network or graphics problem.

## Notes

Use the Remote Login credentials shown in Ubuntu's **Settings → System → Remote Desktop → Remote Login** panel. These are the credentials configured for GNOME Remote Login.

If the problem continues, other black-screen causes are possible. Check the GNOME Remote Desktop logs and confirm that the client is using the imported profile.

References:

- [GNOME: Log in remotely to your device](https://help.gnome.org/gnome-help/remote-login.html)
- [GNOME Remote Desktop: Headless multi-user remote login](https://github.com/GNOME/gnome-remote-desktop#headless-multi-user-remote-login)
- [Microsoft: Connect to Remote Desktop Services and remote PCs on macOS](https://learn.microsoft.com/en-us/previous-versions/remote-desktop-client/remote-desktop-macos)
- [Microsoft: Remote Desktop URI and RDP properties](https://learn.microsoft.com/en-us/previous-versions/remote-desktop-client/remote-desktop-uri)
