import subprocess
import re
import alphaui as gr
def test():
    cmd = [ 'docker', 'ps']
    running_container = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
    # running_container=str(running_container)
    running_container=running_container.decode("utf-8") 
    docker_ps="""CONTAINER ID        IMAGE                               COMMAND             CREATED             STATUS              PORTS                    NAMES
    ac55ca80b459        alpha-focus_on_depth                "python app.py"     2 hours ago         Up 2 hours          0.0.0.0:9509->7860/tcp   alpha-focus_on_depth
    f24c51dec25d        alpha-resnet101-remove_background   "python app.py"     2 days ago          Up 2 days           0.0.0.0:9505->7860/tcp   alpha-resnet101-remove_background
    8336aea113f3        grafana/grafana-enterprise          "/run.sh"           2 days ago          Up 2 days           0.0.0.0:3001->3000/tcp   affectionate_vaughan
    6c5cb086c3dd        alpha-resnet-voice_recognition      "python app.py"     3 days ago          Up 3 days           0.0.0.0:9501->7860/tcp   alpha-resnet-voice_recognition
    f6c25e175358        alpha-person_detection              "python app.py"     3 days ago          Up 3 days           0.0.0.0:9504->7860/tcp   alpha-person_detection
    5f4760e4d16a        alpha-retinaface-face_detection     "python test.py"    3 days ago          Up 2 days           0.0.0.0:9503->7860/tcp   alpha-retinaface-face_detection
    """
    words=re.findall('([^\s]+)', docker_ps)
    words = set(words)

    result = [i for i in words if i.startswith('alpha')]
    strs="""{}""".format("\n".join(result[0:]))


    # words=re.findall(r'\bs\w+', docker_ps)

    # print(running_container)
    print(strs)
# print(type(words))
test()