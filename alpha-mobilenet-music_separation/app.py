from email.policy import default
import alphaui as gr
from pydub import AudioSegment
import os


split_at_timestamp = 10

def inference(audio,only_audio,StrtSec,EndSec,StrtMin,EndMin):
    print(audio)
    print(only_audio)
    print(type(audio))
    sound = AudioSegment.from_mp3(audio)

    # StrtMin = 0
    # StrtSec = 0

    # EndMin = 0
    # EndSec = 10

    StrtTime = StrtMin*60*1000+StrtSec*1000
    EndTime = StrtMin*60*1000+EndSec*1000

    extract = sound[StrtTime:EndTime]

    extract.export("foo_left.wav", format="mp3" or "wav")
    if only_audio:
        # output=[gr.outputs.Audio(type="file", label="Trim Audio")]
        return "foo_left.wav",None,None
    else:
        os.system("""python3 -m bytesep separate     --source_type="vocals"     --audio_path="foo_left.wav"     --output_path="sep_vocals.mp3" """)
        #os.system('./separate_scripts/separate_vocals.sh ' + audio.name + ' "sep_vocals.mp3"')
        os.system("""python3 -m bytesep separate     --source_type="accompaniment"     --audio_path="foo_left.wav"     --output_path="sep_accompaniment.mp3" """)
        #os.system('./separate_scripts/separate_accompaniment.sh ' + audio.name + ' "sep_accompaniment.mp3"')
        # os.system('python separate_scripts/separate.py --audio_path=' +audio.name+' --source_type="accompaniment"')
        # os.system('python separate_scripts/separate.py --audio_path=' +audio.name+' --source_type="vocals"')
        # os.system('python separate_scripts/separate.py --audio_path=' +audio.name+' --source_type="vocals"')
        # os.system('python separate_scripts/separate.py --audio_path=' +audio.name+' --source_type="vocals"')
        return 'foo_left.wav','sep_vocals.mp3', 'sep_accompaniment.mp3'
title = "Music Source Separation"

trim=gr.outputs.Audio(type="file", label="Trim Audio")
vocals=gr.outputs.Audio(type="file", label="Vocals")
comp=gr.outputs.Audio(type="file", label="Accompaniment")

# output =[gr.outputs.Audio(type="file", label="Vocals"),gr.outputs.Audio(type="file", label="Accompaniment"),gr.outputs.Audio(type="file", label="Trim Audio")]

examples = [['./examples/example1.wav',True,0,6,0,0],['./examples/example2.wav',False,0,20,0,0],['./examples/example5.mp3',False,5,20,1,0],['./examples/example3.wav',False,10,20,0,0]]
start_sec=gr.inputs.Number(default=0, label="Start Sec", optional=False)

end_sec=gr.inputs.Number(default=20, label="End Sec", optional=False)

start_min=gr.inputs.Number(default=0, label="Start Mins", optional=False)

end_min=gr.inputs.Number(default=0, label="End Mins", optional=False)


gr.Interface(
    inference, 
    [gr.inputs.Audio(type="filepath", label="Input"),gr.inputs.Checkbox(label="Only Trim Audio",default=True,optional=False),start_sec,end_sec,start_min,end_min], 
    [trim,vocals,comp],
    title=title,
    enable_queue=True,
    examples=examples,
    theme='dark'
    ).launch(server_name='0.0.0.0',server_port=7860)