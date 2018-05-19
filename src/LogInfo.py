import os
Output_Filename = "../results/A5_Gp1/output.log"
RuntimeInfo_Logname = "../results/A5_Gp1/runtime.log"
Perodical_Logname = "../results/A5_Gp1/perodical.log"
Error_Filename = "../results/A5_Gp1/Error.log"


def set_logs_empty(flag):
    if flag:
        if os.path.exists(Output_Filename):
            os.remove(Output_Filename)
        if os.path.exists(RuntimeInfo_Logname):
            os.remove(RuntimeInfo_Logname)
        if os.path.exists(Perodical_Logname):
            os.remove(Perodical_Logname)
        if os.path.exists(Error_Filename):
            os.remove(Error_Filename)
        return True
    return False


def write_output(content, filename=Output_Filename):
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n")
    return True


def write_runtimeInfo(content, filename = RuntimeInfo_Logname):
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n")
    return True

def write_perodicalInfo(content, filename=Perodical_Logname):
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n")
    return True

def write_error(content, filename=Error_Filename):
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n")
    return True