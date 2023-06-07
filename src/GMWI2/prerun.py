import subprocess

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def print_check_message(boolean):
    print(
        bcolors.OKGREEN + "passed" + bcolors.ENDC
        if boolean
        else bcolors.FAIL + "failed" + bcolors.ENDC
    )

output_dict = {
    "metaphlan": "MetaPhlAn"
}

version_dict = {
    "metaphlan": "3.0.13"
}

def check_tool(tool):
    gt = output_dict[tool]
    version = version_dict[tool]
    print(f"Checking for {gt} v{version} on path")
    flag = "--version"
    cmd = [tool, flag]
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = proc.stdout.read().decode("ASCII")
        correct = gt in output
        correct_version = version in output
    except:
        correct = False
    print_check_message(correct)
    if not correct or not correct_version:
        print(bcolors.WARNING + tool, "not found on path or incorrect version")
        print(
            f'please run: "mamba install -c bioconda {tool}={version}"',
            bcolors.ENDC,
        )
    print()
    return correct

def check_dependencies():
    print(
        "-" * 5,
        "Dependency checks",
        "-" * 5,
    )
    any_failed = False
    for tool in output_dict:
        if not check_tool(tool):
            any_failed = True
    if any_failed:
        print(
            bcolors.FAIL,
            "Please (re)install dependencies with above instructions and rerun",
            bcolors.ENDC,
        )
    else:
        print(
            bcolors.OKGREEN,
            "All dependencies up to date",
            bcolors.ENDC,
        )
    print("-" * 5, "Dependency checks done", "-" * 5, "\n")
    return not any_failed