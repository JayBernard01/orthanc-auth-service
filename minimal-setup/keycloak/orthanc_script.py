from pyorthanc import orthanc_sdk

# TODO(Jé): change permissions automatically to reflect all Azure AD users
# TODO(Jé): -> next: update on adding or removing users from Azure (post, put, delete)
# TODO(Jé): automatically add a tag to a new instance with a specific label
# TODO(Jé): -> next: specific for the user's role
# TODO(Jé): -> next: change tag based on user's role when modified (post, put, delete)
# TODO(Jé): -> next: change permissions automatically when change in keycloack (post, put, delete)
# TODO(Jé): -> next: let users give access and auth rights to other users


# curl -u share-user:change-me -H "Content-Type: application/json" http://localhost:8000/settings/roles
# -d '{"roles":{
# "admin-role":{"authorized-labels":["*"],"permissions":["all"]},
# "doctor-role":{"authorized-labels":["*"],"permissions":["view","download","share","send"]},
# "external-role":{"authorized-labels":["external"],"permissions":["view","download"]}},"available-labels":[]}'
def on_change(change_type: orthanc_sdk.ChangeType, _level: orthanc_sdk.ResourceType, resource: str) -> None:
    if change_type == orthanc_sdk.ChangeType.ORTHANC_STARTED:
        print("Started", flush=True)  # noqa: T201

    elif change_type == orthanc_sdk.ChangeType.ORTHANC_STOPPED:
        print("Stopped", flush=True)  # noqa: T201

    elif change_type == orthanc_sdk.ChangeType.STABLE_STUDY:
        print("A stable study was uploaded: %s" % resource, flush=True)  # noqa: T201
        label = "research"

        orthanc_sdk.RestApiPut(f"/studies/{resource}/labels/{label}", "{}")


orthanc_sdk.RegisterOnChangeCallback(on_change)
