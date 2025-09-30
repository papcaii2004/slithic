
# Slithic

[![Forked from MythicAgents/sliver](https://img.shields.io/badge/Forked%20from-MythicAgents%2Fsliver-blue)](https://github.com/MythicAgents/sliver)

This is a fork of the official [Sliver](https://github.com/MythicAgents/sliver) agent for the Mythic C2 framework. This repository is intended for customizing, bug fixing, and experimenting with new features based on the original agent.

All credit for the original agent goes to the development team at **MythicAgents**.

---

## Purpose of this Fork

This repository was created to track and implement the following changes:

- [ ] Fix the missing log issue for the `generate` command.
- [ ] Optimize asynchronous command handling.
- [ ] Add a new command to... *(e.g., automatically clean up generated payloads)*.
- [ ] For learning and research purposes on how Mythic agents work.

## Key Changes (Changelog)

- **[Date]** - Forked the repository and set up the local development environment.
- *(Document your changes here)*

---

## Installation & Development Setup

To install and work with this version of the agent from a local directory, follow these steps on your Mythic server.

### Step 1: Remove the Old Agent (If present)

To prevent any conflicts, first remove any existing installation of the `sliver` agent.

```bash
# Navigate to your Mythic installation directory
cd /path/to/your/Mythic/

# Run the remove command
sudo ./mythic-cli remove sliver
```

### Step 2: Clone Your Repository

Clone this repository to a location on your Mythic server.

```bash
# Example: cloning to the /root/ directory
git clone https://github.com/papcaii2004/sliver.git /root/my-sliver-agent
```

### Step 3: Install the Agent from the Local Directory

Instruct Mythic to use the source code from the directory you just cloned instead of pulling from GitHub.

```bash
# Still within the Mythic directory
sudo ./mythic-cli install /root/my-sliver-agent
```

### Step 4: Restart Mythic

This command will build the new Docker images from your local source code and restart the entire system.

```bash
sudo ./mythic-cli restart
```

## Development Workflow

Once the initial setup is complete, the workflow for editing code and testing changes is extremely fast:

1.  **Edit Code:** Modify the source code files (e.g., the Python files) in your cloned directory (`/root/my-sliver-agent`).
2.  **Apply Changes:** After saving your files, you **only need to restart the agent's container**.

    ```bash
    # From your Mythic directory
    sudo ./mythic-cli restart sliverapi
    ```

This process takes only a few seconds, and your changes will be applied immediately.