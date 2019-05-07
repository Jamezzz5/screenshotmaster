import sys
import logging
import argparse
import ssm.site as sit
import ssm.export as exp

formatter = logging.Formatter('%(asctime)s [%(module)14s]'
                              '[%(levelname)8s] %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)

console = logging.StreamHandler(sys.stdout)
console.setFormatter(formatter)
log.addHandler(console)

log_file = logging.FileHandler('logfile.log', mode='w')
log_file.setFormatter(formatter)
log.addHandler(log_file)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Uncaught exception: ",
                     exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

parser = argparse.ArgumentParser()
parser.add_argument('--ss', action='store_true')
parser.add_argument('--api', action='store_true')
parser.add_argument('--ad', action='store_true')
parser.add_argument('--date', type=str)
parser.add_argument('--exp', choices=['all', 'db', 'ftp'])
args = parser.parse_args()


def main():
    sc = sit.SiteConfig(ss_file_path_date=args.date)
    if args.ss or args.ad:
        sc.take_screenshots()
    if args.api:
        sc.upload_screenshots()
    if args.exp:
        eh = exp.ExportHandler()
        eh.export_loop(args.exp)


if __name__ == '__main__':
    main()
