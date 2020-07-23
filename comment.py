import sys

from darwin.client import Client
from darwin.exceptions import NotFound
from tqdm import tqdm


def post_workflow_comment(client, workflow_id, text, x=1, y=1, w=1, h=1):
    client.post(
        f"workflows/{workflow_id}/workflow_comment_threads",
        {"bounding_box": {"x": x, "y": y, "w": w, "h": h}, "workflow_comments": [{"body": text}]},
    )


def instantitate_item(client, item_id):
    result = client.post(f"dataset_items/{item_id}/workflow")
    return result["current_workflow_id"]


def post_comment(dataset, filename, text, x=1, y=1, w=1, h=1):
    items = dataset.fetch_remote_files(filters={"filenames": [filename]})
    items = list(items)
    if len(items) == 0:
        print(f"No files matching '{filename}' found")
    for item in items:
        workflow_id = item.current_workflow_id
        if not workflow_id:
            workflow_id = instantitate_item(dataset.client, item.id)
        post_workflow_comment(dataset.client, workflow_id, text, x, y, w, h)


if len(sys.argv) < 4:
    print("usage: python approve.py team/dataset filename comment")
    sys.exit(0)
dataset_name = sys.argv[1]
filename = sys.argv[2]
comment = " ".join(sys.argv[3:])

client = Client.local()
try:
    dataset = client.get_remote_dataset(dataset_identifier=dataset_name)
except NotFound:
    print(f"unable to find dataset: {dataset_name}")
    sys.exit(0)

post_comment(dataset, filename, comment)
