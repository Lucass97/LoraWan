class Singleton:
    """
    A decorator for implementing the Singleton design pattern.

    :param callable cls: The class to be turned into a Singleton.
    """

    def __init__(self, cls) -> None:
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        """
        Overrides the call method to create a Singleton instance of the class.

        :param args: Positional arguments for the class constructor.
        :param kwargs: Keyword arguments for the class constructor.

        :return: The Singleton instance of the class.
        """
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance