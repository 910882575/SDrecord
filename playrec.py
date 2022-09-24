#import sounddevice as sd
#
#fs = 44100
#
#def callback(indata, outdata, frames, time, status):
#    if status:
#        print(status)
#    outdata[:] = indata
#
#print(sd.query_devices())
#
#try:
#    with sd.Stream(device=(0,1), samplerate=fs, dtype='float32', latency=None, channels=2, callback=callback):
#        input()
#except KeyboardInterrupt:
#    pass

import argparse
import tempfile
import sounddevice as sd
import soundfile as sf

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
parser.add_argument(
    '-din', '--devicein', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-dout', '--deviceout', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-fin', '--filein', type=str, 
    help='audio file to store recording to')
parser.add_argument(
    '-fout', '--fileout', type=str, 
    help='audio file to play')

args = parser.parse_args()

if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
if args.filein is None:
    args.filein = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')
if args.fileout is None:   
    print('Error: No file to be played ... ')
    parser.exit(0)   
    
sd.default.device = [args.devicein,args.deviceout]
data, fs = sf.read(args.fileout, always_2d=True)
record= sd.playrec(data, fs, channels=args.channels)
sd.wait()
sf.write(args.filein, record, fs)
