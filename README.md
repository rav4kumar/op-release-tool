# op-release-tool
A tool for openpilot that creates squashed release branches for quick cloning.

In `op_releaser.py` simply change the following class variables to your liking and run the file!

Note: The `self.target_branch` will be overwritten every time you run the tool.

```python
class opReleaser:
  def __init__(self):
    """
      self.op_base_dir: Replace with the path leading to your local openpilot repository
      
      self.release_branch: Replace with the name of your most stable branch
      
      self.target_branch: Replace with the name of the target branch you
        want a squashed version of your release branch on
        
      self.commit_message: The commit message to be pushed to your target_branch.
        You can either use the included date function or remove it
    """
```

[An example release target branch.](https://github.com/ShaneSmiskol/openpilot/commits/stock_additions-release)
