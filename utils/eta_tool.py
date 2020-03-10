import datetime
import threading
import os
import time


BYTE_TO_MB = 1048576
push_metrics = {'size': 147.68270778656006, 'time': 62}  # used to calculate push eta
up_speed_constant = 6.436  # used in up speed consideration


class ETATool:
  def __init__(self, op_base_dir, up_speed):  # only supports up to minutes
    self.op_base_dir = op_base_dir
    self.up_speed = up_speed

    self.print_freq = 15  # seconds

    self.last_print_time = time.time()
    self.to_run = True

  def start_eta(self):
    target_size = self.calculate_target_size()
    estimated_time = (target_size * push_metrics['time']) / push_metrics['size']
    estimated_time /= (self.up_speed / 8) * up_speed_constant  # speed consideration
    threading.Thread(target=self.eta_thread, args=(estimated_time,)).start()

  def eta_thread(self, estimated_time):
    start_time = time.time()
    while True:
      if not self.to_run:
        return
      if time.time() - self.last_print_time > self.print_freq:
        print('Pushing, ETA: {}'.format(self.get_eta(estimated_time - (time.time() - start_time))))
        self.last_print_time = time.time()
        time.sleep(self.print_freq / 2.0)
      if time.time() - start_time > estimated_time:
        print('Any second now...')
        return

  def calculate_target_size(self):
    repo_size = self.folder_size(self.op_base_dir)
    _git_size = self.folder_size('{}/.git'.format(self.op_base_dir))
    return (repo_size - _git_size) / BYTE_TO_MB

  def folder_size(self, path):
    total = 0
    for entry in os.scandir(path):
      if entry.is_file():
        total += entry.stat().st_size
      elif entry.is_dir():
        total += self.folder_size(entry.path)
    return total

  def stop(self):
    self.to_run = False

  def get_eta(self, etr):
    sec_string = ''
    min_string = ''
    etr = datetime.timedelta(seconds=round(etr))
    etr = str(etr).split(':')[-2:]
    minutes = int(etr[0])
    seconds = int(etr[1])

    sec_string += '{} second'.format(seconds)
    min_string += '{} minute'.format(minutes)

    if seconds != 1:
      sec_string += 's'
    if minutes != 1:
      min_string += 's'

    etr_string = []
    if minutes != 0:
      etr_string.append(min_string)
    etr_string.append(sec_string)
    etr_string = ', '.join(etr_string)

    return etr_string
