import datetime
import subprocess
from utils.eta_tool import ETATool


up_speed = 1.2433  # in megabits, can replace with your github upload speed to get more accurate eta results


class opReleaser:
  def __init__(self):
    """
      self.op_base_dir: Replace with the path leading to your local openpilot repository
      self.release_branch: Replace with the name of your most stable branch
      self.target_branch: Replace with the name of the target branch you want a squashed version of your release branch on
      self.commit_message: The commit message to be pushed to your target_branch. You can either use the included date function or remove it
    """

    self.op_base_dir = 'C:/Git/op-smiskol/openpilot'
    self.release_branch = 'stock_additions'
    self.target_branch = 'stock_additions-release'
    self.commit_message = 'Stock Additions 0.2 (0.7.1) {} Release'.format(self.get_cur_date())

    self.eta_tool = ETATool(self.op_base_dir, up_speed)

    self.msg_count = 0
    self.total_steps = 3

    self.create_release()

  def create_release(self):
    # Checkout release branch
    r = self.run('git checkout {}'.format(self.release_branch))
    if any([True if r in i else False for i in ['Switched to branch', 'Already on']]):
      raise Exception('Error checking out release branch!')

    # Delete old target branch if it exists
    self.attempt_delete()

    # Checkout a new orphan branch
    r = self.run('git checkout --orphan {}'.format(self.target_branch))
    if 'Switched to a new branch' not in r:
      raise Exception('Error switching to target branch!')

    # Add all files in release branch to new target branch
    self.message('Adding and committing all files to {} branch...'.format(self.target_branch))
    self.run('git add --all')

    # Commit all files
    r = self.run(['git', 'commit', '-am', self.commit_message], no_convert=True)

    if 'create mode' not in r:
      raise Exception('Error adding files to current branch!')

    self.eta_tool.start_eta()

    # Replace current release on remote
    self.message('Now force pushing to remote (origin/{})...'.format(self.target_branch))
    self.run('git push -f --set-upstream origin {}'.format(self.target_branch))
    self.eta_tool.stop()

    # Check the release branch back out
    self.run('git checkout {}'.format(self.release_branch))

    # Finished
    print('\nFinished! Squashed {} branch to 1 commit and force pushed to {} branch!'.format(self.release_branch, self.target_branch))
    print('Commit message: {}'.format(self.commit_message))

  def run(self, cmd, no_convert=False):
    if not no_convert:
      cmd = cmd.split(' ')
    return subprocess.check_output(cmd, cwd=self.op_base_dir, stderr=subprocess.STDOUT, encoding='utf8')

  def attempt_delete(self):
    try:
      r = self.run('git branch -D {}'.format(self.target_branch))
      self.message(r.replace('\n', ''))
    except subprocess.CalledProcessError:
      self.message('{} branch already deleted.'.format(self.target_branch))

  def get_cur_date(self):
    today = datetime.datetime.today()
    return today.strftime('%h %d, %Y').replace(' 0', ' ')

  def message(self, msg):
    print('[{}/{}]: {}'.format(self.msg_count + 1, self.total_steps, msg), flush=True)
    self.msg_count += 1


opReleaser()
