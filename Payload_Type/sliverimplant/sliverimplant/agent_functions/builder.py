import pathlib
from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *
from sliver import SliverClientConfig, SliverClient, client_pb2


class SliverImplant(PayloadType):
    name = "sliverimplant"
    author = "Spencer Adolph"
    note = """This payload connects to sliver to interact with a specific implant."""
    supported_os = [SupportedOS.Windows, SupportedOS.Linux, SupportedOS.MacOS]
    file_extension = ""
    wrapper = False
    wrapped_payloads = []
    supports_dynamic_loading = False
    c2_profiles = []
    mythic_encrypts = False
    translation_container = None # "myPythonTranslation"
    # agent_type = ""
    agent_path = pathlib.Path(".") / "sliverimplant"
    agent_icon_path = agent_path / "agent_functions" / "sliver.svg"
    agent_code_path = agent_path / "agent_code"
    build_steps = []
    build_parameters = [
        BuildParameter(name="sliverconfig_file_uuid", description="sliverconfig_file_uuid", parameter_type=BuildParameterType.String),
        BuildParameter(name="os", description="os", parameter_type=BuildParameterType.String),
        BuildParameter(name="mode", description="mode", parameter_type=BuildParameterType.String),
        BuildParameter(name="protocol", description="protocol", parameter_type=BuildParameterType.String),
        BuildParameter(name="host", description="host", parameter_type=BuildParameterType.String),
        BuildParameter(name="task_id", description="Original Task ID for reporting", parameter_type=BuildParameterType.Number, required=False),
    ]

    async def build(self) -> BuildResponse:

        task_id = self.get_parameter('task_id')

        try:

            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response="\n[+] Builder received task. Fetching sliver config...".encode("utf-8"),
            ))

            os = self.get_parameter('os')
            mode = self.get_parameter('mode')
            protocol = self.get_parameter('protocol')
            host = self.get_parameter('host')
            sliverconfig_file_uuid = self.get_parameter('sliverconfig_file_uuid')

            if not os:
                return BuildResponse(status=BuildStatus.Error, build_message="Missing operating system")

            if not sliverconfig_file_uuid:
                return BuildResponse(status=BuildStatus.Error, build_message="Missing sliverconfig_file_uuid")
            
            filecontent = await SendMythicRPCFileGetContent(
                MythicRPCFileGetContentMessage(AgentFileId=sliverconfig_file_uuid
            ))

            if not getattr(filecontent, "Success", True) and not getattr(filecontent, "Content", None):
                return BuildResponse(status=BuildStatus.Error, build_message="Failed to fetch sliver config file content")

            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response="\n[*] Connecting to Sliver server...".encode("utf-8"),
            ))

            config = SliverClientConfig.parse_config(filecontent.Content)
            client = SliverClient(config)
            await client.connect()

            # create C2
            url = f"{protocol}://{host}"
            c2_list = [client_pb2.ImplantC2(Priority=0, URL=url)]

            implant_config = client_pb2.ImplantConfig(
                IsBeacon=(mode=="beacon"),
                Name=f"{self.uuid}",
                GOARCH="amd64",
                GOOS=os,
                Format=client_pb2.OutputFormat.EXECUTABLE,
                ObfuscateSymbols=False,
            )
            implant_config.C2.extend(c2_list)

            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response="\n[*] Sending generate command to Sliver...".encode("utf-8"),
            ))

            implant = await client.generate_implant(implant_config)
            implant_bytes = implant.File.Data

            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response=f"\n[*] Sliver generated implant: {implant.File.Name}. Uploading to Mythic...".encode("utf-8"),
            ))

            # Upload implant to Mythic
            file_resp = await SendMythicRPCFileCreate(
                MythicRPCFileCreateMessage(
                    TaskID=self.uuid,
                    Filename=f"sliver_{mode}_{os}_{self.uuid}.bin",
                    Comment="Generated Sliver implant",
                    FileContents=implant_bytes
                )
            )

            if not getattr(file_resp, "Success", False):
                # file upload failed
                err = getattr(file_resp, "Error", "Unknown error uploading file to Mythic")
                return BuildResponse(status=BuildStatus.Error, build_message=f"Payload generated but upload failed: {err}")

            # success, file uploaded; include AgentFileId in build_message
            agent_file_id = getattr(file_resp, "AgentFileId", "UNKNOWN_ID")
            final_msg = f"[+] Success! Implant uploaded.\nAgentFileId: {agent_file_id}"
            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response=final_msg.encode("utf-8"),
            ))
            return BuildResponse(status=BuildStatus.Success, payload=implant_bytes)

        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"[-] Exception during build: {e}\n{tb}"
            
            await SendMythicRPCResponseCreate(MythicRPCResponseCreateMessage(
                TaskID=task_id,
                Response=error_msg.encode("utf-8"),
            ))
            return BuildResponse(status=BuildStatus.Error, build_message=f"See task log for error details.")