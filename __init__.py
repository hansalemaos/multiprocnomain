import os
import platform
import subprocess
import sys
import multiprocessing

import dill

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
        "cwd": os.getcwd(),
    }
else:
    invisibledict = {}
fu = None


def init_worker(f):
    global fu
    fu = dill.loads(f)


def multifu(k, di1):
    rindex = k.pop("resultindex")
    di1[rindex] = (fu)(**k)


def start_multiprocessing(fu, it, processes=3, chunks=1,        print_stdout=False,
        print_stderr=True,):
    r"""
    Execute a given function in parallel using multiprocessing.

    Parameters:
        - fu (callable): The function to be executed in parallel.
        - it (iterable): An iterable of dictionaries, each containing the input parameters for the function.
        - processes (int): The number of processes to use (default is 3).
        - chunks (int): The chunk size for multiprocessing.Pool.starmap (default is 1).

    Returns:
        dict: A dictionary containing the results of the parallel executions, where keys correspond to the indices
            of the input iterable and values contain the corresponding function outputs.

    Examples:
        import random
        from multiprocnomain import start_multiprocessing
        import subprocess
        from a_cv_imwrite_imread_plus import open_image_in_cv
        import numpy as np


        def somefu(q=100):
            exec(f"import random", globals())  # necessary
            y = random.randint(10, 20)
            for x in range(q):
                y = y + x

            return y


        # somefu=lambda r:1111
        it = [{"q": 100}, {"q": 100}, {"q": 100}, {"q": 10}]
        b2 = start_multiprocessing(fu=somefu, it=it, processes=3, chunks=1)
        print(b2)


        def somefu2(path):
            exec(f"import subprocess", globals()) # necessary
            y = subprocess.run([f"ls" ,f"{path}"],capture_output=True)
            return y

        allpath=[{'path':'c:\\windows'}, {'path':'c:\\cygwin'}]
        b1 = start_multiprocessing(fu=somefu2, it=allpath, processes=3, chunks=1)
        print(b1)
        def somefu3(q):
            exec(f"from a_cv_imwrite_imread_plus import open_image_in_cv", globals()) # necessary
            exec(f"import numpy as np", globals()) # necessary

            im = open_image_in_cv(q)
            r = im[..., 2]
            g = im[..., 1]
            b = im[..., 0]
            return np.where((r == 255) & (g == 255) & (b == 255))


        allimages = [
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_06_04_51_956747.png"},
            {"q": r"C:\Users\hansc\Pictures\bw_clickabutton.png"},
            {"q": r"C:\Users\hansc\Pictures\cgea.png"},
            {"q": r"C:\Users\hansc\Pictures\checkboxes.png"},
            {"q": r"C:\Users\hansc\Pictures\clickabutton.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_24_31_797203.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_25_48_657510.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_26_16_431863.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_27_07_483808.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_27_41_985343.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_28_16_529438.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_28_55_105250.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_29_11_492492.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_05_38_13_226848.png"},
            {"q": r"C:\Users\hansc\Pictures\collage_2023_04_23_06_04_14_676085.png"},
            {'q':r"C:\Users\hansc\Downloads\IMG-20230618-WA0000.jpeg"},
            {'q':r"C:\Users\hansc\Downloads\maxresdefault.jpg"},
            {'q':r"C:\Users\hansc\Downloads\panda-with-broom-600x500 (1).jpg"},
            {'q':r"C:\Users\hansc\Downloads\panda-with-broom-600x500.jpg"},
            {'q':r"C:\Users\hansc\Downloads\panda-with-broom-600x500222222222.jpg"},
            {'q':r"C:\Users\hansc\Downloads\pexels-alex-andrews-2295744.jpg"},
            {'q':r"C:\Users\hansc\Downloads\pexels-niki-nagy-1128416.jpg"},

        ]
        b = start_multiprocessing(fu=somefu3, it=allimages, processes=3, chunks=5)
        print(b)
    """
    multidict = {}

    _ = [x.update({"resultindex": no}) for no, x in enumerate(it)]

    multidict["fu"] = dill.dumps(fu, protocol=dill.HIGHEST_PROTOCOL)
    multidict["procdata"] = it
    multidict["processes"] = processes
    multidict["chunks"] = chunks
    v = dill.dumps(multidict, protocol=dill.HIGHEST_PROTOCOL)
    osenv = os.environ.copy()
    osenv["___START___MULTIPROCESSING___"] = "1"
    p = subprocess.run(
        [sys.executable, __file__],
        **invisibledict,
        env=osenv,
        capture_output=True,
        input=b"STARTDATASTARTDATASTARTDATA" + v + b"ENDDATAENDDATAENDDATAENDDATA"
    )
    if print_stderr:
        for ste in p.stderr.decode("utf-8", "backslashreplace"):
            sys.stderr.write(ste)
            sys.stderr.flush()
    d = dill.loads(
        p.stdout.split(b"ENDEND1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1ENDEND")[1].split(
            b"DNE1YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYDNE1"
        )[0]
    )
    if print_stdout:
        print(d)
    return d


if __name__ == "__main__":
    if int(os.environ.get("___START___MULTIPROCESSING___", 0)):
        allmydata = []
        for xxxa in iter(sys.stdin.buffer.readline, b""):
            allmydata.append(xxxa)
        initdict = dill.loads(
            b"".join(allmydata)
            .split(b"STARTDATASTARTDATASTARTDATA")[1]
            .split(b"ENDDATAENDDATAENDDATAENDDATA")[0]
        )
        processes = initdict["processes"]
        chunks = initdict["chunks"]
        md = initdict["procdata"]
        with multiprocessing.Manager() as manager:
            shared_dict = manager.dict()

            with multiprocessing.Pool(
                processes=processes,
                initializer=init_worker,
                initargs=(initdict["fu"],),
            ) as pool:
                pool.starmap(
                    multifu,
                    ((value, shared_dict) for value in md),
                    chunksize=chunks,
                )
                alldataready2 = {o: b for o, b in shared_dict.items()}
                outd = dill.dumps(alldataready2, protocol=dill.HIGHEST_PROTOCOL)
                sys.stdout.buffer.write(
                    b"\n\n\nENDEND1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1ENDEND"
                    + outd
                    + b"DNE1YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYDNE1\n\n\n"
                )
                sys.stdout.buffer.flush()
