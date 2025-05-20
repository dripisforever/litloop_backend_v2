class ShardRouter:
    def db_for_read(self, model, **hints):
        user_id = self._get_user_id(model, hints)
        return self._get_db(user_id)

    def db_for_write(self, model, **hints):
        user_id = self._get_user_id(model, hints)
        return self._get_db(user_id)

    def allow_relation(self, obj1, obj2, **hints):
        return True  # or restrict to same db

    def _get_user_id(self, model, hints):
        if 'instance' in hints:
            instance = hints['instance']
            if hasattr(instance, 'user_id'):
                return instance.user_id
            if hasattr(instance, 'author_id'):
                return instance.author_id
        elif 'user_id' in hints:
            return hints['user_id']
        return None

    def _get_db(self, user_id):
        if user_id is None:
            return 'default'
        return f'shard_{user_id % 100}'  # or however you name shards
