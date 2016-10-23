import os
import logging
import argparse
from datetime import datetime

from data import Frame
from data import FrameInputError

ErrNoSuchDirectory = "No such directory {}"
ErrNoFilesFound = "No files found in {}"
ErrNoFramesFound = "No frames found"
ErrFrameInput = "Could not parse frame info: {}"


def list_files(directory):
    """ Returns list of available files from input directory """
    if not (os.path.isdir(directory)):
        logging.error(ErrNoSuchDirectory.format(directory))
        return []
    return [os.path.join(directory, _file) for _file in os.listdir(directory) if
            os.path.isfile(os.path.join(directory, _file))]


def process_file(input_file):
    """ Returns list of frames extracted from input file """
    with open(input_file) as _file:
        lines = map(lambda line: line.replace('\n', '').split(","), _file.readlines())
        try:
            _frames = [Frame(line[0], *line[1:]) for line in lines if len(line) == 4]
        except FrameInputError as e:
            logging.error(ErrFrameInput.format(e.args[0]))
            return []
    return _frames


def process_frames(_frames):
    """ Returns dictionary where frames are counted. Frame ID is dict key """
    _by_frame_id = {}
    for _frame in _frames:
        if _by_frame_id.get(_frame.frame_id):
            _by_frame_id[_frame.frame_id] += 1
        else:
            _by_frame_id[_frame.frame_id] = 1
    return _by_frame_id


def extract_percentile(frames_count, total_frames, percentile):
    """ Returns a list of frames which are present in at least percentile of the files """
    return [frame_id for frame_id, frame_count in frames_count.items() if frame_count / total_frames * 100 > percentile]


def save_results(_frames, result_file="results.txt"):
    with open(result_file, mode='wt', encoding='utf-8') as results:
        results.write("\n".join(_frames))
        logging.info("Saved {} frames to {}".format(len(_frames), result_file))


def main(_args):
    """ Parses and processes files based on arguments provided. Output saved to file"""
    file_list = list_files(_args.directory)
    if not file_list:
        logging.error(ErrNoFilesFound.format(_args.directory))
        return -1

    logging.debug("Found files: {}".format("; ".join(file_list)))

    frames = []
    for frame in file_list:
        frames.extend(process_file(frame))
    if not frames:
        logging.error(ErrNoFramesFound)
        return -1

    by_frame_id = process_frames(frames)
    logging.debug(by_frame_id)

    extracted = extract_percentile(by_frame_id, len(frames), _args.percentage)
    logging.debug(";".join(extracted))

    output_file = "{}-frames-{}.txt".format(datetime.now().strftime("%d-%m-%y_%H%M%S"), args.percentage)
    save_results(extracted, output_file)
    return 1


if __name__ == '__main__':
    log_level = os.environ.get("FRAMES_DEBUG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s [%(levelname)s] {%(funcName)s} : %(message)s', level=log_level)
    logging.info("Log level {}".format(log_level))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True, help="directory with frame files")
    parser.add_argument("-p", "--percentage", required=True, type=float,
                        help="down boundary for frame occurrence expressed as percentage")

    args = parser.parse_args()
    logging.info("Script started with directory={} and percentage={}".format(args.directory, args.percentage))

    main(args)
