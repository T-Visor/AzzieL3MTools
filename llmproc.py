## AzzieL3MTools
## llmproc.py
## Hillman
## April 2026

import ollama
import utils
import json
import httpx

## following loads the LLM data
llmfile = "llminit.json"

## following returns a list of LLM models
def getllmlist(model = ""):
    lset = []
    if model != "":
        # lset= []
        lmlist = ollama.list()["models"]
        for i in lmlist:
            if i['model'] == model:
                lset.append({"model": i['model'], 
                            "testrun": "",
                            "format": i["details"]["format"],
                            "families": i["details"]["families"],
                            "quantizationlevel": i["details"]["quantization_level"],
                            "digest": i["digest"],
                            "total_params": i['details']['parameter_size'],
                            "filesize GB": i["size"]/1000000000
                            })
        if len(lset) == 0: lset.append({})
        return lset[0] 
    else:
        lmlist = ollama.list()["models"]
        for i in lmlist:
            sval = float(i["size"] / 1000000000)
            if sval < 0.01: sval = 0
            pval = i['details']['parameter_size']
            cllm = ""
            if  ":CLOUD" in i["model"].upper():  #pval == "": 
                pval = " n/a "
                cllm = "CLOUD_"
            lset.append({"model": i['model'], "details": f"{cllm}{i["model"]}   Parameters: {pval} Filesize: {sval:.2f} GB"})

        return lset       

def getllmsetlist():
    lset = []
    # Load your config
    data = utils.loadjson("config/llminit.json")
    lmlist = data.get("llmsettings", [])
    
    for i in lmlist:
        if isinstance(i, dict):
            # If it's a dict, get the config name
            lset.append(i.get("llmconfig", "Unknown"))
        else:
            # If it's already a string, just add it!
            lset.append(str(i))
    return lset


# following provides a dict of named llm setting
def getllmsettings(sname="Baseline"):
    lset = {}
    data = utils.loadjson("config/llminit.json")
    lmlist = data.get("llmsettings", [])
    
    for i in lmlist:
        # We can only find a "named" setting if 'i' is a dictionary
        if isinstance(i, dict) and i.get("llmconfig") == sname:
            return i
            
    # If we didn't find a dict, return a default set of options 
    # so startllm() doesn't crash later
    return {
        "llmconfig": sname,
        "format": "json",
        "keep_alive": "5m",
        "options": {}
    }

# following returns a string with currently running LLM
def getcurrentllm():
    cllm = ""
    llmcurr = ollama.ps()["models"]
    if len(llmcurr) == 0:
        cllm = ""
    else:
        cllm =  llmcurr[0]["model"]
    return cllm

## following gets the preprompt from the pp file
def getpreprompt(pp):
    pplist = utils.loadjson("config/llmprompts.json")
    # fnd = False
    ipp = {"preprompt": {}}
    for i in pplist:
        if i["preprompt"]["qryid"] == pp: 
            ipp = i
    return ipp

## following will start an LLM
# def startllm(model: str,llmtime="30m", settings="Baseline"):
def startllm(model: str,settings="Baseline"):   
    try:
        if ":CLOUD" in model.upper(): return "Cloud Model Started"
        mset = ollama.ps()["models"]
        # print(mset)
        if len(mset) > 0:
            print(mset[0]["model"])            
            if mset[0]["model"] == model: 
                print(model, " ALREADY RUNNING ")
                return "RUNNING"
        print("Starting: " + model)

        getllmset = getllmsettings(settings)
        # llmoptions = getllmset["options"]
        # keep_alive = getllmset["keep_alive"]

        fpp = "init"  
        
        llmsystem = fpp 

        ollama.chat(
            model=model,
            stream=False,
            format=getllmset["format"],
            keep_alive= getllmset["keep_alive"],
            messages= [
                {"role":"system", "content": json.dumps(llmsystem) },
                {"role":"user","content": json.dumps("init")}
            ],
            options = getllmset["options"]
        )

        return model + " ... STARTED"
    except:
        return model + " ... LOAD FAILED"


## following will stop an LLM
def stopllm(model: str):
    try:
        if ":CLOUD" in model.upper(): return "Model Started"
        if model == "":
            # print("stopping model: ", model)
            model = mset = ollama.ps()["models"][0]["model"]
            print(model)
        # ollama.chat(model=model, keep_alive=0)
        ollama.generate(model=model, prompt="",keep_alive=0)
        return model + " ... TERMINATED"
    except:
        return model + " ... TERMINATION FAILED"

## following supports getting op data on a specific LLM
def getllmdata(model: str):
    lset= []
    lmlist = ollama.list()["models"]
    # print(lmlist)
    for i in lmlist:
        if i['model'] == model[0]: 
            lset.append({"model": i['model'], 
                        "testrun": "",
                        "format": i["details"]["format"],
                        "families": i["details"]["families"],
                        "quantizationlevel": i["details"]["quantization_level"],
                        "digest": i["digest"],
                        "total_params": i['details']['parameter_size'],
                        "filesize GB": i["size"]
                        })
    return lset 


def getlocalmodels():
    lmset= []
    lmlist = ollama.list()["models"]

    for i in lmlist:
        lmset.append({"model": i.model, "fsize": i.size,"params": int(utils.parse_compact_number(i.details["parameter_size"]))})   #, "params": i['details']['parameter_size'], "fsize": i["size"]})

    llms = lmset
    lset = []
    lsetall = []
    for i in llms:
        if not("CLOUD" in i["model"].upper()):
            lset.append(i["model"])
            lsetall.append(i)
    return lset,lsetall


BASE_URL = "https://ollama.com"
# need to make the following secret
API_KEY = ""

## following provides a list via the web interface and access to Ollama
def list_models():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    with httpx.Client(timeout=30) as client:
        r = client.get(f"{BASE_URL}/api/tags", headers=headers)
        r.raise_for_status()
        return r.json()


