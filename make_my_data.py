import pathlib
import sys

import soundfile as sf
from scipy import signal


# process wav files
def wavread(fn, resr=None):
    if resr is None:
        data, sr = sf.read(fn)
    else:
        data, sr = sf.read(fn)
        data = signal.resample(data, int(resr * len(data) / sr))
        sr = resr
    f = sf.info(fn)
    return data, sr, f.subtype


def wavwrite(fn, data, sr, subtype, resr=None):
    if resr is None:
        sf.write(fn, data, sr, subtype)
    else:
        data = signal.resample(data, int(resr * len(data) / sr))
        sf.write(fn, data, resr, subtype)


def make_my_data():
    fs = int(sys.argv[1])

    path = pathlib.Path("./Data")

    file = list(path.glob("*.wav"))

    for f in file:
        data, sr, subtype = wavread(f, resr=fs)
        if data.ndim == 2:  # stereo
            wavwrite(
                "./MyData/" + f.stem + ".wav",
                data[:, 0],
                fs,
                subtype,
            )
        else:  # mono
            wavwrite(
                "./MyData/" + f.stem + ".wav",
                data,
                fs,
                subtype,
            )


if __name__ == "__main__":
    make_my_data()
