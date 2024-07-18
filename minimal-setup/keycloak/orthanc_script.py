from pyorthanc import orthanc_sdk


def on_change(change_type: orthanc_sdk.ChangeType, _level: orthanc_sdk.ResourceType, resource: str) -> None:
    if change_type == orthanc_sdk.ChangeType.ORTHANC_STARTED:
        print("Started", flush=True)  # noqa: T201

    elif change_type == orthanc_sdk.ChangeType.ORTHANC_STOPPED:
        print("Stopped", flush=True)  # noqa: T201

    elif change_type == orthanc_sdk.ChangeType.STABLE_STUDY:
        print("A stable study was uploaded: %s" % resource, flush=True)  # noqa: T201
        # label = "research"

        # orthanc_sdk.RestApiPut(f"/studies/{resource}/labels/{label}", "{}")


orthanc_sdk.RegisterOnChangeCallback(on_change)
