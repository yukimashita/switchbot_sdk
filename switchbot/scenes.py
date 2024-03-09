class SwitchBotScene:
    def __init__(self, client,
                 sceneId=None,
                 sceneName=None):
        self.client = client
        self.sceneId = sceneId
        self.sceneName = sceneName
        self._scenes = None

    def _path(self, path=None):
        if path is None:
            return f'scenes/{self.sceneId}'
        if path.startswith('/'):
            path = path[1:]
        return f'scenes/{self.sceneId}/{path}'

    def execute(self):
        path = self._path('execute')
        return self.client.post_json(path, data=None)

    def __str__(self):
        class_name = type(self).__name__
        return f'<<{class_name}: {self.sceneName}>>'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_json(cls, client, scene_json):
        return cls(client, **scene_json)

    @classmethod
    def from_scene_list(cls, client, scene_list):
        return [SwitchBotScene.from_json(client, s) for s in scene_list]
