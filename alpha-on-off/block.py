import alphaui as gr
import random
import re
import subprocess

def cn_model(cmd, desc):
    print(cmd)
    if cmd == "Start":
        desc=desc.replace('\n', '')
        print(desc)
        cmds=['docker','start',desc]
        running_container = subprocess.Popen( cmds, stdout=subprocess.PIPE ).communicate()[0]
        running_container=running_container.decode("utf-8")
        if running_container =="":
            return str(cmds)+"  -------> Error Check the app Name"
            print("Error")
        return running_container+"  --------> App Started"

    elif cmd == "Stop":
        desc=desc.replace('\n', '')
        print(desc)
        cmds=['docker','stop',desc]
        running_container = subprocess.Popen( cmds, stdout=subprocess.PIPE ).communicate()[0]
        running_container=running_container.decode("utf-8")
        if running_container =="":
            return str(cmds)+"  -------> Error Check the app Name"
            print("Error") 

        return running_container+"  --------> App Stoped"

    elif cmd == "Get Running APPS":
        cmds = [ 'docker', 'ps']
        running_container = subprocess.Popen( cmds, stdout=subprocess.PIPE ).communicate()[0]
        running_container=running_container.decode("utf-8") 
        # running_container=str(running_container)
        # running_container=running_container.decode("utf-8") 
        
        words=re.findall('([^\s]+)', running_container)
        words = set(words)

        result = [i for i in words if i.startswith('alpha-')]
        strs="""{}""".format("\n".join(result[0:]))
        return strs

    elif cmd == "Get Stop APPS":
        cmds = [ 'docker', 'ps','-f status=exited']
        running_container = subprocess.Popen( cmds, stdout=subprocess.PIPE ).communicate()[0]
        running_container=running_container.decode("utf-8") 
        # running_container=str(running_container)
        # running_container=running_container.decode("utf-8") 
        
        words=re.findall('([^\s]+)', running_container)
        words = set(words)

        result = [i for i in words if i.startswith('alpha-')]
        strs="""{}""".format("\n".join(result[0:]))
        print(desc)
        return strs



    return desc

block = gr.Blocks()

with block:
    gr.Markdown("Choose the Application to Start or Stop")
    cmd = gr.inputs.Radio(["Start", "Stop", "Get Running APPS","Get Stop APPS"],
                                      label="APP Status Status")



    with gr.Tab("Applications"):
        with gr.Row():
            cn_text = gr.inputs.Textbox(placeholder="Enter the App name to Start or Stop", lines=1)
            cn_results = gr.outputs.Textbox()
        cn_run = gr.Button("Submit")
        cn_run.click(cn_model, inputs=[cmd, cn_text], outputs=cn_results,)
    
    with gr.Tab("Bulk"):
        with gr.Row():
            cn_text = gr.inputs.Textbox(placeholder="Enter the App name to Start or Stop", lines=7)
            cn_results = gr.outputs.Textbox()
        cn_run = gr.Button("Submit")
        cn_run.click(cn_model, inputs=[cmd, cn_text], outputs=cn_results,)


# cmds = [ 'docker', 'ps','-f status=exited']
# print(cmds)
# running_container = subprocess.Popen( cmds, stdout=subprocess.PIPE ).communicate()[0]
# running_container=running_container.decode("utf-8") 
# print(running_container)
# exit()


block.launch(server_name='0.0.0.0',server_port=7860, auth=("alpha","alpha"),auth_message="Hey Contact an Alpha for Accessing 🙂")