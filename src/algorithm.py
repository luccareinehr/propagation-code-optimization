class Algorithm:
    def __init__(self, args, hparams) -> None:
        self.args = args
        self.hparams = hparams

    def run(self, num_steps) -> None:
        raise NotImplementedError