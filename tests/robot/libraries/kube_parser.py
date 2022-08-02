"""
Library to parse output (stdout) of kubectl adn kubeadm command

TODO: Do not use this, call the following (example):
  kubectl get pod -l "app=test-server" -o jsonpath='{.items[0].status.podIP}'
"""

def _general_parser(stdout):
    """Parse any kubectl output with column like output"""
    lines = stdout.splitlines()
    result = {}
    kws = lines[0].split()
    for line in lines[1:]:
        parsed_line = line.split()
        item = {kws[i]: parsed_line[i] for i in range(len(kws))}
        name = item.pop('NAME')
        result[name] = item
    return result

def parse_kubectl_get_pods(stdout):
    """Parse kubectl get pods output"""
    lines = stdout.splitlines()
    result = {}
    if "No resources found." in stdout or len(lines) == 0:
        return result
    kws = lines[0].split()
    for line in lines[1:]:
        parsed_line = line.split()
        item = {kws[i]: parsed_line[i] for i in range(len(kws))}
        parsed_line = line.split()
        name = item.pop('NAME')
        result[name] = item
    return result

def parse_kubectl_get_pods_and_get_pod_name(stdout, pod_prefix):
    """Get list of pod names with given prefix"""
    pods = parse_kubectl_get_pods(stdout)
    pods = parse_kubectl_get_pods(stdout)
    return [
        pod_name
        for pod_name, pod_value in pods.iteritems()
        if pod_prefix in pod_name
    ]

def parse_kubectl_get_nodes(stdout):
    return _general_parser(stdout)

def parse_kubectl_describe_pod(stdout):
    """Parse kubectl describe pod output"""
    lines = stdout.splitlines()
    result = {}
    info = ["IP", "Name", "Status"]
    for line in lines:
        for item in info:
            if line.startswith(f"{item}: "):
                result[item] = line.split(": ")[-1].strip()
    name = result.pop("Name")
    return {name: result}

_CID = "Container ID:"

def parse_for_first_container_id(stdout):
    lines = stdout.splitlines()
    for line in lines:
        stripline = line.strip()
        if stripline.startswith(_CID):
            return stripline[len(_CID):].strip().rpartition("//")[2]

def get_join_from_kubeadm_init(stdout):
    """Parse kubeadm init output

    Returns the join command,
    """
    lines = stdout.splitlines()
    join_cmd = [line for line in lines if "kubeadm join --token" in line]
    if len(join_cmd)  != 1:
        raise Exception(f"Not expected result: {join_cmd}")
    return join_cmd[0]
