# Slithic

[![Status](https://img.shields.io/badge/Status-Functional-brightgreen)](https://github.com/papcaii2004/slithic) [![Forked from MythicAgents/sliver](https://img.shields.io/badge/Forked%20from-MythicAgents%2Fsliver-blue)](https://github.com/MythicAgents/sliver)

This is a fixed and customized fork of the official [Sliver](https://github.com/MythicAgents/sliver) agent for the Mythic C2 framework. This repository was created to fix a critical bug in the payload generation workflow and to serve as a learning and research project for Mythic's agent architecture.

All credit for the original agent goes to the development team at **MythicAgents**.

---

## Purpose & Status

This version **successfully fixes** the payload generation process, a core feature that was broken in the original agent.

- [x] **Fixed missing log issue for the `generate` command:** The build process now provides detailed, step-by-step, real-time feedback.
- [x] **Re-architected the build flow:** Clearly separated the roles of `sliverapi` (requester) and `sliverimplant` (builder/reporter) for proper asynchronous communication.
- [ ] Optimize handling for other asynchronous commands.
- [ ] For learning and research purposes on how Mythic agents work.

## How the Fixed Build Process Works

1.  **`sliverapi` (`generate.py`):** Acts as the user-facing interface. It collects parameters from the operator, then dispatches a build request (RPC) to the Mythic core, attaching the original `TaskID`.
2.  **`sliverimplant` (`builder.py`):** Acts as the build "engine". It receives the build request from the Mythic core, connects to the Sliver server, generates the implant, and crucially, **continuously reports status updates** back to the original `TaskID`, providing a detailed log for the operator.

## Changelog

- **2025-09-29:** Fully refactored the payload generation process. Fixed the communication flow between `sliverapi` and the `sliverimplant` builder, implemented a detailed logging mechanism, and corrected the file association bug (`TaskID` vs `self.uuid`) in the RPC.
- **2025-09-29:** Forked the repository and established the local development environment.

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

Clone this `slithic` repository to a location on your Mythic server.

```bash
# Example: cloning to the /root/ directory
git clone https://github.com/papcaii2004/slithic.git /root/slithic-agent
```

### Step 3: Install the Agent from the Local Directory

Instruct Mythic to use the source code from the directory you just cloned.

```bash
# Still within the Mythic directory
sudo ./mythic-cli install folder /root/slithic-agent
```

### Step 4: Restart Mythic

This command will build the new Docker images from your local source code and restart the entire system.

```bash
sudo ./mythic-cli restart
```

## Development Workflow

Once the initial setup is complete, the workflow for editing code and testing changes is extremely fast:

1.  **Edit Code:** Modify the source code files (e.g., the Python files) in your cloned directory (`/root/slithic-agent`).
2.  **Apply Changes:** After saving your files, you **only need to restart the corresponding agent container**.

    -   If you edit commands in `sliverapi` (e.g., `generate.py`):
        ```bash
        # Still within the Mythic directory
        sudo ./mythic-cli install folder /root/slithic-agent
        sudo ./mythic-cli restart
        ```

This process takes only a few seconds, and your changes will be applied immediately.
